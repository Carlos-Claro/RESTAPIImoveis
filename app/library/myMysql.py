#!/usr/bin/python3

import mysql.connector as mysql
from mysql.connector import Error
import json


class myMysql(object):
    
    def __init__(self):
        self.getDataconnection();
        
    def add(self,query):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            id = cursor.lastrowid
            return id
        except Error as error :
            conn.rollback() #rollback if any exception occured
            print("Failed inserting record into python_users table {}".format(error))
        finally:
            #closing database connection.
            if(conn.is_connected()):
                cursor.close()
                conn.close()
                print("MySQL connection is closed")
    
    def update(self,query):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return True
        except Error as error :
            conn.rollback() #rollback if any exception occured
            print("Failed update record into python_users table {}".format(error))
        finally:
            #closing database connection.
            if(conn.is_connected()):
                cursor.close()
                conn.close()
                print("MySQL connection is closed")
    
    def delete(self,query):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return True
        except Error as error :
            conn.rollback() #rollback if any exception occured
            print("Failed delete record into python_users table {}".format(error))
        finally:
            #closing database connection.
            if(conn.is_connected()):
                cursor.close()
                conn.close()
    
    def get(self,query):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        retorno = cursor.fetchall()
        conn.close()
        return retorno
    
    def getDataconnection(self):
        with open('/var/www/json/keys.json') as json_file:
            data = json.load(json_file)
            #print(data['database']['localhost']['guiasjp'])
            self.data = data['database']['server']['guiasjp']
        

    def connect(self):
        try:
            data = self.data
            conn = mysql.connect(
                    host=data['hostname'],
                    user=data['username'],
                    passwd=data['password'],
                    database=data['database']
                    );
            return conn
        except Error as e:
            print(e)
            
    

if __name__ == '__main__':
    try:
        a = myMysql()
        b = a.get('SELECT * FROM imoveis LIMIT 2')
        for c in b:
            print(c)
    except KeyboardInterrupt:
        pass
    finally:
        print("Connectionclose")

    #myConnection.connect()
        

    
     