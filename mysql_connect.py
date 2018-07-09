#!/usr/bin/env python
# coding=utf-8
from errno import errorcode

import mysql.connector, sys
from collections import OrderedDict


class MysqlConnect(object):
    """
        Python Class for connecting  with MySQL server and accelerate development project using MySQL
        Extremely easy to learn and use, friendly construction.
    """

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    ## End def __init__

    def __open(self):
        try:
            config = {
                'user': self.__user,
                'password': self.__password,
                'host': self.__host,
                'database': self.__database,
                'raise_on_warnings': True,
            }
            cnx = mysql.connector.connect(**config)
            self.__connection = cnx
            self.__session = cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    ## End def __open

    def __close(self):
        self.__session.close()
        self.__connection.close()

    ## End def __close

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","
        ## End for keys

    def select_advanced(self, sql, tp=None):
        results = None
        self.__open()
        self.__session.execute(sql, tp)
        result = self.__session.fetchall()

        number_rows = len(result)
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            results = result
        else:
            results = [item[0] for item in result]
        self.__close()

        return results

    ## End def select_advanced

    def update(self, table, where=None, *args, **kwargs):
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "` = %s"
            if i < l:
                query += ","
            ## End if i less than 1
        ## End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows

    ## End function update

    def update_advanced(self, sql, tp=None):
        self.__open()
        self.__session.execute(sql, tp)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows

    ## End function update_advanced

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"] * len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"] * len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid

    ## End def insert

    def insert_bulk(self, sql, values):
        self.__open()
        self.__session.executemany(sql, values)
        self.__connection.commit()
        self.__close()
        return self.__session.rowcount

    ## End def insert_bulk

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows

    ## End def delete

## End class
