
import mysql.connector
from mysql.connector import Error


class Database():
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="banks_portal",
                 user='root',
                 password='Tania@22n'):

        self.host       = host
        self.port       = port
        self.database   = database
        self.user       = user
        self.password   = password
        self.connection = None
        self.cursor     = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host         = self.host,
                port         = self.port,
                database     = self.database,
                user         = self.user,
                password     = self.password)
            
            if self.connection.is_connected():
                return
        except Error as e:
            print("Error while connecting to MySQL", e)


    def getAllAccounts(self):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor();
            query = "select * from accounts"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def getAllTransactions(self):
        ''' Complete the method to execute
                query to get all transactions'''
        if self.connection.is_connected():
            self.cursor= self.connection.cursor();
            query = "select * from Transactions"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

       
    def deposit(self, accountID, amount):
        ''' Complete the method that calls store procedure
                    and return the results'''
        
        call_procedure = ("CALL deposit(%s,%s,@success)")

        call_info = (accountID, amount)

        cursor = self.connection.cursor()

        cursor.execute(call_procedure, call_info)

        self.connection.commit()
        cursor.close()
        self.connection.close()
   

    def withdraw(self, accountID, amount):
        ''' Complete the method that calls store procedure
                    and return the results'''
        
        call_procedure = ("CALL withdraw(%s,%s,@success)")

        call_info = (accountID, amount)

        cursor = self.connection.cursor()

        cursor.execute(call_procedure, call_info)

        self.connection.commit()
        cursor.close()
        self.connection.close()

        
    def addAccount(self, ownerName, owner_ssn, balance, status):
        ''' Complete the method to insert an
                    account to the accounts table'''
        
        add_account = ("INSERT INTO accounts "
                       "(ownerName,owner_ssn,balance,account_status) "
                       "VALUES (%s,%s,%s,%s)")
        
        account_info = (ownerName, owner_ssn, balance, status)

        cursor = self.connection.cursor()

        cursor.execute(add_account, account_info)

        self.connection.commit()
        cursor.close()
        self.connection.close()
  
    def accountTransactions(self, accountID):
        ''' Complete the method to call
                    procedure accountTransaction return results'''
        
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            query = f"select * from Transactions where accountID = {accountID}"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
  
    def deleteAccount(self, AccountID):
        ''' Complete the method to delete account
                and all transactions related to account'''
        
        del_account = ("CALL deleteAccount(%s,@success)")

        del_info = (AccountID,)

        cursor = self.connection.cursor()

        cursor.execute(del_account,del_info)

        self.connection.commit()
        cursor.close()
        self.connection.close()
