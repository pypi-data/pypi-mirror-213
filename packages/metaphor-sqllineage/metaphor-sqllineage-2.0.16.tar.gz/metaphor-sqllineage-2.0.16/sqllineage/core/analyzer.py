from functools import reduce
from operator import add
from typing import Dict, List, NamedTuple, Optional, Set, Union

from sqlparse.sql import (
    Function,
    Identifier,
    IdentifierList,
    Statement,
    TokenList,
    Where,
)

from sqllineage.core.handlers.base import CurrentTokenBaseHandler, NextTokenBaseHandler
from sqllineage.core.holders import StatementLineageHolder, SubQueryLineageHolder
from sqllineage.core.models import Column, SubQuery, Table, TableMetadata
from sqllineage.exceptions import SQLLineageException
from sqllineage.utils.constant import EdgeType
from sqllineage.utils.sqlparse import (
    get_subquery_parentheses,
    is_subquery,
    is_token_negligible,
)


class AnalyzerContext(NamedTuple):
    subquery: Optional[SubQuery] = None
    prev_cte: Optional[Dict[SubQuery, Set[Column]]] = None


class LineageAnalyzer:
    """SQL Statement Level Lineage Analyzer."""

    def analyze(
        self, stmt: Statement, metadata=TableMetadata()
    ) -> StatementLineageHolder:
        """
        to analyze the Statement and store the result into :class:`sqllineage.holders.StatementLineageHolder`.

        :param stmt: a SQL statement parsed by `sqlparse`
        :param metadata: metadata of the statement
        """
        if (
            stmt.get_type() == "DELETE"
            or stmt.token_first(skip_cm=True).normalized == "TRUNCATE"
            or stmt.token_first(skip_cm=True).normalized.upper() == "REFRESH"
            or stmt.token_first(skip_cm=True).normalized == "CACHE"
            or stmt.token_first(skip_cm=True).normalized.upper() == "UNCACHE"
            or stmt.token_first(skip_cm=True).normalized == "SHOW"
        ):
            holder = StatementLineageHolder()
        elif stmt.get_type() == "DROP":
            holder = self._extract_from_ddl_drop(stmt, metadata)
        elif (
            stmt.get_type() == "ALTER"
            or stmt.token_first(skip_cm=True).normalized == "RENAME"
        ):
            holder = self._extract_from_ddl_alter(stmt, metadata)
        else:
            # DML parsing logic also applies to CREATE DDL
            holder = StatementLineageHolder.of(
                self._extract_from_dml(stmt, AnalyzerContext(), metadata)
            )
        return holder

    @classmethod
    def _extract_from_ddl_drop(
        cls, stmt: Statement, metadata: TableMetadata
    ) -> StatementLineageHolder:
        holder = StatementLineageHolder()
        for table in {
            Table.of(t, metadata) for t in stmt.tokens if isinstance(t, Identifier)
        }:
            holder.add_drop(table)
        return holder

    @classmethod
    def _extract_from_ddl_alter(
        cls, stmt: Statement, metadata: TableMetadata
    ) -> StatementLineageHolder:
        holder = StatementLineageHolder()
        tables = []
        for t in stmt.tokens:
            if isinstance(t, Identifier):
                tables.append(Table.of(t, metadata))
            elif isinstance(t, IdentifierList):
                for identifier in t.get_identifiers():
                    tables.append(Table.of(identifier, metadata))

        keywords = [t for t in stmt.tokens if t.is_keyword]
        if any(k.normalized == "RENAME" for k in keywords):
            if stmt.get_type() == "ALTER" and len(tables) == 2:
                holder.add_rename(tables[0], tables[1])
            elif (
                stmt.token_first(skip_cm=True).normalized == "RENAME"
                and len(tables) % 2 == 0
            ):
                for i in range(0, len(tables), 2):
                    holder.add_rename(tables[i], tables[i + 1])
        if any(k.normalized == "EXCHANGE" for k in keywords) and len(tables) == 2:
            holder.add_write(tables[0])
            holder.add_read(tables[1])
        return holder

    @classmethod
    def _extract_from_dml(
        cls, token: TokenList, context: AnalyzerContext, metadata: TableMetadata
    ) -> SubQueryLineageHolder:
        holder = SubQueryLineageHolder()
        if context.prev_cte is not None:
            # CTE can be referenced by subsequent CTEs
            for cte, columns in context.prev_cte.items():
                holder.add_cte(cte)
                for column in columns:
                    holder.add_table_has_column(column)

        if context.subquery is not None:
            # If within subquery, then manually add subquery as target table
            holder.add_write(context.subquery)

        current_handlers = [
            handler_cls() for handler_cls in CurrentTokenBaseHandler.__subclasses__()
        ]
        next_handlers = [
            handler_cls(metadata)
            for handler_cls in NextTokenBaseHandler.__subclasses__()
        ]

        subqueries = []
        for sub_token in token.tokens:
            if is_token_negligible(sub_token):
                continue

            for sq in cls.parse_subquery(sub_token):
                # Collecting subquery on the way, hold on parsing until last
                # so that each handler don't have to worry about what's inside subquery
                subqueries.append(sq)

            for current_handler in current_handlers:
                current_handler.handle(sub_token, holder)

            if sub_token.is_keyword:
                for next_handler in next_handlers:
                    next_handler.indicate(sub_token)
                continue

            for next_handler in next_handlers:
                if next_handler.indicator:
                    next_handler.handle(sub_token, holder)
        else:
            # call end of query hook here as loop is over
            target_table = None
            if holder.write:
                if len(holder.write) > 1:
                    raise SQLLineageException
                target_table = next(iter(holder.write))

            # recursively extracting each subquery of the parent and merge
            for sq in subqueries:
                prev_cte = cls._find_cte_columns(holder)
                sq_holder = cls._extract_from_dml(
                    sq.token, AnalyzerContext(sq, prev_cte), metadata
                )
                holder |= sq_holder

            for next_handler in next_handlers:
                next_handler.end_of_query_cleanup(holder, target_table)

        return holder

    @classmethod
    def _find_cte_columns(
        cls,
        holder: SubQueryLineageHolder,
    ) -> Dict[SubQuery, Set[Column]]:
        """
        Finds the previous CTEs and their columns from the holder graph
        """
        mapping: Dict[SubQuery, Set[Column]] = {}
        for src, tgt, attr in holder.graph.edges(data=True):
            if attr.get("type") == EdgeType.HAS_COLUMN and src in holder.cte:
                if src not in mapping:
                    mapping[src] = set()
                mapping[src].add(tgt)

        return mapping

    @classmethod
    def parse_subquery(cls, token: TokenList) -> List[SubQuery]:
        result = []
        if isinstance(token, (Identifier, Function, Where)):
            # usually SubQuery is an Identifier, but not all Identifiers are SubQuery
            # Function for CTE without AS keyword
            result = cls._parse_subquery(token)
        elif isinstance(token, IdentifierList):
            # IdentifierList for SQL89 style of JOIN or multiple CTEs, this is actually SubQueries
            result = reduce(
                add,
                [
                    cls._parse_subquery(identifier)
                    for identifier in token.get_sublists()
                ],
                [],
            )
        elif is_subquery(token):
            # Parenthesis for SubQuery without alias, this is valid syntax for certain SQL dialect
            result = [SubQuery.of(token, None)]
        return result

    @classmethod
    def _parse_subquery(
        cls, token: Union[Identifier, Function, Where]
    ) -> List[SubQuery]:
        """
        convert SubQueryTuple to sqllineage.core.models.SubQuery
        """
        return [
            SubQuery.of(parenthesis, alias)
            for parenthesis, alias in get_subquery_parentheses(token)
        ]
