import sqlite3
from pathlib import Path


class DBmanage:
    CWD = Path.cwd()
    DATA = Path(CWD) / 'Data'
    DATA.mkdir(parents=True, exist_ok=True)
    
    DB_NAME = 'data.db'
    DB_PATH = Path(DATA) / DB_NAME
    
    # Connecting to sqlite
    CONN = sqlite3.connect(DB_PATH)
    
    # Set Forign Key Enabled
    CONN.execute("PRAGMA foreign_keys = 1")
    
    # Creating a cursor object using the cursor() method
    CURSOR = CONN.cursor()
    
    def __init__(self):
        # Initialise Variables
        
        # Create Company Table if Not Exist
        self.create_company_table()
    
    # # Create Table
    # Create Company List Table
    def create_company_table(self):
        # Create Companies List
        query = '''CREATE TABLE IF NOT EXISTS company_list(
                                    company_list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    company_list_name TEXT,
                                    company_list_address TEXT,
                                    company_list_state TEXT,
                                    company_list_pin TEXT,
                                    company_list_gstn TEXT,
                                    company_list_phone TEXT,
                                    company_list_email TEXT)'''
        self.CURSOR.execute(query)
        
        # Commit your changes in the database
        self.CONN.commit()
    
    # Create Ledger Table
    def create_ledger_table(self, company_list):
        company_name = '_'.join(company_list[1].split(' '))
        # Create Ledger Table
        query = f'''CREATE TABLE IF NOT EXISTS ledger_{company_name}(
                                            ledger_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            ledger_name TEXT NOT NULL,
                                            ledger_opening REAL NOT NULL)'''
        self.CURSOR.execute(query)
        
        # Commit your changes in the database
        self.CONN.commit()

    # Create Party Table If Not Exist
    def create_party_table(self, company_list):
        # Company Name Space converted to (_)
        company_name = '_'.join(company_list[1].split(' '))
        
        # Create Party Table
        query = f'''CREATE TABLE IF NOT EXISTS party_{company_name}(
                                party_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                party_name TEXT NOT NULL,
                                party_address TEXT NOT NULL,
                                party_state TEXT NOT NULL,
                                party_type TEXT NOT NULL,
                                party_pin TEXT,
                                party_gstn TEXT,
                                party_phone TEXT,
                                party_email TEXT,
                                party_opening REAL NOT NULL)'''
        self.CURSOR.execute(query)
    
        # Commit your changes in the database
        self.CONN.commit()

    # Create Purchase Sale Bill table If Not Exist
    def create_bill_table(self, company_list):
        # Company Name Space converted to (_)
        company_name = '_'.join(company_list[1].split(' '))

        # Create Purchase Sale Bill table
        query = f'''CREATE TABLE IF NOT EXISTS bill_{company_name}(
                                        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        bill_date TEXT NOT NULL,
                                        party_id INTEGER NOT NULL,
                                        bill_amount REAL NOT NULL,
                                        bill_type TEXT NOT NULL,
                                        bill_notes TEXT,
                                        FOREIGN KEY (party_id)
                                        REFERENCES party_{company_name} (party_id)
                                        ON UPDATE CASCADE
                                        ON DELETE RESTRICT
                                    );'''
        self.CURSOR.execute(query)

        # Commit your changes in the database
        self.CONN.commit()
    
    # Create Payment Receipt Voucher table if Not Exist
    def create_voucher_table(self, company_list):
        # Company Name Space converted to (_)
        company_name = '_'.join(company_list[1].split(' '))

        # Create Payment Receipt Voucher table
        query = f'''CREATE TABLE IF NOT EXISTS voucher_{company_name}(
                                        voucher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        voucher_date TEXT NOT NULL,
                                        party_id INTEGER NOT NULL,
                                        ledger_id INTEGER NOT NULL,
                                        voucher_amount REAL NOT NULL,
                                        voucher_type TEXT NOT NULL,
                                        voucher_notes TEXT,
                                        FOREIGN KEY (party_id)
                                        REFERENCES party_{company_name} (party_id)
                                        FOREIGN KEY (ledger_id)
                                        REFERENCES ledger_{company_name} (ledger_id)
                                        ON UPDATE CASCADE
                                        ON DELETE RESTRICT
                                    );'''
        self.CURSOR.execute(query)
    
        # Commit your changes in the database
        self.CONN.commit()
    
    # # Insert Edit DB Data
    # Insert Edit Company
    def insert_edit_company(self, company_list):
        # Get all Companies list from DB
        all_company_list = self.fetch_company_list()
        
        # If Last Element (Company ID) is 0 To Insert Data else Update
        if company_list[-1] == 0:
            
            # Check Company Already Exist
            for company_in_db in all_company_list:
                if company_list[0] == company_in_db[1]:
                    return False, f"Company '{company_list[0]}' Already Exist"
            
            # Query To Insert The Details of New Company
            query = f'''INSERT INTO company_list(
                                company_list_name,
                                company_list_address,
                                company_list_state,
                                company_list_pin,
                                company_list_gstn,
                                company_list_phone,
                                company_list_email)
                                VALUES(?,?,?,?,?,?,?)'''
            try:
                self.CURSOR.execute(query, company_list[:-1])
                self.CONN.commit()
                return True, f"Company '{company_list[0]}' Inserted Successfully"
            except Exception as e:
                print(e)
                return False, f"Company Not Created\n\nDB Error"  # SQL Error
            
        # Company on Edit Mode (Update)
        else:
            # Query To Update Company Details
            query = f'''UPDATE company_list SET
                                    company_list_name=?,
                                    company_list_address=?,
                                    company_list_state=?,
                                    company_list_pin=?,
                                    company_list_gstn=?,
                                    company_list_phone=?,
                                    company_list_email=?
                                    WHERE company_list_id=?'''
            try:
                self.CURSOR.execute(query, company_list)
                self.CONN.commit()
                return True, f"Company '{company_list[0]}' Updated Successfully"
            except Exception as e:
                print(e)
                return False, "Company Not Updated\n\nDB Error"  # SQL Error
    
    # Insert Edit Ledger
    def insert_edit_ledger(self, data, company_list):
        # Company Name Space converted to (_)
        company_name = '_'.join(company_list[1].split(' '))
        
        # Create Ledger Table If Not Exist
        self.create_ledger_table(company_list)
        
        # Get Available Ledger from DB
        all_ledgers = self.fetch_ledger_list(company_name)
        
        # If last Element is 0 Then Insert else Update
        if data[-1] == 0:
            
            # Check Ledger Name Already exist
            for account in all_ledgers:
                if data[0] == account[1]:
                    return False, f'Type of Account "{data[0]}" Already in Data Base'
            
            # Query to Insert Ledger
            query = f'''INSERT INTO ledger_{company_name}(
                                        ledger_name,
                                        ledger_opening)
                                        VALUES(?,?)'''
            try:
                self.CURSOR.execute(query, data[:-1])
                self.CONN.commit()
                return True, f"Ledger '{data[0]}' Inserted Successfully"
            except Exception as e:
                print(e)
                return False, f"Ledger Not Inserted\n\nDB Error"  # SQL Error
            
        # Update Type of Account
        else:
            query = f'''UPDATE ledger_{company_name} SET
                                        ledger_name=?,
                                        ledger_opening=?
                                        WHERE ledger_id=?'''
            try:
                self.CURSOR.execute(query, data)
                self.CONN.commit()
                return True, f"Ledger '{data[0]}' Updated Successfully"
            except Exception as e:
                print(e)
                return False, "Ledger Not Updated\n\nDB Error"  # SQL Error
            
    # Insert Edit Party
    def insert_edit_party(self, data, company_list):
        # Company Name Space converted to (_)
        company_name = '_'.join(company_list[1].split(' '))
    
        # Create Party Table If Not Exist
        self.create_party_table(company_list)
    
        # Get All Parties from DB
        all_parties = self.fetch_party_list(company_name)
    
        # If last Element is 0 Then Insert else Update
        if data[-1] == 0:
        
            # Check Data Already exist
            for party in all_parties:
                if data[0] == party[1]:
                    return False, f'Party "{data[0]}" Already in Data Base'
        
            # Query to Insert Type of Account
            query = f'''INSERT INTO party_{company_name}(
                                party_name,
                                party_address,
                                party_state,
                                party_type,
                                party_pin,
                                party_gstn,
                                party_phone,
                                party_email,
                                party_opening)
                                VALUES(?,?,?,?,?,?,?,?,?)'''
            try:
                self.CURSOR.execute(query, data[:-1])
                self.CONN.commit()
                return True, f"Party '{data[0]}' Added Successfully"
            except Exception as e:
                print(e)
                return False, f"Party Not Created\n\nDB Error"  # SQL Error
            
        # Update Party
        else:
            query = f'''UPDATE party_{company_name} SET
                                            party_name=?,
                                            party_address=?,
                                            party_state=?,
                                            party_type=?,
                                            party_pin=?,
                                            party_gstn=?,
                                            party_phone=?,
                                            party_email=?,
                                            party_opening=?
                                            WHERE party_id=?'''
            try:
                self.CURSOR.execute(query, data)
                self.CONN.commit()
                return True, f"Party '{data[0]}' Updated Successfully"
            except Exception as e:
                print(e)
                return False, "Party Not Updated\n\nDB Error"  # SQL Error
    
    # Insert Edit Bill
    def insert_edit_bill(self, data, company_list):
        print(data)
        # Company Name Space converted to (_)
        company_name = '_'.join(company_list[1].split(' '))
    
        # Create Bill Table If Not Exist
        self.create_bill_table(company_list)
    
        # If last Element is 0 Then Insert else Update
        if data[-1] == 0:
        
            # Query to Insert Type of Account
            query = f'''INSERT INTO bill_{company_name}(
                                        bill_date,
                                        party_id,
                                        bill_amount,
                                        bill_type,
                                        bill_notes)
                                        VALUES(?,?,?,?,?)'''
            try:
                self.CURSOR.execute(query, data[:-1])
                self.CONN.commit()
                return True, f"Bill Added Successfully"
            except Exception as e:
                print(e)
                return False, f"Bill Not Added\n\nDB Error"  # SQL Error
            
        # Update Bill
        else:
            query = f'''UPDATE bill_{company_name} SET
                                            bill_date=?,
                                            party_id=?,
                                            bill_amount=?,
                                            bill_type=?,
                                            bill_notes=?
                                            WHERE bill_id=?'''
            try:
                self.CURSOR.execute(query, data)
                self.CONN.commit()
                return True, f"Bill Updated Successfully"
            except Exception as e:
                print(e)
                return False, "Bill Not Updated\n\nDB Error"  # SQL Error

    # Insert Edit Voucher
    def insert_edit_voucher(self, data, company_list):
        # Company Name Space converted to (_)
        company_name = '_'.join(company_list[1].split(' '))

        # Create Voucher Table If Not Exist
        self.create_voucher_table(company_list)

        # If last Element is 0 Then Insert else Update
        if data[-1] == 0:
    
            # Query to Insert Voucher
            query = f'''INSERT INTO voucher_{company_name}(
                                                voucher_date,
                                                party_id,
                                                ledger_id,
                                                voucher_amount,
                                                voucher_type,
                                                voucher_notes)
                                                VALUES(?,?,?,?,?,?)'''
            try:
                self.CURSOR.execute(query, data[:-1])
                self.CONN.commit()
                return True, f"Voucher Added Successfully"
            except Exception as e:
                print(e)
                return False, f"Voucher Not Added\n\nDB Error"  # SQL Error
            
        # Update Type of Account
        else:
            query = f'''UPDATE voucher_{company_name} SET
                                            voucher_date=?,
                                            party_id=?,
                                            ledger_id=?,
                                            voucher_amount=?,
                                            voucher_type=?,
                                            voucher_notes=?
                                            WHERE voucher_id=?'''
            try:
                self.CURSOR.execute(query, data)
                self.CONN.commit()
                return True, f"Voucher Updated Successfully"
            except Exception as e:
                print(e)
                return False, "Voucher Not Updated\n\nDB Error"  # SQL Error
    
    # # Fetch Data from DB
    # Get All Company List
    def fetch_company_list(self):
        query = "SELECT * FROM company_list"
        self.CURSOR.execute(query)
        
        return self.CURSOR.fetchall()
    
    # Get All Ledgers
    def fetch_ledger_list(self, company):
        query = f"SELECT * FROM ledger_{company}"
        self.CURSOR.execute(query)
        
        return self.CURSOR.fetchall()
    
    # Fetch Table List
    def fetch_all_tables(self):
        query = "SELECT name FROM sqlite_master"
        self.CURSOR.execute(query)
        
        return self.CURSOR.fetchall()
    
    # Get All Party List
    def fetch_party_list(self, company):
        query = f"SELECT * FROM party_{company}"
        self.CURSOR.execute(query)
        
        return self.CURSOR.fetchall()
    
    # Get All Bill List
    def fetch_bill_list(self, company):
        query = f"SELECT * FROM bill_{company}"
        self.CURSOR.execute(query)
    
        return self.CURSOR.fetchall()

    # Get All Voucher List
    def fetch_voucher_list(self, company):
        query = f"SELECT * FROM voucher_{company}"
        self.CURSOR.execute(query)

        return self.CURSOR.fetchall()
    
    # # Delete Data From DB
    # Delete Company
    def delete_company(self, company_to_del):
        # Get All Company Detailed List (List of List)
        all_companies = self.fetch_company_list()
        valid_company = False  # Set Validation Variable as False
        for company_db in all_companies:
            if company_db == company_to_del:
                valid_company = True  # If Company Name and ID Match set Validation Variable
        if valid_company:
            try:
                # Delete Company Details from Company List Table
                query = f"DELETE FROM company_list WHERE company_list_id=?"
                data = [company_to_del[0]]
                self.CURSOR.execute(query, data)
                self.CONN.commit()
                
                # Get all Table Names
                all_table_list = self.fetch_all_tables()
                
                # Search table Name Ends with Company name (Eg. bill_company)
                for table_name in all_table_list:
                    if table_name[0].endswith('_'.join(company_to_del[1].split(' '))):
                        query = f"DROP TABLE {table_name}"
                        self.CURSOR.execute(query)  # Drope All Tables related to the company
                        self.CONN.commit()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            print("Company Not Found in Index Table")  # If somehow Company Details Mismatch (Not Possible)
    
    # Ledger Delete
    def delete_ledget(self, company_name, ledger_id):
        try:
            # Delete Party Details from Party Table
            query = f"DELETE FROM ledger_{company_name} WHERE ledger_id=?"
            data = [ledger_id]
            self.CURSOR.execute(query, data)
            self.CONN.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    # Party Delete
    def delete_party(self, company_name, party_id):
        try:
            # Delete Party Details from Party Table
            query = f"DELETE FROM party_{company_name} WHERE party_id=?"
            data = [party_id]
            self.CURSOR.execute(query, data)
            self.CONN.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # Delete Voucher
    def delete_bill(self, company_name, bill_id):
        try:
            # Delete Bill Details from Bill Table
            query = f"DELETE FROM bill_{company_name} WHERE bill_id=?"
            data = [bill_id]
            self.CURSOR.execute(query, data)
            self.CONN.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    # Delete Voucher
    def delete_voucher(self, company_name, voucher_id):
        try:
            # Delete Voucher Details from Voucher Table
            query = f"DELETE FROM voucher_{company_name} WHERE voucher_id=?"
            data = [voucher_id]
            self.CURSOR.execute(query, data)
            self.CONN.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    # Close Data Base
    def close_db(self):
        self.CONN.commit()
        self.CONN.close()
