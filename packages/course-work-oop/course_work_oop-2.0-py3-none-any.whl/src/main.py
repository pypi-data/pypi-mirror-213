# This is a sample Python script.
import sys

from src.database.mysql_connector import MySQLUtils
from src.point_present.complex_number import ComplexNumber
from src.point_present import Fraction
from src.point_present.point import Point


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def main():

    arg = sys.argv[1]
    arg_1 = sys.argv[2]

    sql_work = MySQLUtils()
    sql_work.connect()
    sql_work.delete_data()
    sql_work.insert_data("Fraction", 3, 6)
    sql_work.insert_data("Point", 4, 1)
    sql_work.insert_data("Complex number", 5, 6)

    point = Point(sql_work.querying_data("Point")[0][0], sql_work.querying_data("Point")[0][1])
    fraction = Fraction(sql_work.querying_data("Fraction")[0][0], sql_work.querying_data("Fraction")[0][1])
    complex_num = ComplexNumber(sql_work.querying_data("Complex number")[0][0], sql_work.querying_data("Complex number")[0][1])

    action = {
        'Point': point.action(arg_1, point),
        'Fraction': fraction.action(arg_1, point),
        'Complex': complex_num.action(arg_1, complex_num)
    }

    print(action[arg])

if __name__ == '__main__':
    main()

