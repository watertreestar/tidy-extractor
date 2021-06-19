#!/usr/python3
# coding=utf-8

import pymysql
from tools.logger import logger


class MySQLExporter:
    """
    Exporter for MySQL destination
    """

    def __init__(self, host, port, db, user, passwd):
        """
        Create connection to MySQL database
        :param db:
        :param user:
        :param pwd:
        """
        logger.info("Starting create database connection.........")
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        self.cur = self.conn.cursor()
        logger.info("Finished creating database connection..........")

    def export(self, table, data):
        """
        Insert data to specific table
        :param table:  table name to insert
        :param data:   tuple list to insert. Just like [('name','watertreestar'),('age',18),........]
        :return:
        """
        columns = []
        values = []
        if isinstance(data, list):
            for d_tuple in data:
                if not isinstance(d_tuple, tuple):
                    continue
                columns.append(d_tuple[0])
                values.append(d_tuple[1])

        sql = "insert into " + table + "("
        sql += ",".join(columns)
        sql += ') values ('
        for v in values:
            if type(v) == str:
                v = v.replace("'", "")
                v = v.replace('"', '')
                sql += "'" + v + "',"
            else:
                sql += v + ','
        sql = sql[:-1]
        sql += ")"

        logger.debug("Export sql is [%s]", sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.exception("Exception occurs while export to mysql db,%s", e)

    def exist(self, table, cond):
        sql = "select count(*) from " + table + " where " + cond[0] + "='" + cond[1] + "'"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        if result and result[0][0] == 1:
            return True
        return False
