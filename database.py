import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", 
    password = "", 
)
mycursor = mydb.cursor()

#creating the database
mycursor.execute("CREATE DATABASE `games`")
mycursor.execute("use `games`")

#creating table
mycursor.execute("CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(225) NOT NULL , password VARCHAR(225) NOT NULL ) ")

# adding the column of fruit slicer
mycursor.execute("ALTER TABLE `user` ADD `fruit-score` INT NULL DEFAULT '0' ")

#adding the column of car racing
mycursor.execute("ALTER TABLE `user` ADD `car-score` INT NULL DEFAULT '0' ")

#adding the date column for user
mycursor.execute("ALTER TABLE `user` ADD `date` DATE DEFAULT CURDATE() ")

#adding the time column for user
mycursor.execute("ALTER TABLE `user` ADD `time` TIME DEFAULT CURTIME() ")

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)
