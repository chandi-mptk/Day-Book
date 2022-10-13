from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

from Validation import *
from DBManage import DBmanage


class Window:
    # Initialize main Window
    root = Tk()
    
    # Detect screen size
    W = root.winfo_screenwidth()
    H = root.winfo_screenheight()
    
    # Contents
    APP_NAME = "Day Book Software"
    STATE_LIST = ['01-Jammu & Kashmir',
                  '02-Himachal Pradesh',
                  '03-Punjab',
                  '04-Chandigarh',
                  '05-Uttarakhand',
                  '06-Haryana',
                  '07-Delhi',
                  '08-Rajasthan',
                  '09-Uttar Pradesh',
                  '10-Bihar',
                  '11-Sikkim',
                  '12-Arunachal Pradesh',
                  '13-Nagaland',
                  '14-Manipur',
                  '15-Mizoram',
                  '16-Tripura',
                  '17-Meghalaya',
                  '18-Assam',
                  '19-West Bengal',
                  '20-Jharkhand',
                  '21-Orissa',
                  '22-Chhattisgarh',
                  '23-Madhya Pradesh',
                  '24-Gujarat',
                  '25-Daman & Diu',
                  '26-Dadra & Nagar Haveli',
                  '27-Maharashtra',
                  '28-Andhra Pradesh (Old)',
                  '29-Karnataka',
                  '30-Goa',
                  '31-Lakshadweep',
                  '32-Kerala',
                  '33-Tamil Nadu',
                  '35-Andaman & Nicobar Islands',
                  '36-Telengana',
                  '37-Andhra Pradesh (New)']
    PARTY_TYPE_LIST = ['Creditor', 'Debtor', 'Other']
    BILL_TYPE_LIST = ['Sales', 'Purchase']
    VOUCHER_TYPE_LIST = ['Receipt', 'Payment']
    
    # Set window Size
    root.geometry(f"{W}x{H}+0+0")
    
    # Maximize window
    root.state('zoomed')
    
    # Creating Menubar
    menubar = Menu(root)
    
    def __init__(self):
        # # DB Related Variables
        # Create Instants
        self.db_Manage_inst = DBmanage()
        
        # Variables
        self.selected_company = []  # If A Company Selected
        self.selected_ledger = []  # If an Account Type Selected
        self.selected_party = []  # If A party is Selected
        self.selected_bill = []  # If Bill is Selected
        self.selected_voucher = []  # If voucher is Selected
        
        # Get All Company Data
        self.db_Manage_inst.create_company_table()
        all_company_data = self.db_Manage_inst.fetch_company_list()
        
        if all_company_data:  # Check Company Name Available
            self.open_company_widget_status = NORMAL
        else:
            self.open_company_widget_status = DISABLED
        
        # Title
        self.root.title(f"{self.APP_NAME}")
        
        # display Menu
        self.root.config(menu=self.menubar)
        # Adding File Menu and commands
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Create Company', command=self.create_company_widgets)
        self.file_menu.add_command(label='Open Company', command=self.open_company_widget,
                                   state=self.open_company_widget_status)
        self.file_menu.add_command(label='Close Company', command=self.close_company, state=DISABLED)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.destroy)
        
        # Initialise Widget
        self.company_address = None
        self.party_address = None
        
        # Frames on Root Window
        self.base_Frame = Frame(self.root, bg='light blue')
        self.base_Frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
    
    # # Navigation Methods
    # Tab To Next Field in Address(Text Widget)
    def next_widget_to_address(self, event):
        event.widget.tk_focusNext().focus()
        return ('break')
    
    # # Validate Data Area
    # Company Data Validate
    def company_validate(self):
        # Get Data from Widgets
        # Column names as List
        data_sequence = ['company_name', 'company_address', 'state', 'pin', 'gstn', 'mob', 'email']
        data_dict = {}  # Dict to store Data from Widgets
        valid_company = True  # Company Data Validation Status
        
        # Loop through Widgets to Get Data
        for index, widget in enumerate(self.base_Frame.winfo_children()):
            
            # Entry Widget Data Collection
            if widget.winfo_name().startswith('!entry'):
                data_dict[data_sequence[(index // 2)]] = widget.get()
                if data_dict[data_sequence[(index // 2)]]:
                    while data_dict[data_sequence[(index // 2)]][-1] == ' ':
                        data_dict[data_sequence[(index // 2)]] = data_dict[data_sequence[(index // 2)]][:-1]
            
            # Text Widget Data Collection
            if widget.winfo_name().startswith('!text'):
                data_dict[data_sequence[index // 2]] = widget.get('1.0', END)
            
            # Combo Box Widget Data Collection
            if widget.winfo_name().startswith('!combobox'):
                data_dict[data_sequence[index // 2]] = widget.get()
        data_dict['company_name'] = data_dict['company_name'].upper()  # Company Name In Upper Case
        data_dict['gstn'] = data_dict['gstn'].upper()  # Company GST Number In Upper Case
        
        # # Data Validation
        # Check Name for Special Char and Minimum Length 3
        if not name_check(data_dict['company_name']):
            valid_company = False
            messagebox.showerror('Invalid Company Name',
                                 'Allowed Letters, Numbers, (Space) with at least 3 letter Long')
        
        # Check Address for Special Char and Minimum Length 5
        if not address_check(data_dict['company_address']) and valid_company:
            valid_company = False
            messagebox.showerror('Invalid Company Address', 'Allowed Letters, Numbers, (.), (,), (-), (_), (Space), '
                                                            '(Enter) and 5 Letter long')
        
        # Check if GSTN available and State Matching and GSTN Checksum Correct
        if not gstn_validate(data_dict['state'], data_dict['gstn']) and valid_company:
            valid_company = False
            messagebox.showerror('Invalid GST Number', 'GST Number not Matching with State or GST Number maybe wrong')
        
        # Check PIN Code Valid
        if not pin_validation(data_dict['pin']) and valid_company:
            valid_company = False
            messagebox.showerror('Invalid PIN Code', 'PIN Code Not Valid (Eg: 654321')
        
        # Check 10 Digit Mobile Number
        if not phone_validate(data_dict['mob']) and valid_company:
            valid_company = False
            messagebox.showerror('Invalid Mobile Number', 'Mobile Number Not Valid (Eg. 9876543210)')
        
        # Check Valid Email
        if not email_validation(data_dict['email']) and valid_company:
            valid_company = False
            messagebox.showerror('Invalid Email', 'Email Not Valid')
        
        # If Company Data Valid Try to Insert/ Update it into DB
        if valid_company:
            company_list = list(data_dict.values())
            if self.selected_company:
                company_list.append(self.selected_company[0])
            else:
                company_list.append(0)
            
            # Insert to DB and Get Status and Message
            status, message = self.db_Manage_inst.insert_edit_company(company_list)
            
            # If Unsuccessfully
            if not status:
                messagebox.showerror('Company Not Created', f'{message}')  # Show Error Message
            else:
                messagebox.showinfo('Company Created Successfully', f'{message}')  # Show Success Message
                self.destroy_base()  # Remove Data and Widgets
                self.file_menu.entryconfig('Close Company', state=NORMAL)
                all_company_list = self.db_Manage_inst.fetch_company_list()
                for company_list_db in all_company_list:
                    if company_list_db[1] == company_list[0]:
                        self.selected_company = company_list_db
                self.root.title(f"{self.APP_NAME} - {self.selected_company[1]}")  # Include Company Name in Window Title
                self.load_other_menu_bars()
                self.selected_company = []
    
    # Ledger Data Validate
    def ledger_validate(self):
        # # Get Data from Widgets
        # Column names as List
        data_sequence = []  # List to store Data from Widgets
        valid_ledger = True  # Data Validation Status
        
        for index, widget in enumerate(self.base_Frame.winfo_children()):
            # Entry Widget Data Collection
            if widget.winfo_name().startswith('!entry'):
                data_sequence.append(widget.get())
                if data_sequence[(index // 2)]:
                    while data_sequence[(index // 2)][-1] == ' ':
                        data_sequence[(index // 2)] = data_sequence[(index // 2)][:-1]
        
        if not name_check(data_sequence[0]):
            valid_ledger = False
            messagebox.showerror('Invalid Ledger Name',
                                 'Allowed Letters, Numbers, (Space) with at least 3 letter Long')
        if not amount(data_sequence[1]) and valid_ledger:
            valid_ledger = False
            messagebox.showerror('Invalid Ledger Opening Balance', 'Allowed +ve or -ve Integer or Decimal Numbers')
        
        if valid_ledger:
            data_sequence[1] = float(data_sequence[1])
            if self.selected_ledger:
                data_sequence.append(self.selected_ledger[0])
            else:
                data_sequence.append(0)
            status, message = self.db_Manage_inst.insert_edit_ledger(data_sequence, self.selected_company)
            
            # If Unsuccessfully
            if not status:
                messagebox.showerror('Ledger Insert Failed', f'{message}')  # Show Error Message
            else:
                messagebox.showinfo('Ledger Successfully Inserted', f'{message}')  # Show Success Message
                self.destroy_base()  # Remove Data and Widgets
                self.selected_ledger = []
                self.create_ledgers_widget()
    
    # Party Data Validate
    def party_validate(self):
        # Get Data from Widgets
        
        # Column names as List
        data_sequence = ['party_name', 'party_address', 'state', 'type', 'pin', 'gstn', 'mob', 'email', 'opening']
        data_dict = {}  # Dict to store Data from Widgets
        valid_party = True  # Company Data Validation Status
        
        # Loop through Widgets to Get Data
        for index, widget in enumerate(self.base_Frame.winfo_children()):
            
            # Entry Widget Data Collection
            if widget.winfo_name().startswith('!entry'):
                data_dict[data_sequence[(index // 2)]] = widget.get()
                if data_dict[data_sequence[(index // 2)]]:
                    while data_dict[data_sequence[(index // 2)]][-1] == ' ':
                        data_dict[data_sequence[(index // 2)]] = data_dict[data_sequence[(index // 2)]][:-1]
            
            # Text Widget Data Collection
            if widget.winfo_name().startswith('!text'):
                data_dict[data_sequence[index // 2]] = widget.get('1.0', END)
            
            # Combo Box Widget Data Collection
            if widget.winfo_name().startswith('!combobox'):
                data_dict[data_sequence[index // 2]] = widget.get()
        data_dict['party_name'] = data_dict['party_name'].upper()  # Party Name In Upper Case
        data_dict['gstn'] = data_dict['gstn'].upper()  # Party GST Number In Upper Case
        
        # # Data Validation
        # Check Name for Special Char and Minimum Length 3
        if not name_check(data_dict['party_name']):
            valid_party = False
            messagebox.showerror('Invalid Party Name', 'Allowed Letters, Numbers, (Space) with at least 3 letter Long')
        
        # Check Address for Special Char and Minimum Length 5
        if not address_check(data_dict['party_address']) and valid_party:
            valid_party = False
            messagebox.showerror('Invalid Party Address', 'Allowed Letters, Numbers, (.), (,), (-), (_), (Space), '
                                                          '(Enter) and 5 Letter long')
        
        # Check if GSTN available and State Matching and GSTN Checksum Correct
        if not gstn_validate(data_dict['state'], data_dict['gstn']) and valid_party:
            valid_party = False
            messagebox.showerror('Invalid GST Number',
                                 'GST Number not Matching with State or GST Number maybe wrong')
        
        # Check Party Type is Not Blank
        if not data_dict['type'] and valid_party:
            valid_party = False
            messagebox.showerror('Party Type Not Selected', 'Please Select a Party Type')
        
        # Check PIN Code Valid
        if data_dict['pin']:
            if not pin_validation(data_dict['pin']) and valid_party:
                valid_party = False
                messagebox.showerror('Invalid PIN Code', 'PIN Code Not Valid')
        
        # Check 10 Digit Mobile Number
        if not phone_validate(data_dict['mob']) and valid_party:
            valid_party = False
            messagebox.showerror('Invalid Mobile Number', 'Mobile Number Not Valid(Eg. 9876543210)')
        
        # Check Valid Email
        if data_dict['email']:
            if not email_validation(data_dict['email']) and valid_party:
                valid_party = False
                messagebox.showerror('Invalid Email', 'Email Not Valid')
        
        # Check Party Opening Balance
        if data_dict['opening']:
            if not amount(data_dict['opening']):
                valid_party = False
                messagebox.showerror('Invalid Opening Balance', 'Enter a Valid Amount')
            else:
                data_dict['opening'] = float(data_dict['opening'])
        else:
            data_dict['opening'] = 0.0
        
        # If Party Data Valid Try to Insert it into DB
        if valid_party:
            party_list = list(data_dict.values())
            if self.selected_party:
                party_list.append(self.selected_party[0])
            else:
                party_list.append(0)
            
            # Insert to DB and Get Status and Message
            status, message = self.db_Manage_inst.insert_edit_party(party_list, self.selected_company)
            
            # If Unsuccessfully
            if not status:
                messagebox.showerror('Party Not Inserted', f'{message}')  # Show Error Message
            else:
                messagebox.showinfo('Party Inserted Successfully', f'{message}')  # Show Success Message
                self.destroy_base()  # Remove Data and Widgets
                self.selected_party = []
                self.create_party_widget()
    
    # Bill Validation
    def bill_validate(self):
        # Required Data Collecting
        company_name = '_'.join(self.selected_company[1].split(' '))
        
        # List of List All Party all Details
        all_parties_list = self.db_Manage_inst.fetch_party_list(company_name)
        
        # Get Data from Widgets
        
        # Column names as List
        data_sequence = ['bill_date', 'party_name', 'amount', 'type', 'notes']
        data_dict = {}  # Dict to store Data from Widgets
        valid_bill = True  # Bill Data Validation Status
        
        # Loop through Widgets to Get Data
        for index, widget in enumerate(self.base_Frame.winfo_children()):
            # Entry Widget Data Collection
            if 'entry' in widget.winfo_name():
                data_dict[data_sequence[(index // 2)]] = widget.get()
                if data_dict[data_sequence[(index // 2)]]:
                    while data_dict[data_sequence[(index // 2)]][-1] == ' ':
                        data_dict[data_sequence[(index // 2)]] = data_dict[data_sequence[(index // 2)]][:-1]
            
            # Text Widget Data Collection
            if widget.winfo_name().startswith('!text'):
                data_dict[data_sequence[index // 2]] = widget.get('1.0', END)
            
            # Combo Box Widget Data Collection
            if widget.winfo_name().startswith('!combobox'):
                data_dict[data_sequence[index // 2]] = widget.get()

        # # Data Validation
        data_list = []
        
        # Check Bill Date
        if not data_dict['bill_date']:
            valid_bill = False
            messagebox.showerror('Invalid Date', 'Please Select a Valid Date')
        else:
            data_list.append(data_dict['bill_date'])
        
        # Check Bill to Party
        if valid_bill:
            if not data_dict['party_name']:
                valid_bill = False
                messagebox.showerror('Invalid Party Name', 'Please Select a Party from The List')
            else:
                party_in_list = False
                for party_list in all_parties_list:
                    if party_list[1] == data_dict['party_name']:
                        party_in_list = True
                        data_list.append(party_list[0])
                if not party_in_list:
                    valid_bill = False
                    messagebox.showerror('Invalid Party Name', 'Please Select a Party from The List')
        
        # Check Bill Amount
        if valid_bill:
            if data_dict['amount']:
                if not amount(data_dict['amount']):
                    valid_bill = False
                    messagebox.showerror('Invalid Amount', 'Enter a Valid Amount')
                else:
                    data_list.append(float(data_dict['amount']))
            else:
                data_list.append(0.0)
        
        # Check Bill Type
        if valid_bill:
            if not data_dict['type']:
                valid_bill = False
                messagebox.showerror('Bill Type Not Selected', 'Select a Bill Type from The List')
            else:
                data_list.append(data_dict['type'])
        
        # Check Note
        if valid_bill:
            if not notes_check(data_dict['notes']) and valid_bill:
                valid_bill = False
                messagebox.showerror('Invalid Note', 'Allowed Letters, Numbers, (.), (,), (-), (_), (Space), (Enter)')
            else:
                data_list.append(data_dict['notes'])
        
        # If Bill Data Valid Try to Insert it into DB
        if valid_bill:
            if self.selected_bill:
                data_list.append(self.selected_bill[0])
            else:
                data_list.append(0)
            
            # Insert to DB and Get Status and Message
            status, message = self.db_Manage_inst.insert_edit_bill(data_list, self.selected_company)
            
            # If Unsuccessfully
            if not status:
                messagebox.showerror('Bill Not Inserted', f'{message}')  # Show Error Message
            else:
                messagebox.showinfo('Bill Inserted Successfully', f'{message}')  # Show Success Message
                self.destroy_base()  # Remove Data and Widgets
                self.selected_bill = []
                self.add_bill_widget()
    
    # Voucher Validation
    def voucher_validate(self):
        # Required Data Collecting
        company_name = '_'.join(self.selected_company[1].split(' '))
        
        # List of List All Party all Details
        all_parties_list = self.db_Manage_inst.fetch_party_list(company_name)
        all_ledgers = self.db_Manage_inst.fetch_ledger_list(company_name)
        
        # Get Data from Widgets
        
        # Column names as List
        data_sequence = ['voucher_date', 'party_name', 'ledger', 'amount', 'voucher_type', 'notes']
        data_dict = {}  # Dict to store Data from Widgets
        valid_voucher = True  # Bill Data Validation Status
        
        # Loop through Widgets to Get Data
        for index, widget in enumerate(self.base_Frame.winfo_children()):
            
            # Entry Widget Data Collection
            if 'entry' in widget.winfo_name():
                data_dict[data_sequence[(index // 2)]] = widget.get()
                if data_dict[data_sequence[(index // 2)]]:
                    while data_dict[data_sequence[(index // 2)]][-1] == ' ':
                        data_dict[data_sequence[(index // 2)]] = data_dict[data_sequence[(index // 2)]][:-1]
            
            # Text Widget Data Collection
            if widget.winfo_name().startswith('!text'):
                data_dict[data_sequence[index // 2]] = widget.get('1.0', END)
            
            # Combo Box Widget Data Collection
            if widget.winfo_name().startswith('!combobox'):
                data_dict[data_sequence[index // 2]] = widget.get()

        # # Data Validation
        data_list = []
        
        # Check Bill Date
        if not data_dict['voucher_date']:
            valid_voucher = False
            messagebox.showerror('Invalid Date', 'Please Select a Date')
        else:
            data_list.append(data_dict['voucher_date'])
        
        # Check Voucher Party
        if valid_voucher:
            if not data_dict['party_name']:
                valid_voucher = False
                messagebox.showerror('Invalid Party Name', 'Please Select a Party from The List')
            else:
                party_in_list = False
                for party_list in all_parties_list:
                    if party_list[1] == data_dict['party_name']:
                        party_in_list = True
                        data_list.append(party_list[0])
                if not party_in_list:
                    valid_voucher = False
                    messagebox.showerror('Invalid Party Name', 'Please Select a Party from The List')
        
        # Check Voucher Ledger
        if valid_voucher:
            if not data_dict['ledger']:
                valid_voucher = False
                messagebox.showerror('Invalid Ledger Name', 'Please Select Ledger Name from The List')
            else:
                voucher_type_in_list = False
                for ledger in all_ledgers:
                    if ledger[1] == data_dict['ledger']:
                        voucher_type_in_list = True
                        data_list.append(ledger[0])
                if not voucher_type_in_list:
                    valid_voucher = False
                    messagebox.showerror('Invalid Ledger Name', 'Please Select Ledger Name from The List')
        
        # Check Bill Amount
        if valid_voucher:
            if data_dict['amount']:
                if not amount(data_dict['amount']):
                    valid_voucher = False
                    messagebox.showerror('Invalid Amount', 'Enter a Valid Amount')
                else:
                    data_list.append(float(data_dict['amount']))
            else:
                data_list.append(0.0)
        
        # Check Voucher Type
        if valid_voucher:
            if not data_dict['voucher_type']:
                valid_voucher = False
                messagebox.showerror('Voucher Type Not Selected', 'Select a Voucher Type from The List')
            else:
                data_list.append(data_dict['voucher_type'])
        
        # Check Note
        if valid_voucher:
            if not notes_check(data_dict['notes']):
                valid_voucher = False
                messagebox.showerror('Invalid Note', 'Allowed Letters, Numbers, (.), (,), (-), (_), (Space), (Enter)')
            else:
                data_list.append(data_dict['notes'])
        
        # If Bill Data Valid Try to Insert it into DB
        if valid_voucher:
            if self.selected_voucher:
                data_list.append(self.selected_voucher[0])
            else:
                data_list.append(0)
            # Insert to DB and Get Status and Message
            status, message = self.db_Manage_inst.insert_edit_voucher(data_list, self.selected_company)
            
            # If Unsuccessfully
            if not status:
                messagebox.showerror('Voucher Not Inserted', f'{message}')  # Show Error Message
            else:
                messagebox.showinfo('Voucher Inserted Successfully', f'{message}')  # Show Success Message
                self.destroy_base()  # Remove Data and Widgets
                self.selected_bill = []
                self.add_voucher_widget()
    
    # # Create Widget Area
    # Menubar Widget
    def load_other_menu_bars(self):
        # Adding Items
        add_items_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Add Items', menu=add_items_menu)
        add_items_menu.add_command(label='Ledgers', command=self.create_ledgers_widget)
        add_items_menu.add_command(label='Party', command=self.create_party_widget)
        add_items_menu.add_command(label='Bill Voucher', command=self.add_bill_widget)
        add_items_menu.add_command(label='Cash Voucher', command=self.add_voucher_widget)
        
        # Editing Items
        edit_items_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit Items', menu=edit_items_menu)
        edit_items_menu.add_command(label='Ledgers', command=self.edit_ledgers_widget)
        edit_items_menu.add_command(label='Party', command=self.edit_party_widget)
        edit_items_menu.add_command(label='Bill Voucher', command=self.edit_bill_widget)
        edit_items_menu.add_command(label='Cash Voucher', command=self.edit_voucher_widget)
        
        # Report View & Download
        report_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Reports', menu=report_menu)
        report_menu.add_command(label='Ledgers', command=None)
        report_menu.add_command(label='Party', command=None)
        report_menu.add_command(label='Bill', command=None)
        report_menu.add_command(label='Receipt', command=None)
    
    # Create Company Widgets
    def create_company_widgets(self):
        self.file_menu.entryconfig('Create Company', state=DISABLED)
        self.file_menu.entryconfig('Open Company', state=DISABLED)
        self.file_menu.entryconfig('Exit', state=DISABLED)
        
        # Back Button Func
        def back_func():
            self.selected_company = []
            self.file_menu.entryconfig('Create Company', state=NORMAL)
            self.file_menu.entryconfig('Open Company', state=NORMAL)
            self.file_menu.entryconfig('Exit', state=NORMAL)
            self.destroy_base()
        
        # Widgets
        Label(self.base_Frame, text="Company Name*", font=15).grid(row=0, column=0, padx=20, pady=20)
        company_name_entry = Entry(self.base_Frame, font=15)
        company_name_entry.grid(row=0, column=1, padx=20, pady=20)
        company_name_entry.focus()
        Label(self.base_Frame, text="Company Address*", font=15).grid(row=1, column=0, padx=20, pady=20)
        self.company_address = Text(self.base_Frame, width=20, height=5, font=15)
        self.company_address.grid(row=1, column=1, padx=20, pady=20)
        self.company_address.bind("<Tab>", self.next_widget_to_address)
        
        Label(self.base_Frame, text="State*", font=15).grid(row=2, column=0, padx=20, pady=20)
        company_state_combo = ttk.Combobox(self.base_Frame, width=28, values=self.STATE_LIST, state='readonly')
        company_state_combo.current(31)
        company_state_combo.grid(row=2, column=1, padx=20, pady=20)
        
        Label(self.base_Frame, text="PIN Code*", font=15).grid(row=3, column=0, padx=20, pady=20)
        company_pin_entry = Entry(self.base_Frame, font=15)
        company_pin_entry.grid(row=3, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Company GSTN", font=15).grid(row=4, column=0, padx=20, pady=20)
        company_gstn_entry = Entry(self.base_Frame, font=15)
        company_gstn_entry.grid(row=4, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Company Mobile*", font=15).grid(row=5, column=0, padx=20, pady=20)
        company_mob_entry = Entry(self.base_Frame, font=15)
        company_mob_entry.grid(row=5, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Company E-Mail*", font=15).grid(row=6, column=0, padx=20, pady=20)
        company_email_entry = Entry(self.base_Frame, font=15)
        company_email_entry.grid(row=6, column=1, padx=20, pady=20)
        
        Button(self.base_Frame, text="Submit", font=15, command=self.company_validate).grid(row=7, column=0, padx=20,
                                                                                            pady=20)
        Button(self.base_Frame, text="Back", font=15, command=back_func).grid(row=7, column=1, padx=20, pady=20)
        
        if self.selected_company:
            Button(self.base_Frame, text="Delete", font=15, command=self.delete_company).grid(row=7, column=2, padx=20,
                                                                                              pady=20)
            company_name_entry.delete(0, END)
            company_name_entry.insert(0, self.selected_company[1])
            self.company_address.delete(0.1, END)
            self.company_address.insert(0.1, self.selected_company[2])
            company_state_combo.current(self.STATE_LIST.index(self.selected_company[3]))
            company_pin_entry.delete(0, END)
            company_pin_entry.insert(0, self.selected_company[4])
            company_gstn_entry.delete(0, END)
            company_gstn_entry.insert(0, self.selected_company[5])
            company_mob_entry.delete(0, END)
            company_mob_entry.insert(0, self.selected_company[6])
            company_email_entry.delete(0, END)
            company_email_entry.insert(0, self.selected_company[7])
    
    # Open Company Widget
    def open_company_widget(self):
        self.file_menu.entryconfig('Create Company', state=DISABLED)
        self.file_menu.entryconfig('Open Company', state=DISABLED)
        self.file_menu.entryconfig('Exit', state=DISABLED)
        
        # Open Company Back Button Function
        def back_func():
            self.file_menu.entryconfig('Create Company', state=NORMAL)
            self.file_menu.entryconfig('Open Company', state=NORMAL)
            self.file_menu.entryconfig('Exit', state=NORMAL)
            self.destroy_base()
        
        # Get All Company Data
        all_company_data = self.db_Manage_inst.fetch_company_list()
        
        # Open Company Tree View Headings
        column_heading = ['Company Name', 'Company Address', 'State', 'PIN Code', 'GSTN', 'Mobile', 'Email']
        
        # Open Company Tree View Page Heading Frame
        heading = Frame(self.base_Frame, relief=RAISED, bd=5, bg='light blue')
        heading.place(relx=0, rely=0, relwidth=1.0, relheight=0.1)
        
        # Open Company Tree View Heading Lablel
        Label(heading, text="Select Company", font=("Arial", 25), bg='light blue').pack(expand=True, fill=BOTH,
                                                                                        side=BOTTOM)
        
        # Open Company Tree View Frame
        tree_frame = Frame(self.base_Frame, bd=5, bg='light blue')
        tree_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.5)
        
        # Tree View
        tree_view = ttk.Treeview(tree_frame,
                                 columns=column_heading,
                                 show='headings',
                                 height=8,
                                 selectmode='browse')
        
        # Open Company Tree View Column Settings and Insert Name
        for index, head in enumerate(column_heading, start=1):
            tree_view.column(f'#{index}', anchor=CENTER, minwidth=0, width=190, stretch=NO)
            tree_view.heading(f'#{index}', text=head)
        
        # Open Company Tree View Data Insert
        for index, company in enumerate(all_company_data, start=1):
            company = [data.split('\n')[0] if isinstance(data, str) else data for data in company]
            tree_view.insert('', 'end', text=f'{index}', values=company[1:])
        
        # Open Company Vertical Scroll Bar Settings
        tree_v_scroll_bar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_view.yview)
        tree_view.configure(yscrollcommand=tree_v_scroll_bar.set)
        tree_v_scroll_bar.pack(side=RIGHT, fill=BOTH)
        
        tree_view.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        
        # Open Company Edit Delete Options By Right-Clicking
        def right_click(event):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'cell':
                # Get The Reference of Selected Item
                item = tree_view.selection()
                
                # Get The Values of Selected Item
                selection = tree_view.item(item, 'values')
                
                # If address is Multi line it will Be Cropped so get the real data from DB
                for company in all_company_data:
                    if company[1] == selection[0]:
                        self.selected_company = company  # Full Data from Company Lists
                self.destroy_base()  # Clear Window
                self.create_company_widgets()  # Edit Data In Create Company Widget
            
        # Bind Tree View for Right Click
        tree_view.bind('<Button-3>', right_click)
        
        # Double click to Open Company
        def double_click(event):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'cell':
                # Get The Reference of Selected Item
                item = tree_view.selection()[0]
                
                # Get The Values of Selected Company
                selection = tree_view.item(item, 'values')[0]
                
                # If address is Multi line it will Be Cropped so get the real data from DB
                for company in all_company_data:
                    if company[1] == selection:
                        self.selected_company = company  # Full Data from Company Lists
                self.destroy_base()  # Clear Window
                self.root.title(f"{self.APP_NAME} - {self.selected_company[1]}")  # Include Company Name in Window Title
                
                # Show Menubar For Selected Company
                self.load_other_menu_bars()
                
                # Disable Create and Open Company Menus
                self.file_menu.entryconfig('Create Company', state=DISABLED)
                self.file_menu.entryconfig('Open Company', state=DISABLED)
                self.file_menu.entryconfig('Close Company', state=NORMAL)
            
        # Bind Tree View for Double Click
        tree_view.bind('<Double-1>', double_click)
        
        # Insert Note Below the Tree View How it works
        # Tree View Page Note Frame
        bottom_frame = Frame(self.base_Frame, relief=RAISED, bd=2, bg='light blue')
        bottom_frame.place(relx=0, rely=0.6, relwidth=1.0, relheight=0.1)
        Button(bottom_frame, text="Back", font=15, command=back_func).grid(row=0, column=0, padx=20, pady=20)
        note_frame = Frame(bottom_frame, bg='light blue')
        note_frame.place(relx=0.1, rely=0, relwidth=0.9, relheight=1.0)
        note = "Note: Select and Right Click to Edit or Delete the Company\n Double Click to Open The Company"
        note_label = Label(note_frame, text=note, font=15, bg='light blue', anchor=W)
        note_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
    
    # Create Ledger Widget
    def create_ledgers_widget(self):
        self.destroy_menu_bars()  # Remove all Menu Till Process End
        
        # Back Button Function
        def back_func():
            self.destroy_base()
            self.load_other_menu_bars()
            if self.selected_ledger:
                self.selected_ledger = []
                self.edit_ledgers_widget()
                
        
        # TK Variables
        account_name = StringVar()
        account_opening = StringVar()
        
        # Widgets
        Label(self.base_Frame, text="Ledger Name*", font=15).grid(row=0, column=0, padx=20, pady=20)
        name_entry = Entry(self.base_Frame, font=15, textvariable=account_name)
        name_entry.grid(row=0, column=1, padx=20, pady=20)
        name_entry.focus()
        Label(self.base_Frame, text="Opening Balance*", font=15).grid(row=3, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=account_opening).grid(row=3, column=1, padx=20, pady=20)
        
        Button(self.base_Frame, text="Submit", font=15, command=self.ledger_validate).grid(row=7, column=0,
                                                                                           padx=20, pady=20)
        Button(self.base_Frame, text="Back", font=15, command=back_func).grid(row=7, column=1, padx=20, pady=20)
        
        if self.selected_ledger:
            Button(self.base_Frame, text="Delete", font=15, command=self.delete_ledger).grid(row=7, column=2, padx=20,
                                                                                             pady=20)
            account_name.set(self.selected_ledger[1])
            account_opening.set(self.selected_ledger[2])
    
    # Edit Ledger Widget
    def edit_ledgers_widget(self):
        self.destroy_menu_bars()  # Remove all Menu Till Process End
        
        # Back Button Function
        def back_func():
            self.destroy_base()
            self.load_other_menu_bars()
            self.selected_ledger = []
            
        
        selected_company_name = '_'.join(self.selected_company[1].split(' '))
        
        # Fetch all account Types
        all_account_types = self.db_Manage_inst.fetch_ledger_list(selected_company_name)
        
        # Tree View Headings
        column_heading = ['Ledger Name', 'Opening Balance']
        
        # Tree View Page Heading Frame
        heading = Frame(self.base_Frame, relief=RAISED, bd=5, bg='light blue')
        heading.place(relx=0, rely=0, relwidth=1.0, relheight=0.1)
        
        # Tree View Heading Lablel
        Label(heading, text="Edit Ledgers", font=("Arial", 25), bg='light blue').pack(expand=True, fill=BOTH,
                                                                                      side=BOTTOM)
        
        # Tree View Frame
        tree_frame = Frame(self.base_Frame, bd=5, bg='light blue')
        tree_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.3)
        
        # Tree View
        tree_view = ttk.Treeview(tree_frame,
                                 columns=column_heading,
                                 show='headings',
                                 height=8,
                                 selectmode='browse')
        
        # Tree View Column Settings
        for index, head in enumerate(column_heading, start=1):
            tree_view.column(f'#{index}', anchor=CENTER, minwidth=0, width=150, stretch=NO)
            tree_view.heading(f'#{index}', text=head)
        
        # Tree View Data Insert
        for index, account_type in enumerate(all_account_types, start=1):
            account_type = [data.split('\n')[0] if isinstance(data, str) else data for data in account_type]
            tree_view.insert('', 'end', text=f'{index}', values=account_type[1:])
        
        # Vertical Scroll Bar Settings
        tree_v_scroll_bar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_view.yview)
        tree_view.configure(yscrollcommand=tree_v_scroll_bar.set)
        tree_v_scroll_bar.pack(side=RIGHT, fill=BOTH)
        
        tree_view.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        
        # Double click to Edit Ledger
        def double_click(event):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'cell':
                # Get The Reference of Selected Item
                item = tree_view.selection()[0]
                
                # Get The Values of Selected Item
                selection = tree_view.item(item, 'values')[0]
                
                # If address is Multi line it will Be Cropped so get the real data from DB
                for account_type in all_account_types:
                    if account_type[1] == selection:
                        self.selected_ledger = account_type  # Full Data from Company Lists
                self.destroy_base()  # Clear Window
                self.create_ledgers_widget()
            
        # Bind Tree View for Double Click
        tree_view.bind('<Double-1>', double_click)
        
        # Insert Note Below the Tree View How it works
        # Tree View Page Note Frame
        bottom_frame = Frame(self.base_Frame, relief=RAISED, bd=2, bg='light blue')
        bottom_frame.place(relx=0, rely=0.4, relwidth=1.0, relheight=0.1)
        Button(bottom_frame, text="Back", font=15, command=back_func).grid(row=0, column=0, padx=20, pady=20)
        note_frame = Frame(bottom_frame, bg='light blue')
        note_frame.place(relx=0.1, rely=0, relwidth=0.9, relheight=1.0)
        note = "Note: Double Click to Edit the Ledger"
        note_label = Label(note_frame, text=note, font=15, bg='light blue', anchor=CENTER)
        note_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
    
    # Create Party Widget
    def create_party_widget(self):
        # Search Party Type Combo Box
        def party_type_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
            
            # If Value is Blank Use Full List as Value
            if value == '':
                party_type_combo['value'] = self.PARTY_TYPE_LIST
            
            # If Value is Entered Filter the items Starts with the letter
            else:
                party_type_filter_list = []
                for party_type in self.PARTY_TYPE_LIST:
                    if party_type.startswith(value.upper()):
                        party_type_filter_list.append(party_type)
                
                party_type_combo['value'] = party_type_filter_list
            party_type_combo.event_generate('<Down>')
        
        self.destroy_menu_bars()  # Remove all Menu Till Process End
        
        # Back Button Function
        def back_func():
            self.destroy_base()
            self.load_other_menu_bars()
            if self.selected_party:
                self.selected_party = []
                self.edit_party_widget()
        
        # TK Variables
        
        party_name = StringVar()
        party_pin = StringVar()
        party_gstn = StringVar()
        party_mob = StringVar()
        party_email = StringVar()
        party_opening = StringVar()
        
        # Widgets
        Label(self.base_Frame, text="Party Name*", font=15).grid(row=0, column=0, padx=20, pady=20)
        name_entry = Entry(self.base_Frame, font=15, textvariable=party_name)
        name_entry.grid(row=0, column=1, padx=20, pady=20)
        name_entry.focus()
        
        Label(self.base_Frame, text="Party Address*", font=15).grid(row=1, column=0, padx=20, pady=20)
        self.party_address = Text(self.base_Frame, width=20, height=4, font=15)
        self.party_address.grid(row=1, column=1, padx=20, pady=20)
        self.party_address.bind("<Tab>", self.next_widget_to_address)  # Tab to Next Widget from Text Widget
        
        Label(self.base_Frame, text="State*", font=15).grid(row=2, column=0, padx=20, pady=20)
        state = ttk.Combobox(self.base_Frame, width=28, values=self.STATE_LIST)
        state.current(31)
        state.grid(row=2, column=1, padx=20, pady=20)
        
        Label(self.base_Frame, text="Party Type*", font=15).grid(row=3, column=0, padx=20, pady=20)
        party_type_combo = ttk.Combobox(self.base_Frame, width=28, values=self.PARTY_TYPE_LIST, state='readonly')
        party_type_combo.grid(row=3, column=1, padx=20, pady=20)
        party_type_combo.bind('<KeyRelease>', party_type_check_input)
        
        Label(self.base_Frame, text="PIN Code", font=15).grid(row=4, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=party_pin).grid(row=4, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Party GSTN", font=15).grid(row=5, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=party_gstn).grid(row=5, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Party Mobile*", font=15).grid(row=6, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=party_mob).grid(row=6, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Party E-Mail", font=15).grid(row=7, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=party_email).grid(row=7, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Opening Balance*", font=15).grid(row=8, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=party_opening).grid(row=8, column=1, padx=20, pady=20)
        
        Button(self.base_Frame, text="Submit", font=15, command=self.party_validate).grid(row=9, column=0, padx=20,
                                                                                          pady=20)
        Button(self.base_Frame, text="Back", font=15, command=back_func).grid(row=9, column=1, padx=20, pady=20)
        
        if self.selected_party:
            Button(self.base_Frame, text="Delete", font=15, command=self.delete_party).grid(row=9, column=2, padx=20,
                                                                               pady=20)
            party_name.set(self.selected_party[1])
            self.party_address.delete(0.1, END)
            self.party_address.insert(0.1, self.selected_party[2])
            state.current(self.STATE_LIST.index(self.selected_party[3]))
            party_type_combo.current(self.PARTY_TYPE_LIST.index(self.selected_party[4]))
            party_pin.set(self.selected_party[5])
            party_gstn.set(self.selected_party[6])
            party_mob.set(self.selected_party[7])
            party_email.set(self.selected_party[8])
            party_opening.set(self.selected_party[9])
    
    # Edit Party Widget
    def edit_party_widget(self):
        self.destroy_menu_bars()  # Remove all Menu Till Process End
        
        # Back Button Function
        def back_func():
            self.selected_party = []
            self.destroy_base()
            self.load_other_menu_bars()
        
        selected_company_name = '_'.join(self.selected_company[1].split(' '))
        
        # Fetch all account Types
        all_party_list = self.db_Manage_inst.fetch_party_list(selected_company_name)
        
        # Tree View Headings
        column_heading = ['Party Name', 'Party Address', 'State', 'PIN Code', 'GSTN', 'Mobile', 'Email', 'Opening']
        
        # Tree View Page Heading Frame
        heading = Frame(self.base_Frame, relief=RAISED, bd=5, bg='light blue')
        heading.place(relx=0, rely=0, relwidth=1.0, relheight=0.1)
        
        # Tree View Heading Lablel
        Label(heading, text="Select Party", font=("Arial", 25), bg='light blue').pack(expand=True, fill=BOTH,
                                                                                      side=BOTTOM)
        
        # Tree View Frame
        tree_frame = Frame(self.base_Frame, bd=5, bg='light blue')
        tree_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.3)
        
        # Tree View
        tree_view = ttk.Treeview(tree_frame,
                                 columns=column_heading,
                                 show='headings',
                                 height=8,
                                 selectmode='browse')
        
        # Tree View Column Settings
        for index, head in enumerate(column_heading, start=1):
            tree_view.column(f'#{index}', anchor=CENTER, minwidth=0, width=190, stretch=NO)
            tree_view.heading(f'#{index}', text=head)
        
        # Tree View Data Insert
        for index, party in enumerate(all_party_list, start=1):
            party = [data.split('\n')[0] if isinstance(data, str) else data for data in party]
            tree_view.insert('', 'end', text=f'{index}', values=party[1:])
        
        # Vertical Scroll Bar Settings
        tree_v_scroll_bar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_view.yview)
        tree_view.configure(yscrollcommand=tree_v_scroll_bar.set)
        tree_v_scroll_bar.pack(side=RIGHT, fill=BOTH)
        
        tree_view.pack(fill=Y)
        
        # Double click to Open Company
        def double_click(event):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'cell':
                # Get The Reference of Selected Item
                item = tree_view.selection()[0]
                
                # Get The Values of Selected Item
                selection = tree_view.item(item, 'values')[0]
                
                # Get the real data from DB including ID
                for party in all_party_list:
                    if party[1] == selection:
                        self.selected_party = party  # Full Data from Party Lists
                self.destroy_base()  # Clear Window
                self.create_party_widget()  # Create Party Widget used to Edit Too
            
        # Bind Tree View for Double Click
        tree_view.bind('<Double-1>', double_click)
        
        # Insert Note Below the Tree View How it works
        # Tree View Page Note Frame
        bottom_frame = Frame(self.base_Frame, relief=RAISED, bd=2, bg='light blue')
        bottom_frame.place(relx=0, rely=0.4, relwidth=1.0, relheight=0.1)
        Button(bottom_frame, text="Back", font=15, command=back_func).grid(row=0, column=0, padx=20, pady=20)
        note_frame = Frame(bottom_frame, bg='light blue')
        note_frame.place(relx=0.1, rely=0, relwidth=0.9, relheight=1.0)
        note = "Note: Double Click to Edit The Party"
        note_label = Label(note_frame, text=note, font=15, bg='light blue', anchor=CENTER)
        note_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
    
    # Add Bill Widget
    def add_bill_widget(self):
        self.destroy_menu_bars()  # Remove all Menu Till Process End
        
        # Back Button Function
        def back_func():
            self.destroy_base()
            self.load_other_menu_bars()
            if self.selected_bill:
                self.selected_bill = []
                self.edit_bill_widget()
        
        # Required Data Collecting
        company_name = '_'.join(self.selected_company[1].split(' '))
        
        # List of List All Party all Details
        all_parties_list = self.db_Manage_inst.fetch_party_list(company_name)
        
        # Party Name only List
        party_name_only_list = [party[1] for party in all_parties_list]
        
        today_date = datetime.today()
        year = today_date.year
        
        # Search Party Name Combo Box
        def party_name_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
            
            # If Value is Blank Use Full List as Value
            if value == '':
                party_name_combobox['value'] = party_name_only_list
            
            # If Value is Entered Filter the items Starts with the letter
            else:
                party_name_filter_list = []
                for party_name_only in party_name_only_list:
                    if party_name_only.startswith(value.upper()):
                        party_name_filter_list.append(party_name_only)
                
                party_name_combobox['value'] = party_name_filter_list
            party_name_combobox.event_generate('<Down>')
        
        # Search Party Type Combo Box
        def bill_type_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
            
            # If Value is Blank Use Full List as Value
            if value == '':
                bill_type_combo['value'] = self.BILL_TYPE_LIST
            
            # If Value is Entered Filter the items Starts with the letter
            else:
                party_type_filter_list = []
                for party_type in self.BILL_TYPE_LIST:
                    if party_type.startswith(value.upper()):
                        party_type_filter_list.append(party_type)
                
                bill_type_combo['value'] = party_type_filter_list
            bill_type_combo.event_generate('<Down>')
        
        # TK Variables
        bill_amount = StringVar()
        bill_type = StringVar()
        
        # Widgets
        Label(self.base_Frame, text="Date*", font=15).grid(row=0, column=0, padx=20, pady=20)
        bill_date = DateEntry(self.base_Frame, selectmode='day', year=year, date_pattern='dd-mm-y', state='readonly')
        bill_date.grid(row=0, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Select Party*", font=15).grid(row=1, column=0, padx=20, pady=20)
        party_name_combobox = ttk.Combobox(self.base_Frame, width=28, values=party_name_only_list)
        party_name_combobox.grid(row=1, column=1, padx=20, pady=20)
        party_name_combobox.bind('<KeyRelease>', party_name_check_input)
        
        party_name_combobox.focus()
        
        Label(self.base_Frame, text="Amount*", font=15).grid(row=2, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=bill_amount).grid(row=2, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Bill Type*", font=15).grid(row=3, column=0, padx=20, pady=20)
        bill_type_combo = ttk.Combobox(self.base_Frame, width=28, values=self.BILL_TYPE_LIST, state='readonly')
        bill_type_combo.grid(row=3, column=1, padx=20, pady=20)
        bill_type_combo.bind('<KeyRelease>', bill_type_check_input)
        
        Label(self.base_Frame, text="Bill Notes", font=15).grid(row=4, column=0, padx=20, pady=20)
        bill_notes = Text(self.base_Frame, width=20, height=4, font=15)
        bill_notes.grid(row=4, column=1, padx=20, pady=20)
        bill_notes.bind("<Tab>", self.next_widget_to_address)  # Tab to Next Widget from Text Widget
        
        Button(self.base_Frame, text="Submit", font=15, command=self.bill_validate).grid(row=5, column=0, padx=20,
                                                                                         pady=20)
        Button(self.base_Frame, text="Back", font=15, command=back_func).grid(row=5, column=1, padx=20, pady=20)
        
        if self.selected_bill:
            Button(self.base_Frame, text="Delete", font=15, command=self.delete_bill).grid(row=5, column=2, padx=20,
                                                                               pady=20)
            
            # Insert Bill Date
            bill_date.set_date(self.selected_bill[1])
            
            # Iterate through All Party List of List from DB
            for party_list in all_parties_list:
                # If Party ID Match with Selected Bill Party ID
                if party_list[0] == self.selected_bill[2]:
                    # get the Index of Party name Only List and Set The Value
                    party_name_combobox.current(party_name_only_list.index(party_list[1]))
            # Set other values
            bill_amount.set(self.selected_bill[3])
            bill_type_combo.current(self.BILL_TYPE_LIST.index(self.selected_bill[4]))
            bill_notes.delete(0.1, END)
            bill_notes.insert(0.1, self.selected_bill[5])
    
    # Add Voucher Widget
    def add_voucher_widget(self):
        self.destroy_menu_bars()  # Remove all Menu Till Process End
    
        # Back Button Function
        def back_func():
            self.destroy_base()
            self.load_other_menu_bars()
            if self.selected_voucher:
                self.selected_voucher = []
                self.edit_voucher_widget()
            
        # Required Data Collecting
        company_name = '_'.join(self.selected_company[1].split(' '))
        
        # List of All Details
        all_parties_list = self.db_Manage_inst.fetch_party_list(company_name)
        all_ledgers_list = self.db_Manage_inst.fetch_ledger_list(company_name)
        
        # Name only List
        party_name_only_list = [party[1] for party in all_parties_list]
        ledgers_name_only_list = [ledger[1] for ledger in all_ledgers_list]
        
        today_date = datetime.today()
        year = today_date.year
        
        # Search Party Name Combo Box
        def party_name_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
            
            # If Value is Blank Use Full List as Value
            if value == '':
                party_name_combobox['value'] = party_name_only_list
            
            # If Value is Entered Filter the items Starts with the letter
            else:
                party_name_filter_list = []
                for party_name_only in party_name_only_list:
                    if party_name_only.startswith(value.upper()):
                        party_name_filter_list.append(party_name_only)
                
                party_name_combobox['value'] = party_name_filter_list
            party_name_combobox.event_generate('<Down>')
        
        # Search Voucher Type Combo Box
        def voucher_type_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
            
            # If Value is Blank Use Full List as Value
            if value == '':
                voucher_type_combo['value'] = self.VOUCHER_TYPE_LIST
            
            # If Value is Entered Filter the items Starts with the letter
            else:
                voucher_type_filter_list = []
                for voucher_type in self.VOUCHER_TYPE_LIST:
                    if voucher_type.startswith(value.upper()):
                        voucher_type_filter_list.append(voucher_type)
                
                voucher_type_combo['value'] = voucher_type_filter_list
            voucher_type_combo.event_generate('<Down>')
        
        # Search Ledger Combo Box
        def ledger_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
            
            # If Value is Blank Use Full List as Value
            if value == '':
                ledger_combo['value'] = ledgers_name_only_list
            
            # If Value is Entered Filter the items Starts with the letter
            else:
                ledger_list = []
                for ledgers_name in ledgers_name_only_list:
                    if ledgers_name.startswith(value.upper()):
                        ledger_list.append(ledgers_name)
                
                ledger_combo['value'] = ledger_list
            ledger_combo.event_generate('<Down>')
        
        # TK Variables
        voucher_amount = StringVar()
        bill_type = StringVar()
        
        # Widgets
        Label(self.base_Frame, text="Date*", font=15).grid(row=0, column=0, padx=20, pady=20)
        voucher_date = DateEntry(self.base_Frame, selectmode='day', year=year, date_pattern='dd-mm-y', state='readonly')
        voucher_date.grid(row=0, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Select Party*", font=15).grid(row=1, column=0, padx=20, pady=20)
        party_name_combobox = ttk.Combobox(self.base_Frame, width=28, values=party_name_only_list)
        party_name_combobox.grid(row=1, column=1, padx=20, pady=20)
        party_name_combobox.bind('<KeyRelease>', party_name_check_input)
        
        party_name_combobox.focus()
        
        Label(self.base_Frame, text="Ledger*", font=15).grid(row=2, column=0, padx=20, pady=20)
        ledger_combo = ttk.Combobox(self.base_Frame, width=28, values=ledgers_name_only_list, state='readonly')
        ledger_combo.grid(row=2, column=1, padx=20, pady=20)
        ledger_combo.bind('<KeyRelease>', ledger_check_input)
        
        Label(self.base_Frame, text="Amount*", font=15).grid(row=3, column=0, padx=20, pady=20)
        Entry(self.base_Frame, font=15, textvariable=voucher_amount).grid(row=3, column=1, padx=20, pady=20)
        Label(self.base_Frame, text="Voucher Type*", font=15).grid(row=4, column=0, padx=20, pady=20)
        voucher_type_combo = ttk.Combobox(self.base_Frame, width=28, values=self.VOUCHER_TYPE_LIST, state='readonly')
        voucher_type_combo.grid(row=4, column=1, padx=20, pady=20)
        voucher_type_combo.bind('<KeyRelease>', voucher_type_check_input)
        
        Label(self.base_Frame, text="Voucher Notes", font=15).grid(row=5, column=0, padx=20, pady=20)
        voucher_notes = Text(self.base_Frame, width=20, height=4, font=15)
        voucher_notes.grid(row=5, column=1, padx=20, pady=20)
        voucher_notes.bind("<Tab>", self.next_widget_to_address)  # Tab to Next Widget from Text Widget
        
        Button(self.base_Frame, text="Submit", font=15, command=self.voucher_validate).grid(row=6, column=0, padx=20,
                                                                                            pady=20)
        Button(self.base_Frame, text="Back", font=15, command=back_func).grid(row=6, column=1, padx=20, pady=20)
        
        if self.selected_voucher:

            Button(self.base_Frame, text="Delete", font=15, command=self.delete_voucher).grid(row=6, column=2, padx=20,
                                                                               pady=20)
            voucher_date.set_date(self.selected_voucher[1])
            for party_list in all_parties_list:
                if party_list[0] == self.selected_voucher[2]:
                    party_name_combobox.current(party_name_only_list.index(party_list[1]))
            
            for ledgers_list in all_ledgers_list:
                if ledgers_list[0] == self.selected_voucher[3]:
                    ledger_combo.current(ledgers_name_only_list.index(ledgers_list[1]))
            
            voucher_amount.set(self.selected_voucher[4])
            voucher_type_combo.current(self.VOUCHER_TYPE_LIST.index(self.selected_voucher[5]))
            voucher_notes.delete(0.1, END)
            voucher_notes.insert(0.1, self.selected_voucher[6])
    
    # Edit Bill Widget
    def edit_bill_widget(self):
        self.destroy_menu_bars()  # Remove all Menu Till Process End
        
        # Back Button Function
        def back_func():
            self.selected_bill = []
            self.destroy_base()
            self.load_other_menu_bars()
        
        # Required Data Collecting
        company_name = '_'.join(self.selected_company[1].split(' '))
        
        # List of All Details
        all_parties_list = self.db_Manage_inst.fetch_party_list(company_name)
        
        # Name only List
        party_name_only_list = [party[1] for party in all_parties_list]
        
        today_date = datetime.today()
        year = today_date.year
        
        date_var = StringVar()
        
        # Search Function
        def search_func():
            date = date_var.get()
            party_name = party_name_combobox.get()
            if not any(filter(lambda party: party_name in party, all_parties_list)):
                party_name = ""
            self.bill_edit_treeview(date, party_name)
            
        
        # Search Party Name Combo Box
        def party_name_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
            
            # If Value is Blank Use Full List as Value
            if value == '':
                party_name_combobox['value'] = party_name_only_list
            
            # If Value is Entered Filter the items Starts with the letter
            else:
                party_name_filter_list = []
                for party_name_only in party_name_only_list:
                    if party_name_only.startswith(value.upper()):
                        party_name_filter_list.append(party_name_only)
                
                party_name_combobox['value'] = party_name_filter_list
            party_name_combobox.event_generate('<Down>')
        
        # Clear Filters
        def clear_func():
            date_var.set("")
            party_name_combobox.set("")
            self.bill_edit_treeview()
        
        # Tree View Page Heading Frame
        heading = Frame(self.base_Frame, relief=RAISED, bd=5, bg='light blue')
        heading.place(relx=0, rely=0, relwidth=1.0, relheight=0.1)
        
        # Tree View Heading Lablel
        Label(heading, text="Edit Bill", font=("Arial", 25), bg='light blue').pack(expand=True, fill=BOTH,
                                                                                   side=BOTTOM)
        # Tree View Frame
        controls_frame = Frame(self.base_Frame, relief=RAISED, bd=5, bg='light blue')
        controls_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
        
        Label(controls_frame, text="Date*", font=15).grid(row=0, column=0, padx=20, pady=15)
        bill_date = DateEntry(controls_frame, selectmode='day', year=year, date_pattern='dd-mm-y', state='readonly',
                              textvariable=date_var)
        date_var.set("")
        bill_date.grid(row=0, column=1, padx=20, pady=15)
        
        Label(controls_frame, text="Select Party*", font=15).grid(row=0, column=2, padx=20, pady=15)
        party_name_combobox = ttk.Combobox(controls_frame, width=28, values=party_name_only_list)
        party_name_combobox.grid(row=0, column=3, padx=20, pady=15)
        party_name_combobox.bind('<KeyRelease>', party_name_check_input)
        
        Button(controls_frame, text="Search", font=15, command=search_func).grid(row=0, column=4, padx=20, pady=15)
        Button(controls_frame, text="Clear", font=15, command=clear_func).grid(row=0, column=5, padx=20, pady=15)
        Button(controls_frame, text="Back", font=15, command=back_func).grid(row=0, column=6, padx=20, pady=15)
        self.bill_edit_treeview()
    
    # Edit Bill Tree View Widget
    def bill_edit_treeview(self, bill_date="", party_name=""):
        selected_company_name = '_'.join(self.selected_company[1].split(' '))
        
        # Fetch all Data Types
        all_party_list = self.db_Manage_inst.fetch_party_list(selected_company_name)
        all_bills_list = self.db_Manage_inst.fetch_bill_list(selected_company_name)
        
        # Create Dict For Party ID to Name
        all_party_dict = {party[1]: party[0] for party in all_party_list}
        all_party_dict_id = {party[0]: party[1] for party in all_party_list}
        
        filter_bills = []
        # If Date and party Filter set
        if bill_date and party_name:
            for bill in all_bills_list:
                if bill[1] == bill_date and bill[2] == all_party_dict.get(party_name):
                    bill[2] = party_name
                    filter_bills.append(list(bill))
        
        # If Date Filter only
        elif bill_date:
            for bill in all_bills_list:
                if bill[1] == bill_date:
                    filter_bills.append(list(bill))
        
        # If Party Filter Only
        elif party_name:
            for bill in all_bills_list:
                if bill[2] == all_party_dict.get(party_name):
                    filter_bills.append(list(bill))
        
        # No Filter Set Then Show All Data
        else:
            for bill in all_bills_list:
                filter_bills.append(list(bill))
        
        # Change Filtered List Party ID To Party Name
        for index, bill in enumerate(filter_bills):
            bill [2] = all_party_dict_id.get(bill[2])
            filter_bills[index] = bill
            
        # Tree View Headings
        column_heading = ['Bill Date', 'Party Name', 'Amount', 'Bill Type', 'Notes']
        
        # Tree View Frame
        tree_frame = Frame(self.base_Frame, bd=5, bg='light blue')
        tree_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.7)
        
        # Tree View
        tree_view = ttk.Treeview(tree_frame,
                                 columns=column_heading,
                                 show='headings',
                                 height=8,
                                 selectmode='browse')
        
        # Tree View Column Settings
        for index, head in enumerate(column_heading, start=1):
            tree_view.column(f'#{index}', anchor=CENTER, minwidth=0, width=190, stretch=NO)
            tree_view.heading(f'#{index}', text=head)
        
        # Tree View Data Insert
        for index, party in enumerate(filter_bills, start=1):
            party = [data.split('\n')[0] if isinstance(data, str) else data for data in party]
            tree_view.insert('', 'end', text=f'{index}', values=party[1:])
        
        # Vertical Scroll Bar Settings
        tree_v_scroll_bar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_view.yview)
        tree_view.configure(yscrollcommand=tree_v_scroll_bar.set)
        tree_v_scroll_bar.pack(side=RIGHT, fill=BOTH)
        
        tree_view.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        
        # Double click to Open Company
        def double_click(event):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'cell':
                # Get The Reference of Selected Item
                item = tree_view.selection()[0]
                
                # Get The Values of Selected Item
                selection = tree_view.item(item, 'values')[0]
                
                # Get the real data from DB including ID
                for bill in all_bills_list:
                    if bill[1] == selection:
                        self.selected_bill = bill  # Full Data from Party Lists
                self.destroy_base()  # Clear Window
                self.add_bill_widget()  # Create Party Widget used to Edit Too
            
        # Bind Tree View for Double Click
        tree_view.bind('<Double-1>', double_click)
        
        # Insert Note Below the Tree View How it works
        # Tree View Page Note Frame
        bottom_frame = Frame(self.base_Frame, relief=RAISED, bd=2, bg='light blue')
        bottom_frame.place(relx=0, rely=0.9, relwidth=1.0, relheight=0.1)

        note = "Note: Double Click to Edit The Bill"
        note_label = Label(bottom_frame, text=note, font=15, bg='light blue', anchor=CENTER)
        note_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    # Edit Voucher Widget
    def edit_voucher_widget(self):
        self.destroy_menu_bars()  # Remove all Menu Till Process End

        # Back Button Function
        def back_func():
            self.selected_voucher = []
            self.destroy_base()
            self.load_other_menu_bars()

        # Required Data Collecting
        company_name = '_'.join(self.selected_company[1].split(' '))

        # List of All Details
        all_parties_list = self.db_Manage_inst.fetch_party_list(company_name)
        all_ledger_list = self.db_Manage_inst.fetch_ledger_list(company_name)

        # Name only List
        party_name_only_list = [party[1] for party in all_parties_list]
        ledger_name_only_list = [ledger[1] for ledger in all_ledger_list]

        today_date = datetime.today()
        year = today_date.year

        date_var = StringVar()

        # Search Function
        def search_func():
            date = date_var.get()
            party_name = party_name_combobox.get()
            ledger_type = ledger_combobox.get()
            if not any(filter(lambda party: party_name in party, all_parties_list)):
                party_name = ''
            if not any(filter(lambda ledger: ledger_type in ledger, all_ledger_list)):
                ledger_type = ''
                
            self.voucher_edit_treeview(date, party_name, ledger_type)

        # Search Party Name Combo Box
        def party_name_check_input(event):
            # Get the Entered Value
            value = event.widget.get()
    
            # If Value is Blank Use Full List as Value
            if value == '':
                party_name_combobox['value'] = party_name_only_list
    
            # If Value is Entered Filter the items Starts with the letter
            else:
                party_name_filter_list = []
                for party_name_only in party_name_only_list:
                    if party_name_only.startswith(value.upper()):
                        party_name_filter_list.append(party_name_only)
        
                party_name_combobox['value'] = party_name_filter_list
            party_name_combobox.event_generate('<Down>')

        # Search Ledger Name Combo Box
        def ledger_name_check_input(event):
            # Get the Entered Value
            value = event.widget.get()

            # If Value is Blank Use Full List as Value
            if value == '':
                ledger_combobox['value'] = ledger_name_only_list

            # If Value is Entered Filter the items Starts with the letter
            else:
                ledger_name_filter_list = []
                for ledger_name_only in ledger_name_only_list:
                    if ledger_name_only.startswith(value.upper()):
                        ledger_name_filter_list.append(ledger_name_only)
    
                ledger_combobox['value'] = ledger_name_filter_list
            ledger_combobox.event_generate('<Down>')

        # Clear Filters
        def clear_func():
            date_var.set("")
            party_name_combobox.set("")
            ledger_combobox.set("")
            self.voucher_edit_treeview()
            
        # Tree View Page Heading Frame
        heading = Frame(self.base_Frame, relief=RAISED, bd=5, bg='light blue')
        heading.place(relx=0, rely=0, relwidth=1.0, relheight=0.1)

        # Tree View Heading Lablel
        Label(heading, text="Edit Voucher", font=("Arial", 25), bg='light blue').pack(expand=True, fill=BOTH, side=BOTTOM)
        # Tree View Frame
        controls_frame = Frame(self.base_Frame, relief=RAISED, bd=5, bg='light blue')
        controls_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)

        Label(controls_frame, text="Date", font=15).grid(row=0, column=0, padx=20, pady=15)
        bill_date = DateEntry(controls_frame, selectmode='day', year=year, date_pattern='dd-mm-y', state='readonly',
                              textvariable=date_var)
        date_var.set("")
        bill_date.grid(row=0, column=1, padx=20, pady=15)

        Label(controls_frame, text="Select Party", font=15).grid(row=0, column=2, padx=20, pady=15)
        party_name_combobox = ttk.Combobox(controls_frame, width=28, values=party_name_only_list)
        party_name_combobox.grid(row=0, column=3, padx=20, pady=15)
        party_name_combobox.bind('<KeyRelease>', party_name_check_input)

        Label(controls_frame, text="Ledger", font=15).grid(row=0, column=4, padx=20, pady=15)
        ledger_combobox = ttk.Combobox(controls_frame, width=28, values=ledger_name_only_list)
        ledger_combobox.grid(row=0, column=5, padx=20, pady=15)
        ledger_combobox.bind('<KeyRelease>', ledger_name_check_input)

        Button(controls_frame, text="Search", font=15, command=search_func).grid(row=0, column=6, padx=20, pady=15)
        Button(controls_frame, text="Clear", font=15, command=clear_func).grid(row=0, column=7, padx=20, pady=15)
        Button(controls_frame, text="Back", font=15, command=back_func).grid(row=0, column=8, padx=20, pady=15)
        self.voucher_edit_treeview()

    # Edit Voucher Tree View Widget
    def voucher_edit_treeview(self, voucher_date="", party_name="", ledger_type=''):
        selected_company_name = '_'.join(self.selected_company[1].split(' '))

        # Fetch all Details
        all_party_list = self.db_Manage_inst.fetch_party_list(selected_company_name)
        all_voucher_list = self.db_Manage_inst.fetch_voucher_list(selected_company_name)
        all_ledger_list = self.db_Manage_inst.fetch_ledger_list(selected_company_name)
        
        # Create Dict to Switch Between ID and Name
        all_party_dict = {party[1]: party[0] for party in all_party_list}
        all_party_dict_id = {party[0]: party[1] for party in all_party_list}
        all_ledger_dict = {ledger[1]: ledger[0] for ledger in all_ledger_list}
        all_ledger_dict_id = {ledger[0]: ledger[1] for ledger in all_ledger_list}
        
        filter_vouchers = []
        # If Date, Party and Ledger Filter set
        if voucher_date and party_name and ledger_type:
            for voucher in all_voucher_list:
                date_bool = voucher[1] == voucher_date
                party_bool = voucher[2] == all_party_dict.get(party_name)
                ledger_bool = voucher[3] == all_ledger_dict.get(ledger_type)
                if date_bool and party_bool and ledger_bool:
                    filter_vouchers.append(list(voucher))
                    
        # If Date and Party Filter set
        if voucher_date and party_name :
            for voucher in all_voucher_list:
                date_bool = voucher[1] == voucher_date
                party_bool = voucher[2] == all_party_dict.get(party_name)
                if date_bool and party_bool:
                    filter_vouchers.append(list(voucher))
                    
        # If Party and Ledger Filter set
        if party_name and ledger_type:
            for voucher in all_voucher_list:
                party_bool = voucher[2] == all_party_dict.get(party_name)
                ledger_bool = voucher[3] == all_ledger_dict.get(ledger_type)
                if party_bool and ledger_bool:
                    filter_vouchers.append(list(voucher))
                    
        # If Date and Ledger Filter set
        if voucher_date and ledger_type:
            for voucher in all_voucher_list:
                date_bool = voucher[1] == voucher_date
                ledger_bool = voucher[3] == all_ledger_dict.get(ledger_type)
                if date_bool and ledger_bool:
                    filter_vouchers.append(list(voucher))
                    
        # If Date Filter only
        elif voucher_date:
            for voucher in all_voucher_list:
                if voucher[1] == voucher_date:
                    filter_vouchers.append(list(voucher))
                    
        # If Party Filter Only
        elif party_name:
            for voucher in all_voucher_list:
                if voucher[2] == all_party_dict.get(party_name):
                    filter_vouchers.append(list(voucher))
                    
        # If Ledget filter Only
        elif ledger_type:
            for voucher in all_voucher_list:
                if voucher[3] == all_ledger_dict.get(ledger_type):
                    filter_vouchers.append(list(voucher))
                    
        # No Filter Set Then Show All Data
        else:
            for voucher in all_voucher_list:
                filter_vouchers.append(list(voucher))
        
        for index, voucher in enumerate(filter_vouchers):
            voucher[2] = all_party_dict_id.get(voucher[2])
            voucher[3] = all_ledger_dict_id.get(voucher[3])
            filter_vouchers[index] = voucher

        # Tree View Headings
        column_heading = ['Voucher Date', 'Party Name', 'Ledger Type', 'Amount', 'Voucher Type', 'Notes']

        # Tree View Frame
        tree_frame = Frame(self.base_Frame, bd=5, bg='light blue')
        tree_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.7)

        # Tree View
        tree_view = ttk.Treeview(tree_frame,
                                 columns=column_heading,
                                 show='headings',
                                 height=8,
                                 selectmode='browse')

        # Tree View Column Settings
        for index, head in enumerate(column_heading, start=1):
            tree_view.column(f'#{index}', anchor=CENTER, minwidth=0, width=190, stretch=NO)
            tree_view.heading(f'#{index}', text=head)

        # Tree View Data Insert
        for index, voucher in enumerate(filter_vouchers, start=1):
            party = [data.split('\n')[0] if isinstance(data, str) else data for data in voucher]
            tree_view.insert('', 'end', text=f'{index}', values=voucher[1:])

        # Vertical Scroll Bar Settings
        tree_v_scroll_bar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_view.yview)
        tree_view.configure(yscrollcommand=tree_v_scroll_bar.set)
        tree_v_scroll_bar.pack(side=RIGHT, fill=BOTH)

        tree_view.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # Double click to Open Company
        def double_click(event):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'cell':
                # Get The Reference of Selected Item
                item = tree_view.selection()[0]
        
                # Get The Values of Selected Item
                selection = tree_view.item(item, 'values')[0]
        
                # Get the real data from DB including ID
                for voucher in all_voucher_list:
                    if voucher[1] == selection:
                        self.selected_voucher = voucher  # Full Data from Party Lists
                self.destroy_base()  # Clear Window
                self.add_voucher_widget()  # Create Party Widget used to Edit Too

        # Bind Tree View for Double Click
        tree_view.bind('<Double-1>', double_click)

        # Insert Note Below the Tree View How it works
        # Tree View Page Note Frame
        bottom_frame = Frame(self.base_Frame, relief=RAISED, bd=2, bg='light blue')
        bottom_frame.place(relx=0, rely=0.9, relwidth=1.0, relheight=0.1)

        note = "Note: Double Click to Edit The Bill"
        note_label = Label(bottom_frame, text=note, font=15, bg='light blue', anchor=CENTER)
        note_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
    
    # # Destroy Widgets Area
    # Destroy Base Frame widgets
    def destroy_base(self):
        for widget in self.base_Frame.winfo_children():
            if widget.winfo_name().startswith('!entry'):
                widget.delete(0, END)
            if widget.winfo_name().startswith('!combobox'):
                widget.delete(0, END)
            if widget.winfo_name().startswith('!text'):
                widget.delete('1.0', END)
            widget.destroy()
    
    # Destroy Menu Bar Widget Except File Menu
    def destroy_menu_bars(self):
        # Remove All Items Menu Except File Menu(Index 1)
        self.menubar.delete(2, END)
    
    # # Delete Data Area
    # Delete Company
    def delete_company(self):
        details = f"If you Continue with Delete You will \nLoose all Data Entered in " \
                  f"The Company {self.selected_company[1]}" \
                  f"\n\nDo You Wnt To Continue?"
        if messagebox.askyesno("Do you Really Want to Delete Company?", details):
            if self.db_Manage_inst.delete_company(self.selected_company):
                messagebox.showinfo("Company Removed Successfully", f"Company {self.selected_company[1]}"
                                                                    f"Removed From Data Base Successfully")
        
        self.selected_company = []
        self.destroy_base()
        
        # Get All Company Data
        all_company_data = self.db_Manage_inst.fetch_company_list()
        self.file_menu.entryconfig('Create Company', state=NORMAL)
        self.file_menu.entryconfig('Exit', state=NORMAL)
        if all_company_data:  # Check Company Name Available
            self.file_menu.entryconfig('Open Company', state=NORMAL)
    
    # Delete Ledger
    def delete_ledger(self):
        company_name = '_'.join(self.selected_company[1].split(' '))
        all_voucher_list = self.db_Manage_inst.fetch_voucher_list(company_name)

        ledger_used = False
        for voucher in all_voucher_list:
            if voucher[3] == self.selected_ledger[0]:
                ledger_used = True
        if not ledger_used:
            if self.db_Manage_inst.delete_ledget(company_name, self.selected_ledger[0]):
                messagebox.showinfo("Ledger Deleted ", f"Ledger '{self.selected_ledger[1]}' Deleted Successfully")
                self.selected_ledger = []
                self.destroy_base()
                self.load_other_menu_bars()
            else:
                messagebox.showerror("Ledger Not Deleted", "Ledger Deletion Failed")
        else:
            messagebox.showerror("Ledger Is In Use",
                                 f"First Delete All Vouchers Attached with '{self.selected_ledger[1]}'")
    
    # Delete Party If No Bill Attached
    def delete_party(self):
        company_name = '_'.join(self.selected_company[1].split(' '))
        all_bill_list = self.db_Manage_inst.fetch_bill_list(company_name)
        all_voucher_list = self.db_Manage_inst.fetch_voucher_list(company_name)
        print(self.selected_party)
        party_used = False
        for bill in all_bill_list:
            if bill[2] == self.selected_party[0]:
                party_used = True
        for voucher in all_voucher_list:
            if voucher[2] == self.selected_party[0]:
                party_used = True
        if not party_used:
            if self.db_Manage_inst.delete_party(company_name, self.selected_party[0]):
                messagebox.showinfo("Party Deleted ", f"Party '{self.selected_party[1]}' Deleted Successfully")
                self.selected_party = []
                self.destroy_base()
                self.load_other_menu_bars()
            else:
                messagebox.showerror("Party Not Deleted", "Party Deletion Failed")
        else:
            messagebox.showerror("Party Attached Vouchers",
                                 f"Party '{self.selected_party[1]}' is attached with Bills and Vouchers "
                                 f"First Delete Them All")
    
    # Delete Bill
    def delete_bill(self):
        company_name = '_'.join(self.selected_company[1].split(' '))
        bill_id = self.selected_bill[0]
        if self.db_Manage_inst.delete_bill(company_name, bill_id):
            messagebox.showinfo("Bill Deleted ", "Bill Deleted Successfully")
            self.selected_bill = []
            self.destroy_base()
            self.load_other_menu_bars()
        else:
            messagebox.showerror("Bill Not Deleted", "Bill Deletion Failed")
    
    # Delete Voucher
    def delete_voucher(self):
        company_name = '_'.join(self.selected_company[1].split(' '))
        voucher_id = self.selected_voucher[0]
        if self.db_Manage_inst.delete_voucher(company_name, voucher_id):
            messagebox.showinfo("Voucher Deleted ", "Voucher Deleted Successfully")
            self.selected_voucher = []
            self.destroy_base()
            self.load_other_menu_bars()
        else:
            messagebox.showerror("Voucher Not Deleted", "Voucher Deletion Failed")
            
    # Close Current Company
    def close_company(self):
        self.destroy_base()
        
        # Disable Create and Open Company Menus
        self.file_menu.entryconfig('Create Company', state=NORMAL)
        self.file_menu.entryconfig('Open Company', state=NORMAL)
        self.file_menu.entryconfig('Close Company', state=DISABLED)
        self.file_menu.entryconfig('Exit', state=NORMAL)
        
        # Remove Company Name from Window Title
        self.root.title(f"{self.APP_NAME}")
        
        # Remove Menu Bar Except File Menu
        self.destroy_menu_bars()
        
        # Reset Selection
        self.selected_company = []
        self.selected_ledger = []
        self.selected_party = []
        self.selected_bill = []
        self.selected_voucher = []
    
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    window = Window()
    window.run()
