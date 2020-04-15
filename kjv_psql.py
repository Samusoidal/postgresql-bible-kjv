# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -----
# Import CSV and Import into PostgreSQL
# Anthony Crawford
# March 2018
# Dependencies: hashlib (removed April 2020) python-pip python-psycopg2 posgresql
# -----
# Updated for Python 3 and usability
# Jake McDermitt
# April 2020
# ----

import os
import errno

# Third Party Packages
import psycopg2

# Server settings
SERVER_ADDRESS = "127.0.0.1"
DB_USERNAME = "postgres"
DB_PASSWORD = "password"

try:
	print("Connecting ...")
	conn = psycopg2.connect(host=SERVER_ADDRESS, user=DB_USERNAME, password=DB_PASSWORD)
	cur = conn.cursor()
	print("PostgreSQL version:")
	cur.execute('SELECT version()')
	db_version = cur.fetchone()
	print(db_version)
	cur.close()
	print("Connection is good!")
except (Exception, psycopg2.DatabaseError) as error:
	print("Failed to connect!")
	print(error)
	quit()
finally:
	if conn is not None:
		conn.close()

# Import CSV
import csv
import sys

files = [
	'kjv-genesis.csv',
	'kjv-exodus.csv',
	'kjv-leviticus.csv',
	'kjv-numbers.csv',
	'kjv-deuteronomy.csv',
	'kjv-joshua.csv',
	'kjv-judges.csv',
	'kjv-ruth.csv',
	'kjv-1samuel.csv',
	'kjv-2samuel.csv',
	'kjv-1kings.csv',
	'kjv-2kings.csv',
	'kjv-1chronicles.csv',
	'kjv-2chronicles.csv',
	'kjv-ezra.csv',
	'kjv-nehemia.csv',
	'kjv-esther.csv',
	'kjv-job.csv',
	'kjv-psalms.csv',
	'kjv-proverbs.csv',
	'kjv-ecclesiastes.csv',
	'kjv-songofsolomon.csv',
	'kjv-isaiah.csv',
	'kjv-jeremiah.csv',
	'kjv-lamentations.csv',
	'kjv-ezekiel.csv',
	'kjv-daniel.csv',
	'kjv-hosea.csv',
	'kjv-joel.csv',
	'kjv-amos.csv',
	'kjv-obadiah.csv',
	'kjv-jonah.csv',
	'kjv-micah.csv',
	'kjv-nahum.csv',
	'kjv-habakkuk.csv',
	'kjv-zephaniah.csv',
	'kjv-haggai.csv',
	'kjv-zechariah.csv',
	'kjv-malachi.csv',
	'kjv-matthew.csv',
	'kjv-mark.csv',
	'kjv-luke.csv',
	'kjv-john.csv',
	'kjv-acts.csv',
	'kjv-romans.csv',
	'kjv-1corinthians.csv',
	'kjv-2corinthians.csv',
	'kjv-galatians.csv',
	'kjv-ephesians.csv',
	'kjv-philippians.csv',
	'kjv-colossians.csv',
	'kjv-1thessalonians.csv',
	'kjv-2thessalonians.csv',
	'kjv-1timothy.csv',
	'kjv-2timothy.csv',
	'kjv-titus.csv',
	'kjv-philemon.csv',
	'kjv-hebrews.csv',
	'kjv-james.csv',
	'kjv-1peter.csv',
	'kjv-2peter.csv',
	'kjv-1john.csv',
	'kjv-2john.csv',
	'kjv-3john.csv',
	'kjv-jude.csv',
	'kjv-revelation.csv'
]

conn = psycopg2.connect(host=SERVER_ADDRESS, user=DB_USERNAME, password=DB_PASSWORD)

print("Creating database: \'bible\'")

sql = """CREATE DATABASE bible;"""
conn.autocommit = True
cur = conn.cursor()
try:
	cur.execute(sql)
except (Exception, psycopg2.errors.DuplicateDatabase) as error:
	print("Database already exists, continuing")

sql = """SELECT count(*) FROM pg_catalog.pg_database WHERE datname = 'bible' ;"""
cur.execute(sql)
if bool(cur.rowcount) == True:
	print("Database created successfully.")
	print
else:
	print("Database creation failed.")
	quit()

cur.close()
conn.close()

conn = psycopg2.connect(host=SERVER_ADDRESS, database="bible", user=DB_USERNAME, password=DB_PASSWORD)
cur = conn.cursor()

print("Creating table \'kjv\'...")
print

sql = """CREATE TABLE kjv (
	id INTEGER PRIMARY KEY NOT NULL,
	testament text NOT NULL,
	book text NOT NULL,
	chapter text NOT NULL,
	verse text NOT NULL,
	vtext text NOT NULL);"""
cur.execute(sql)
conn.commit()

print("Importing CSV files into PostgreSQL database...")

count = 1
for file in files:
	print(file)
	f = open('csv/'+file, 'rt')
	try:
		reader = csv.reader(f)
		for row in reader:
			bible_testament = row[0]
			bible_book = row[1]
			bible_chapter = row[2]
			bible_verse = row[3]
			bible_text = row[5]
			sql = """INSERT INTO kjv VALUES(%s, %s, %s, %s, %s, %s);"""
			cur.execute(sql, (count, bible_testament, bible_book, bible_chapter, bible_verse, bible_text))
			count+=1

	except (Exception, psycopg2.DatabaseError) as error:
		print("Insert failed! Erase database and start over!")
		print(error)
		cur.close()
		conn.close()
		quit()

conn.commit()
cur.close()
conn.close()

print
print("Import Completed!")
print

sys.exit()
