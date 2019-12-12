import psycopg2
import sys
import os
from urllib.parse import urlparse
import csv
import glob

path = '../src/data/train/'

check_connection = True
try:
    connection = psycopg2.connect(dbname="estay", user="postgres", password="postgres", host="0.0.0.0", port="5434")
    cursor = connection.cursor()
except Exception as e:
    print(e)
    check_connection = False

###STATUS: ACTIVE, PENDING

def migrate_hotels():
    if check_connection:
        try:
            id = 2
            for filename in glob.glob(path+'*'):
                # cursor.execute("DELETE FROM hotels")
                print(filename)
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip the header row.
                    for row in reader:
                        
                        cursor.execute(
                            "INSERT INTO users VALUES("+ str(id) +",'" + "user_" + str(id)  + "','$2b$10$VqDhvjroZy1GyfPStPewO.JjYxxCnrpJXvv49LqCvO8k/BYYbcERa','HOTEL_OWNER')"
                        )
                        
                        cursor.execute(
                            "INSERT INTO hotels VALUES ('"+row[0]+"','"+ str(id) +"','ACTIVE','"+row[1]+"','"+row[2].replace("'","")+"','"+row[3]+"','"+row[4]+"','"+row[5]+"','"+row[6]+"','"+row[7]+"')"
                        )
                        print('insert user' + str(id))
                        id+=1


            print("migrate hotels succesfully")
        except (Exception, psycopg2.Error) as error :
            print (error)

def main():
    migrate_hotels()
    if(connection):
        connection.commit()
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

if __name__ == '__main__':
    main()
