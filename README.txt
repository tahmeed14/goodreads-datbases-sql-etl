SI 330: Data Manipulation - HW5 Documentation
Name: Tahmeed Tureen
Fall 2017 - Dr. Chris Teplovs

# NOTE: ALL CSV FILES MUST BE IN THE SAME DIRECTORY AS .py FILE
# "Code lines" refer to the lines of code in the .py file in this folder

This documentation has information on how certain questions were addressed for homework 5 of SI 330: F17

Question 1: What are the top 10 most highly-rated authors?

To answer this question, I decided to define "highly-rated authors" as authors who have the highest average
ratings overall for all of their books.

For example, if Suzanne Collins has 3 books with average ratings of 3, 4, and 4.5 then her average rating 
of her books' average ratings would be (3 + 4 + 4.5) / 3 ~= 3.833.

After appropriate database manipulation is done, my .py code file will calculate the average rating for each
unique author and then sort it by highest ratings.

Code lines: 90-145

The top ten highly rated authors based on this definition are:
1. Lane T. Dennis
2. Bill Watterson
3. Ronald A. Beers
4. Kelly Jones
5. Steve Oliff
6. Lee Loughridge
7. Daniel Vozzo
8. James E. Talmage
9. Hafez
10. Angie Thomas


Question 2: What are the top 10 most popular authors on people's "To Read" lists?

To answer this question, I decided to define popularity of an author as the number
of times all of their books were added to the To Read list. So, for example if
J.K. Rowling has 3 books and they show up in the To Read list 12, 17, and 5 times 
respectively then her "popularity value" would be 34 ( the math is 12 + 17 + 5 ).

After appropriate database manipulation is done, my .py file will sum of the
"popularity value" for each author and then sort it in descending order.

Code lines: 147-192

The top ten most popular authors from the To Read list based on this definition are:
1. Stephen King
2. Neil Gaiman
3. J.K. Rowling
4. Cassandra Clare
5. George R.R. Martin
6. Rick Riordan
7. Jane Austen
8. John Green
9. Brandon Sanderson
10. James Patterson


[BONUS] Question 3:
Bonus Question: What are the top 5 Suzanne Collin's books or book sets ranked 
amongst eachother? Suzanne Collins is famous for her Hunger Games books 
and I am interested in seeing how her books rank in this data set. 
We will do the same for J.K. Rowling who is the author of the Harry Potter series
We will do the same for J.R.R. Tolkien who is the author of the Lord of the Rings Series

To answer this question we take advantage of SQL and petl to create a table that
we can print to an output using python. The results can be found when the .py file
is run or can be found here:

Code Lines: 195 - 230

Suzanne Collin's Top 5
1. The Hunger Games Trilogy Boxset (#1-3)
2. The Hunger Games (The Hunger Games, #1)
3. Catching Fire (The Hunger Games, #2)
4. Gregor and the Code of Claw (Underland Chronicles, #5)
5. Gregor and the Marks of Secret (Underland Chronicles, #4)

J.K. Rowling's Top 5
1. Harry Potter Boxed Set, Books 1-5 (Harry Potter, #1-5)
2. Harry Potter Boxset (Harry Potter, #1-7)
3. Harry Potter Collection (Harry Potter, #1-6)
4. The Harry Potter Collection 1-4 (Harry Potter, #1-4)
5. Harry and the Deathly Hallows (Harry Potter, #7)

J.R.R. Tolkien's Top 5
1. J.R.R. Tolkien 4-Book Boxed Set: The Hobbit and The Lord of the Rings
2. The Return of the King (The Lord of the Rings, #3)
3. The Hobbit: Graphic Novel
4. The Lord of the Rings (The Lord of the Rings, #1-3)
5. The Two Towers (The Lord of the Rings, #2)

