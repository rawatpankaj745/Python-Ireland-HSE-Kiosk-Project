
#! /usr/bin/env python3


""" Importing of Modules    """       


import sys
import subprocess as sp
import argparse
import re
import csv
import sqlite3
import platform
from sqlite3 import Error
from inputimeout import inputimeout,TimeoutOccurred
from urllib.request import pathname2url
import getpass

""" Declaration of Global Variables """

__author__ = "Pankaj Singh Rawat- C00290835"
__copyright__ = "Copyright 2022, SETU - Campus Carlow"
__licence__ = "European Union Public Licence v1.2"
__version__ = "v 0.1a"
__program__ = sys.argv[0][2:] if (sys.argv[0][:2] == "./") else sys.argv[0]
time_limit = 120
table = "health_centres"
database = "db_hse.sqlite"

""" All Functions are written below """

"""This function is used for the connectivity of the sqllite database."""


def query_(query):
    """Query function for the Database"""
    database = "db_hse.sqlite"
    list_ = list()
    with sqlite3.connect(database) as con:
        cur = con.cursor()
        cur.execute(query)
        list_ = cur.fetchall()  
        cur.close()  
        con.commit()  
    return (list_)


"""This function is used for read the csv file"""


def csv_import(hse_csv):
    header = list()
    data = list()
    with open(hse_csv, mode="r", encoding="utf8") as fh:
        csv_read = list(csv.reader(fh))
        header = csv_read[0]
        data = csv_read[1:]

#    underscore in the header

    header2 = list()
    for x in header:
        header2.append(re.sub(r"\s+", '_', x))

#   argument for DB table to add primary key
    header3 = dict()
    header3 = {header2[0]: "TEXT PRIMARY KEY"}

#   argument for the remaining header just as text
    for x in header2[1:]:
        header3[x] = "TEXT"

    list_ = list()

    for (key, value) in header3.items():
        list_.append(f"{key} {value}")
        str_ = ", ".join(list_)

    query_(f"CREATE TABLE IF NOT EXISTS {table} ({str_})")

    header3 = tuple(header2)

    for d in data:
        try:
            d2 = tuple(d)
            query_(f"INSERT INTO {table} {header3} VALUES {d2}")
        except:
            continue


def get_column_names():
    output_ = query_(f"PRAGMA table_info({table})")
    columns = list()
    for a in output_:
        columns.append(a[1])

    return (columns)


def clear_screen():
    if platform.system().lower() == 'windows':
        sp.run('cls')
    else:
        sp.run('clear')


def timer(time_len):
    ''' Timer in seconds '''

    try:
        inputimeout(prompt='\nPress ENTER to continue',
                    timeout=time_len)
        return (0)
    except TimeoutOccurred:
        return (1)

#  This is the main menu function

def main_menu():
    clear_screen()
    print("\n\tYou are welcome to the Ireland HSE information Kiosk "
          "\n\tchoose from the available options"
          "\n\n\tHSE Location search"
          "\n\t1.By town "
          "\n\t2.By location"
          "\n\n\tSpecific searches"
          "\n\t3. Phone number search"
          "\n\t4. Location search"
          "\n\t5. Role search\n\n")
    return input("\tSelection: ")

def sub_menu(input_):
    header = get_column_names()
    t2 = len(max(header, key=len)) + 2

    if input_ == 1:
        x = input("\tWhich town?:  ")
        output_ = query_(f"SELECT * FROM {table} WHERE Town LIKE ('%{x}%')")

    if input_ == 2:
        x = input("\tWhich location?:  ")
        output_ = query_(f"SELECT * FROM {table} WHERE Hospital_name LIKE \
                         ('%{x}%')")

    if input_ == 3:
        x = input("\tWhich hospital or location?:  ")
        output_ = query_(f"SELECT Hospital_name, Phone FROM {table} WHERE \
                         Town LIKE ('%{x}%')")
        header = ("Hospital Name", "Phone")
        t2 = len(max(header, key=len)) + 2

    if input_ == 4:
        x = input("\tWhich area?  ")
        output_ = query_(f"SELECT Hospital_name, Latitude, Longitude, Address,\
                         Town, Eircode FROM {table} WHERE Hospital_name LIKE \
                         ('%{x}%') OR Town LIKE ('%{x}%')")
        header = ("Hospital Name", "Latitude", "Longitude", "Address", "Town",
                  "Eircode")

    if input_ == 5:
        x = input("\tWhich Hospital or Location?  ")
        role_ = list()
        role_ = query_(f"SELECT DISTINCT Role FROM {table}")
        list4 = [x[0] for x in role_]

        for index, item in enumerate(list4):
            print(f"{index}. {item}")

        z = input("\t\n Select required role: ")
        w = int(z)
        y = list4[w]

        output_ = query_(f"SELECT Hospital_name FROM {table} WHERE Role LIKE \
                         ('%{y}%') AND Town LIKE ('%{x}%')")

        print("\n")
        for a in output_:
            output2_ = list(a)
            for b in range(len(output2_)):
                print(f"{y : <}: {color_text(32)}{output2_[b]}{color_text(0)}")
        timer(time_limit)
        main(parser.parse_args())

    for a in output_:
        output2_ = list(a)
        for b in range(len(output2_)):
            print(f"{header[b] : <{t2}}: {color_text(32)}{output2_[b]}\
                  {color_text(0)}")
        print("\n")
    timer(time_limit)
    main(parser.parse_args())


def admin_page():
    clear_screen()
    j = getpass.getpass(prompt="\n\tType in your password: ")

    if j.lower() == "kenobi":

        print(f"{color_text(32)}\n\tWelcome to the Admin page{color_text(0)}"
              "\n\tHello there!"
              f"\n\t{color_text(32)}General Kenobi!{color_text(0)}"
              "\n\tThe force is strong with you"
              "\n\tWith great power comes greate responsability!\n\n"
              "\n\tYou have 2 options:"
              "\n\t1. Update your database by providing a new CSV file."
              "\n\t2. You want to exit the program.")

        x = input("\n\tEnter the option number you want to pursue: ")

        if x.lower() == "1":
            aux = 1
        elif x.lower() == "2":
            aux = 2
        else:
            aux = 3

        if aux == 1:
            print("\n\tThe CSV file has to be in the same folder as program!")
            csv_file_name = input("\n\tWhat's the CSV file name? ")
            try:
                query_(f"DROP TABLE IF EXISTS {table}")
                csv_import(csv_file_name)
            except:
                print("\n\tThis file does not exist!")
        elif aux == 2:
            sys.exit(1)

        w = input("\n\tDo you want to exit to main menu? (yes/no): ")

        if w.lower() == "Yes":
            main(parser.parse_args())
        elif w.lower() == "y":
            main(parser.parse_args())
        elif w.lower() == "yes":
            main(parser.parse_args())
        else:
            admin_page()

    else:
        print(f"\n\t{color_text(31)}You're weak with the force{color_text(0)}")
        timer(time_limit)
        main(parser.parse_args())

    admin_page()


def color_text(code):
    return "\33[{code}m".format(code=code)


def initial_menu():
    clear_screen()
    print("\n\tThis is the initialization screen for"
          "\n\tthe HSE information Kiosk!"
          "\n\tPlease indicate the source CSV file:\n\n")
    return input("\tSelection: ")

"""  main() Function """         


def main(nspace):
    if nspace.licence:
        list_A = ["Author", "Copyright", "Licence"]
        list_B = [__author__, __copyright__, __licence__]

        tl = len(max(list_A, key=len)) + 2
        print("\n")

        for a in range(0, 3):
            print(f"{list_A[a] : <{tl}}: {list_B[a]}")

        print("\n")

    else:

        try:
            dbfile = 'file:{}?mode=rw'.format(pathname2url(database))
            conn = sqlite3.connect(dbfile, uri=True)
        except sqlite3.OperationalError:
            hse_csv = "ireland_health_centres.csv"
            csv_import(hse_csv)

        match main_menu():
            case '1':
                sub_menu(1)

            case '2':
                sub_menu(2)

            case '3':
                sub_menu(3)

            case '4':
                sub_menu(4)

            case '5':
                sub_menu(5)

            case '66':
                admin_page()

            case _:
                main(nspace)


# End main() function #

""" Global """

# // Command line1 //
parser = argparse.ArgumentParser(description=f"{__program__} Capstone Project")
parser.add_argument(
    "-l", "--licence", help=f"{__program__} licence information",
    required=False, action='store_true'
)
parser.add_argument(
    "-v", "--version", help=f"{__program__} version information",
    action='version', version=__version__
)

# // Call main function (Pick minimum version if necessary) //
if __name__ == "__main__":
    if sys.version_info.major == 3 and sys.version_info.minor >= 0:
        main(parser.parse_args())
    else:
        print('A python version greater that 3.0 is required.')
else:
    sys.exit(1)
