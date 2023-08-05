import os
from mysql.connector import Error
import mysql.connector

class MySQLUtils:
     def __init__(self):
         config = {
             'host': 'localhost',
              'user':'root',
              'password': 'AlexZara20-20',
             'database': 'point'
         }

         self.param = config
         self.connection = None
         self.cursor = None

     def __enter__(self):
         self.connect()
         return self

     def __exit__(self, *args, **kwargs):
         self.close()
         return not (any([args, kwargs]))


     def connect(self):
         if not self.connection:
             try:
                 self.connection = mysql.connector.connect(**self.param)
             except Error as e:
                 print(e)

     def close(self):
         if self.connection:
             self.connection.close()


     def get_cursor(self):
        if not self.cursor:
            self.cursor = self.connection.cursor()
        return self.cursor

     def insert_data(self, object_name, x, y):
         insert_query = "INSERT INTO point (type_point, point_x, point_y) VALUES (%s, %s, %s)"
         data = (object_name, x, y)
         self.get_cursor().execute(insert_query, data)
         self.connection.commit()


     def querying_data(self, custom_point_type):
         query = "SELECT point_x, point_y FROM point WHERE type_point = '{}'".format(custom_point_type)
         self.get_cursor().execute(query)
         result = self.get_cursor().fetchall()
         return result


     def delete_data(self):
         delete_query = "DELETE FROM point"
         self.get_cursor().execute(delete_query)
         self.connection.commit()