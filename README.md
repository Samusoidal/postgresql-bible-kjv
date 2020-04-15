The Holy Bible (King James Version) for PostgreSQL

This project is 100% free to use.

NOTE: Knowledge of how to setup and use PostgreSQL and Python is recommended. 

The repo comes with the following files:

Python script (kjv-psql.py), CSV files for each book of the Bible (created from XLSX files, exported as "CSV Comma Delimited")

The script will create a database called 'bible', create one table called 'kjv', then populate all 31102 verse in the KJV Bible.

This version is ONLY compatible with Python 3. You will need to psycopg2 package which you can install via `pip install psycopg2`.

To import the CSV files into your PostgreSQL instance run this command:

python kjv-psql.py

After import there should be 31102 verses stored. One Bible verse equals one record. 
