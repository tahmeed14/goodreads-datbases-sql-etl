###############################
# Name: Tahmeed Tureen
# si330 - Homework 5 - Databases, SQL & etl
# Dr. Teplovs - Fall 2017
# Worked w/ Lauren Sigurdson & Mariel Setton

import petl as etl
import sqlite3

# Needed for Windows encoding, otherwise will not print appropriate symbols
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

## STEP 1
## Read in the CSV files
ratings = etl.fromcsv('ratings.csv', encoding = 'utf-8')
to_read = etl.fromcsv('to_read.csv', encoding = 'utf-8')
tags = etl.fromcsv('tags.csv', encoding = 'utf-8')
books = etl.fromcsv('books.csv', encoding = 'utf-8')
book_tags = etl.fromcsv('book_tags.csv', encoding = 'utf-8')


## STEP 2
## Connect to Sqlite and Initialize a database
conn = sqlite3.connect('goodbooks.db')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS Tags')
# sql_stat1 = 'CREATE TABLE IF NOT EXISTS Tags ()'
# cur.execute(table_spec1)

# Dump Tags data to db
#cur.execute('DROP TABLE IF EXISTS tags')
createTags = """CREATE TABLE IF NOT EXISTS tags (Tag_ID int primary key not null, Tag_Name char(50) )"""
cur.execute(createTags)
# dump data from csv
tags.todb(conn, 'tags')

# Dump Book Tags data to db
#cur.execute('DROP TABLE IF EXISTS book_tags')
# You don't want to specify primary key according to Piazza post 75
createBookTags = """CREATE TABLE IF NOT EXISTS book_tags (GoodReads_Book_ID int, Tag_ID int, Count int)"""
cur.execute(createBookTags)
# dump data from csv
book_tags.todb(conn, 'book_tags')

# Dump Ratings data to db
#cur.execute('DROP TABLE IF EXISTS ratings')
# You don't want to specify primary key according to Piazza post 75
createRatings = """CREATE TABLE IF NOT EXISTS ratings (User_ID int, Book_ID int, Rating int)"""
cur.execute(createRatings)
# dump data from csv
ratings.todb(conn, 'ratings')

# Dump To_Read data to db
#cur.execute('DROP TABLE IF EXISTS to_read')
# You don't want to specify primary key according to Piazza post 75
createToRead = """CREATE TABLE IF NOT EXISTS to_read (User_ID int, Book_ID int)"""
cur.execute(createToRead)
to_read.todb(conn, 'to_read')

# Dump Books data to db
cur.execute('DROP TABLE IF EXISTS books')
# You don't want to specify primary key according to Piazza post 75
createBooks = """CREATE TABLE IF NOT EXISTS books (Book_ID int, Goodreads_Book_Id int, Best_Book_ID int, Work_ID int, Books_Count int, ISBN int, ISBN13 int, Authors text, Original_Publication_Year char, Original_Title char, Title text, Language_code char, Average_Rating real, Ratings_Count int, Work_Ratings_Count int, Work_Text_Reviews_Count int, Ratings_1 int, Ratings_2 int, Ratings_3 int, Ratings_4 int, Ratings_5 int, Image_Url char(50), Small_Image_Url char(50))"""
cur.execute(createBooks)
books.todb(conn, 'books')

conn.commit()

# We've now read in all of the CSV Data to the Database!

## ******
## SKIP // IGNORE, this code block was used earlier but then later dropped but kept as reference
## STEP 3 - * WILL BE USED FOR BONUS QUESTION 3
## Manipulate current data tables to help us create a easy to understand books table
#Grab only the relevant columns from the books data table
# books_relevant = etl.fromdb(conn, 'SELECT Book_ID, Authors, Title, Average_Rating FROM books')
# createBooks_Relevant = """CREATE TABLE IF NOT EXISTS books_relevant (Book_ID int, Authors text, Title text, Average_Rating real)"""
# cur.execute(createBooks_Relevant)
# books_relevant.todb(conn, 'books_relevant')
# Now we have a more simplistic table for a books table with only fields we are interested in using for our analysis
## ******


## STEP 4
## Creating a Authors Table that has individual authors instead of a book having several

#cur.execute('DROP TABLE IF EXISTS AuthorsTable')
createAuthors = """CREATE TABLE IF NOT EXISTS AuthorsTable ( Authors text, Book_ID int, Average_Rating real)"""
cur.execute(createAuthors)
#conn.commit()

authors = etl.fromdb(conn, 'SELECT DISTINCT Authors, Book_ID, Average_Rating FROM books GROUP BY Book_ID')

for field in authors:
	the_authors = field[0].split(',')
	for author in the_authors:
		author = author.strip()
		author = author.replace('\w+',' ')
		cur.execute('INSERT INTO AuthorsTable(Authors, Book_ID, Average_Rating) VALUES (?,?,?)', (author, field[1], field[2]))

conn.commit()

## STEP 5
## Use this new table to iterate through and count up the average "average ratings" for each author

# We need to use DISTINCT here because we may have duplicate rows in SQL, we want to avoid recounting!
list_authors = etl.fromdb(conn, 'SELECT DISTINCT Authors, Average_Rating, Book_ID FROM AuthorsTable')
# print(list_authors[0])

dict_authors = {} # initialize the dict

for tup in list_authors:
	if tup[0] == "Authors": # There is a row in the database that behaves abnormaly
		continue

	if tup[0] not in dict_authors:
		dict_authors[tup[0]] = (tup[1], 1)
	else:
		total_sum = dict_authors[tup[0]][0] + tup[1] # accumulate the sum
		num = dict_authors[tup[0]][1] + 1 # accumulate the divisor

		dict_authors[tup[0]] = (total_sum, num) # key is author name and value is tuple with total avg_ratings and num is number of avg ratings

#print(dict_authors)

dict_authors_ratings = {}
#print(dict_authors_ratings)

for author_name in dict_authors:
	rating_author = dict_authors[author_name][0] / dict_authors[author_name][1]
	dict_authors_ratings[author_name] = round(rating_author,3) # Round the ratings to 3 decimals

# Now create a sorted list for whoever has the highest ratings
# print(dict_authors_ratings[])

top_ten_authors = sorted(dict_authors_ratings, key = lambda x: dict_authors_ratings[x], reverse = True)
top_ten_authors = top_ten_authors[0:10]

print("*************************************************    QUESTION # 1    ************************************************************")
print("TOP TEN MOST HIGHLY RATED AUTHORS BASED ON THEIR AVERAGE RATING OF THE AVERAGE RATINGS OF ALL OF THEIR BOOKS ")
print(top_ten_authors)
print('\n\n\n\n\n\n\n')

## STEP 6
## ANSWERING QUESTION #2

## Create New Table that has a better To_Read_Count database that can be used for the analysis
createToRead_Count = """CREATE TABLE IF NOT EXISTS to_read_count (Book_ID int, Count_Books int)"""
cur.execute(createToRead_Count)
#Grab only the relevant columns
to_read_count = etl.fromdb(conn, 'SELECT Book_ID, COUNT(Book_ID) FROM to_read GROUP BY Book_ID')

for tup in to_read_count:
	cur.execute('INSERT INTO to_read_count(Book_ID, Count_Books) VALUES (?,?)', (tup[0], tup[1]))

conn.commit()


# Need to use DISTINCT so we don't recount
joined_auth_read = etl.fromdb(conn, "SELECT DISTINCT AuthorsTable.Authors, AuthorsTable.Book_ID, to_read_count.Count_Books FROM AuthorsTable LEFT JOIN to_read_count ON (AuthorsTable.Book_ID = to_read_count.Book_ID)")
#print(joined_auth_read)

top_ten_toread_authors = {}

for tup in joined_auth_read:
	if tup[0] == "Authors":
		continue

	if tup[0] not in top_ten_toread_authors:
		try:
			top_ten_toread_authors[tup[0]] = int(tup[2]) # First value will be the number of times the book was added to the to read list for a specific book
		except:
			pass
	else:
		try:
			top_ten_toread_authors[tup[0]] += int(tup[2])
		except:
			pass

# Top Ten Most Popular Authors
top_ten_authors_toread_list = sorted(top_ten_toread_authors, key = lambda x : top_ten_toread_authors[x], reverse = True)
top_ten_authors_toread_list = top_ten_authors_toread_list[0:10]



print("*************************************************    QUESTION # 2    ************************************************************")
print("TOP TEN MOST HIGHLY POPULAR AUTHORS BASED ON THE NUMBER OF TIMES ALL OF THEIR BOOKS WERE ADDED TO THE TO_READ LIST")
print(top_ten_authors_toread_list)
print('\n\n\n\n\n\n\n')


## STEP 7
## Bonus Question: What are the top 5 Suzanne Collin's books or book sets ranked amongst eachother? Suzanne Collins is famous for her Hunger Games books 
## and I am interested in seeing how her books rank in this data set. 
## We will do the same for J.K. Rowling who is the author of the Harry Potter series
## We will do the same for J.R.R. Tolkien who is the author of the Lord of the Rings Series

## STEP 4
## Creating a Authors Table that has individual authors instead of a book having several

#cur.execute('DROP TABLE IF EXISTS AuthorsTable')
createAuthors_jk = """CREATE TABLE IF NOT EXISTS AuthorsTable_Titles ( Authors text, Book_ID int, Average_Rating real, Title text)"""
cur.execute(createAuthors_jk)
#conn.commit()

authors_jk = etl.fromdb(conn, 'SELECT DISTINCT Authors, Book_ID, Average_Rating, Title FROM books GROUP BY Book_ID')

for field in authors_jk:
	the_authors = field[0].split(',')
	for author in the_authors:
		author = author.strip()
		author = author.replace('\w+',' ')
		cur.execute('INSERT INTO AuthorsTable_Titles(Authors, Book_ID, Average_Rating, Title) VALUES (?,?,?,?)', (author, field[1], field[2], field[3]))

conn.commit()


print("*************************************************    QUESTION # 3    ************************************************************")
print("TOP FIVE RATED BOOKS/BOOKSETS FOR FAMOUS AUTHORS, Suzanne Collins, J.K. Rowling, and J.R.R. Tolkien")

suzanne_collins_books = etl.fromdb(conn, "SELECT DISTINCT Title, Average_Rating FROM AuthorsTable_Titles WHERE Authors LIKE 'Suzanne Collins' ORDER BY Average_Rating DESC")
print(suzanne_collins_books.head(5))

jk_rowling_books = etl.fromdb(conn, "SELECT DISTINCT Title, Average_Rating FROM AuthorsTable_Titles WHERE Authors LIKE 'J.K. Rowling' ORDER BY Average_Rating DESC")
print(jk_rowling_books.head(5))

jrr_tolkien_books = etl.fromdb(conn, "SELECT DISTINCT Title, Average_Rating FROM AuthorsTable_Titles WHERE Authors LIKE 'J.R.R. Tolkien' ORDER BY Average_Rating DESC")
print(jrr_tolkien_books.head(5))

# Close connection to Sqlite
conn.close()