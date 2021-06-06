import os
import flask
import json
import mysql.connector


DB_NAME = 'p_customer'

class DBManager:
    
    def __init__(self, database=DB_NAME, host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host,
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()
        
    def populate_db(self):
        
        self.cursor.execute('CREATE TABLE IF NOT EXISTS As_company (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Name VARCHAR(255) NOT NULL)')
        
        self.cursor.execute('CREATE TABLE IF NOT EXISTS As_account (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Name VARCHAR(255) NOT NULL, Company_id INT, FOREIGN KEY (Company_id) REFERENCES As_company(id))')
        
        self.cursor.execute('CREATE TABLE IF NOT EXISTS As_project (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Name VARCHAR(255) NOT NULL, Account_id INT, Status INT,FOREIGN KEY (Account_id) REFERENCES As_account(id))')
        
        self.cursor.execute('INSERT INTO As_company (Name) VALUES ("test1"), ("test2"), ("test3");')
        self.cursor.execute('INSERT INTO As_account (Name,Company_id) VALUES ("test11",1), ("test12",2), ("test13",3);')
        self.cursor.execute('INSERT INTO As_project (Name,Account_id,Status) VALUES ("aaaa",1,1),("bbb",2,2),("ccc",3,0);')
        self.connection.commit()
        
    def query_data(self):
        self.cursor.execute('SELECT * FROM As_company , As_account, As_project')
        rec = []
        for c in self.cursor:
            rec.append(c)
        return rec


server = flask.Flask(__name__)
conn = None

@server.route('/')
def listdata():
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    rec = conn.query_data()

    result = []
    for c in rec:
        result.append(c)

    return flask.jsonify({"response": result})


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=5000)
