#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker.utils import functions


def install():
    from MySQLdb.cursors import DictCursor as Cursor

    _execute = Cursor.execute

    def _fast_execute(this: Cursor, query, args=None):
        peer = "%s:%s" % (this.connection.get_host_info(), getattr(this.connection, 'port', ''))

        context = get_context()
        with context.new_exit_span(op="Mysql/MySQLdb/execute", peer=peer) as span:
            span.layer = Layer.Database
            span.component = ComponentType.MySQLdb
            res = _execute(this, query, args)

            span.tag(Tag(key=tags.DbType, val="mysql"))
            span.tag(Tag(key=tags.DbInstance, val=(getattr(this.connection, 'db', b'') or b'').decode("utf-8")))
            span.tag(Tag(key=tags.DbStatement, val=query))

            functions.log("mysql span is: %r", span)

            return res

    Cursor.execute = _fast_execute
