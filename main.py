#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import fdb
import psycopg2
import argparse
import logging
import re

parser = argparse.ArgumentParser(description='fb2psql')
parser.add_argument('--fb-host', dest='fb_host', default='localhost')
parser.add_argument('--fb-database', dest='fb_database', default='')
parser.add_argument('--fb-user', dest='fb_user', default='sysdba')
parser.add_argument('--fb-password', dest='fb_password', default='masterkey')

parser.add_argument('--pq-host', dest='pq_host', default='localhost')
parser.add_argument('--pq-database', dest='pq_database', default='postgres')
parser.add_argument('--pq-user', dest='pq_user', default='postgres')
parser.add_argument('--pq-password', dest='pq_password', default='postgres')

args = parser.parse_args()

logger = logging.getLogger('fb2psql')
formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d, %(name)s, %(levelname)s, %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def run_query(cursor, qry):
    start = time.time()
    qry = re.sub('^([ \n]+)', '', qry)
    qry = re.sub('[ \n]+', ' ', qry)
    cursor.execute(qry)
    try:
        retval = cursor.fetchall()
    except psycopg2.ProgrammingError:
        retval = []
    logger.info('(%.3fs) %s' % (time.time() - start, qry.replace('\n', ' ')[:1000]))
    return retval


def drop_table(cursor, table):
    return run_query(cursor, 'drop table if exists %(table)s' % locals())


def null_str(nullable):
    return 'NULL' if nullable else 'NOT NULL'


def default_str(cursor, default):
    if default is not None:
        # default = "'%s'" % default if isinstance(default, (str, unicode)) else default
        return 'DEFAULT %s' % default
    return ''


def unique_str(unique):
    return 'UNIQUE ' if unique else ''


def create_column(cursor, column):
    datatype = column.datatype
    if datatype.startswith('BLOB '):
        datatype = 'bytea'
    return '%s %s %s %s' % (
        column.name,
        datatype,
        null_str(column.isnullable()),
        default_str(pq_cursor, column.default)
    )


def create_constraint(cursor, constraint):
    if constraint.ispkey():
        return 'PRIMARY KEY (%s)' % ','.join([s.name for s in constraint.index.segments])


def consider_constraint(constraint):
    return constraint.ispkey()


def insert_data(cursor, rows, it):
        fields = len(rows) // it
        template = '(' + ', '.join(['%s'] * fields) + ')'
        template = ', '.join([template] * it)
        qry = 'INSERT INTO %s values %s' % (table.name, template)
        cursor.execute(qry, rows)
        table_name = table.name
        logger.info('Saving %(it)s elements in %(table_name)s' % locals())


def copy_data(table, fb_cursor, pq_cursor, bulk_nb=1000):
    values = []
    it = 0
    for row in run_query(fb_cursor, 'SELECT * FROM %s' % table.name):
        values.extend(row)
        it += 1
        if it % bulk_nb == 0:
            insert_data(pq_cursor, values, it)
            values = []
            it = 0
    if it:
        insert_data(pq_cursor, values, it)

if __name__ == '__main__':
    fb_args = dict([(k[3:], v) for k, v in args.__dict__.items() if k.startswith('fb_')])
    fb_conn = fdb.connect(**fb_args)
    fb_cursor = fb_conn.cursor()
    pq_args = dict([(k[3:], v) for k, v in args.__dict__.items() if k.startswith('pq_')])
    pq_conn = psycopg2.connect(**pq_args)
    pq_cursor = pq_conn.cursor()

    for table in fb_conn.schema.tables:
        drop_table(pq_cursor, table.name)
        columns = [create_column(pq_cursor, column) for column in table.columns]
        constraints = [create_constraint(pq_cursor, constraint) for constraint in table.constraints if consider_constraint(constraint)]
        qry = """
            create table %s
            (%s)
        """ % (table.name, ', '.join(columns + constraints))
        run_query(pq_cursor, qry)
        for index in table.indices:
            if not index.constraint or not index.constraint.ispkey():
                run_query(pq_cursor, 'create %s index %s on %s(%s)' % (unique_str(index.isunique()), index.name, table.name, ', '.join([c.name for c in index.segments])))
        copy_data(table, fb_cursor, pq_cursor)

    pq_conn.commit()
