from tkinter import *


class Window:
    # Initialize main Window
    root = Tk()
    
    # Detect screen size
    W = root.winfo_screenwidth()
    H = root.winfo_screenheight()
    
    # Set window Size
    # root.geometry(f"{W}x{H}+0+0")
    
    # Maximize window
    root.state('zoomed')
    
    # Creating Menubar
    menubar = Menu(root)

    # Adding File Menu and commands
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Create Company', command=None)
    file_menu.add_command(label='Open Company', command=None)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=root.destroy)

    # Adding Items
    add_items_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Add Items', menu=add_items_menu)
    add_items_menu.add_command(label='Type of Accounts', command=None)
    add_items_menu.add_command(label='Party', command=None)
    add_items_menu.add_command(label='Bill', command=None)
    add_items_menu.add_command(label='Receipt', command=None)
    
    # Editing Items
    edit_items_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit Items', menu=edit_items_menu)
    edit_items_menu.add_command(label='Type of Accounts', command=None)
    edit_items_menu.add_command(label='Party', command=None)
    edit_items_menu.add_command(label='Bill', command=None)
    edit_items_menu.add_command(label='Receipt', command=None)
    
    # Report View & Download
    report_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Reports', menu=report_menu)
    report_menu.add_command(label='Type of Accounts', command=None)
    edit_items_menu.add_command(label='Party', command=None)
    edit_items_menu.add_command(label='Bill', command=None)
    edit_items_menu.add_command(label='Receipt', command=None)
    
    def __init__(self):
        # Title
        self.root.title("Day Book Software")
        # display Menu
        self.root.config(menu=self.menubar)
    
    def run(self):
        self.root.mainloop()
        
if __name__ == '__main__':
    window = Window()
    window.run()