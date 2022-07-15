# Table 1 -- Trust Score
# Table 2 -- Appointment

import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host='localhost',
    user="root",
    passwd="IMBossno1",
    database="testdb"
)
mycursor = db.cursor()

'''CREATING DATABASE'''
# mycursor.execute("CREATE DATABASE testdb")

'''CREATING TABLES'''
# Q1 = "CREATE TABLE Customers(id int PRIMARY KEY NOT NULL AUTO_INCREMENT, pno int NOT NULL, trust_score int DEFAULT 100)"
# Q2 = "CREATE TABLE Appointments(ap_id int PRIMARY KEY NOT NULL AUTO_INCREMENT, cus_id int NOT NULL, req_rec_time datetime, appointment_time datetime, reach_time datetime, FOREIGN KEY(cus_id) REFERENCES Customers(id))"
# mycursor.execute(Q1)
# mycursor.execute(Q2)
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#     print(x)

'''ALTER TABLES'''
# Q3 = "ALTER TABLE Customers MODIFY pno VARCHAR(10)"
# mycursor.execute(Q3)

'''PRINT TABLE'''
# mycursor.execute("SELECT * FROM Customers")
# for x in mycursor:
#     print(x)


def insert_user(pno):
    Q = "INSERT INTO Customers (pno) VALUES (%s)"
    mycursor.execute(Q, (pno,))
    user_id = mycursor.lastrowid
    db.commit()
    return user_id


def check_and_insert_user(pno):
    Q = "SELECT * from Customers WHERE pno=%s"
    mycursor.execute(Q, (pno,))
    row = mycursor.fetchone()
    if row is None:
        user_id = insert_user(pno)
    else:
        user_id = row[0]
    return user_id


def check_appointment(pno):
    Q = "SELECT * FROM Appointments WHERE cus_id IN (SELECT id FROM Customers WHERE pno = %s)"
    mycursor.execute(Q, (pno,))
    row = mycursor.fetchone()
    return row


def take_appointment(pno):
    prev_appointment = check_appointment(pno)
    if prev_appointment is not None:
        return "Already have appointment booked at {}".format(prev_appointment[2])
    else:
        Q1 = "SELECT id from Customers WHERE pno=%s"
        Q2 = "INSERT INTO Appointments (cus_id, req_rec_time) VALUES (%s, %s)"

        now = datetime.now()
        req_rec_time = now.strftime('%Y-%m-%d %H:%M:%S')
        mycursor.execute(Q1, (pno,))
        user_id = mycursor.fetchone()
        mycursor.execute(Q2, (user_id[0], req_rec_time))
        db.commit()
        return "Appointment booked at {}".format(req_rec_time)
