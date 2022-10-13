from datetime import datetime
from string import ascii_letters, digits
import re


# Name Validation
def name_check(name):
    if len(name) < 3:
        return False  # Name Must contain at least 3 letters
    else:
        valid_letters = ascii_letters + digits + ' '  # All Letters Numbers and (Space) are allowed
        for letter in name:
            if letter not in valid_letters:
                return False  # Any Character not in Valid Letter means invalid Name
        return True  # All Characters in the Valid Letter List Means Valid Name


# Address Validation
def address_check(address):
    if len(address) < 5:
        return False  # Address Must Have at least 5 Character Long
    else:
        valid_letters = ascii_letters + digits + '.' + ',' + '\n' + '-' + '_' + '(' + ')' + ' '  # Valid Character list
        for letter in address:
            if letter not in valid_letters:
                return False  # Any Character not in Valid List Means Invalid Address
        return True  # All Character in Valid List means Valid Address


# Check GSTN and State
def gstn_validate(state, gstn):
    if not gstn:
        return True  # If GST Number not available and State Has a Default Value So It Is Good to go
    if state.split('-')[0] != gstn[:2]:
        return False  # If GST Number's first 2 character denote state, and it doesn't match means Error
    check = gstn[-1]  # Last Character of GSTN is Checksum
    gst = gstn[:-1]  # All other Characters are Split
    l = [int(c) if c.isdigit() else ord(c) - 55 for c in gst]  # GSTN Validation Convert all Letters A start with 10
    l = [val * (ind % 2 + 1) for (ind, val) in list(enumerate(l))]
    l = [(int(x / 36) + x % 36) for x in l]
    csum = (36 - sum(l) % 36)
    csum = str(csum) if (csum < 10) else chr(csum + 55)
    return True if (check == csum) else False


# PIN Code Validation
def pin_validation(pin):
    regex = re.compile(r'^[1-9][0-9]{5}$')  # First Didit 1 to 8, next 5 digits 0 to 9
    return re.fullmatch(regex, pin)


# Phone Number Validation
def phone_validate(mob):
    regex = re.compile(r'\d{10}')  # 10 Digit Number
    return re.fullmatch(regex, mob)


#  Email Validation
def email_validation(email):
    regex = re.compile(r'([a-z0-9]+[.-_])*[a-z0-9]+@[a-z0-9-]+(\.[a-z]{2,})+')
    return re.fullmatch(regex, email)


# Amount Validation
def amount(amount):
    if amount:
        try:
            amount = float(amount)
            return True
        except:
            return False
    return False
    

# Notes Validation
def notes_check(notes):
    if not notes:
        return True  # Notes May Be Blank
    else:
        valid_letters = ascii_letters + digits + '.' + ',' + '\n' + '-' + '_' + '(' + ')' + ' '  # Valid Character list
        for letter in notes:
            if letter not in valid_letters:
                return False  # Any Character not in Valid List Means Invalid Address
        return True  # All Character in Valid List means Valid Address


    
