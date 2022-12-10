import psycopg2
from psycopg2 import Error

def DataUpdate(Location, Places_Category, Radius, Location_weather):
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="root",
        port="5432",
        database="Rasa_Chatbot"
    )

    cursor = mydb.cursor()

    #sql = "CREATE TABLE customers (Location VARCHAR(255), Places_Category VARCHAR(255), Radius VARCHAR(255), Location_weather VARCHAR(255))"

    #cursor.execute(sql)

    sql = """ INSERT INTO customers (Location,Places_Category,Radius,Location_weather) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (Location, Places_Category, Radius, Location_weather)
    cursor.execute(sql, record_to_insert)

    mydb.commit()

    print(cursor.rowcount, "record inserted")

    cursor.close()
    mydb.close()