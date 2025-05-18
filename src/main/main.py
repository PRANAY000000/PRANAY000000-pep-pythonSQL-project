import csv
import sqlite3

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users('../../resources/users.csv')
    load_and_clean_call_logs('../../resources/callLogs.csv')
    write_user_analytics('../../resources/userAnalytics.csv')
    write_ordered_calls('../../resources/orderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data

def load_and_clean_users(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  
        for row in reader:
            if len(row) != 2 or '' in [field.strip() for field in row]:
                continue  
            firstName, lastName = [field.strip() for field in row]
            cursor.execute('INSERT INTO users (firstName, lastName) VALUES (?, ?)', (firstName, lastName))
    conn.commit()



# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data

def load_and_clean_call_logs(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            if len(row) == 5 and all(row):
                try:
                    phoneNumber, startTime, endTime, direction, userId = row
                    cursor.execute('''
                        INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (phoneNumber, int(startTime), int(endTime), direction, int(userId)))
                except ValueError:
                    continue  


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.

def write_user_analytics(csv_file_path):
    cursor.execute('''
        SELECT userId, 
               ROUND(AVG(endTime - startTime), 1) AS avgDuration, 
               COUNT(*) AS numCalls 
        FROM callLogs 
        GROUP BY userId
    ''')

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['userId', 'avgDuration', 'numCalls'])
        for row in cursor.fetchall():
            writer.writerow(row)


# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv

def write_ordered_calls(csv_file_path):
    cursor.execute('''
        SELECT * FROM callLogs 
        ORDER BY userId ASC, startTime ASC
    ''')

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['callId', 'phoneNumber', 'startTime', 'endTime', 'direction', 'userId'])
        for row in cursor.fetchall():
            writer.writerow(row)


# Debug function (optional)
def select_from_users_and_call_logs():
    print("\nPRINTING DATA FROM USERS\n-------------------------")
    cursor.execute('SELECT * FROM users')
    for row in cursor:
        print(row)

    print("\nPRINTING DATA FROM CALLLOGS\n-------------------------")
    cursor.execute('SELECT * FROM callLogs')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()