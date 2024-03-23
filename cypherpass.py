import sys
import re
import pickle
import getpass
import random
import os
import hashlib
import secrets

class PasswordDatabase:
    #  Init the database
    def __init__(self, filename):
        self.passwords = {}
        self.key = ""
        self.filename = filename
        self.passwords["_hash"] = ""
        self.passwords["_salt"] = ""

    def save_key(self):
        hashed, salt = hash_password(self.key, None)
        self.passwords["_hash"] = hashed
        self.passwords["_salt"] = salt

    def check_key(self):
        input_hash, _ = hash_password(self.key, self.passwords["_salt"])
        return input_hash == self.passwords["_hash"]

password_database = PasswordDatabase("")

def main():
    ### Check if it has argument
    if len(sys.argv) == 1:
        main_menu()
    ### Check each argument
    else:
        arguments_process()

## Business Functions
def open_database(file, new, replace, key):
    ## File name is not valid
    if not (file.endswith(".pkl")):
        raise ValueError
    ## trying to create new file, but file does exist
    if os.path.exists(file) and replace != 'yes' and new:
        raise FileExistsError
    if (not os.path.exists(file)) and new == False:
        raise FileNotFoundError
    password_database.filename = file
    password_database.key = key
    if os.path.exists(file) and new == False:
        try:
            with open(file, 'rb') as my_file:
                password_database.passwords =  pickle.load(my_file)
        except:
            raise TypeError
        if password_database.check_key() == False:
            raise SystemError
    if os.path.exists(file) == False:
        f = open(file, "x")
        password_database.passwords = {}
    password_database.save_key()
    with open(password_database.filename, 'wb') as my_file:
        pickle.dump(password_database.passwords, my_file)

def update_passwords(tag, action, password):
    if (tag in ["_hash", "_salt"]):
        raise SystemError
    if action in ["remove", "update"] and tag not in password_database.passwords.keys():
        raise FileNotFoundError
    if action in ["add"] and tag in password_database.passwords.keys():
        raise FileExistsError
    if action == "remove":
        password_database.passwords.pop(tag)
    else:
        password_database.passwords[tag] = encode(password, password_database.key)
    with open(password_database.filename, 'wb') as my_file:
        pickle.dump(password_database.passwords, my_file)

def view_tags():
    tags_to_print = ""
    for x in password_database.passwords.keys():
        if not (x in ["_hash", "_salt"]):
            tags_to_print = tags_to_print + "\n" + x
    return tags_to_print

def view_tag_pass(tag):
    if tag in password_database.passwords.keys() and  (tag not in ["_hash", "_salt"]):
        return decode(password_database.passwords[tag], password_database.key)
    else:
        raise ValueError

## Auxiliary function
# Encode a string with another string
def encode(to_encode, passkey):
    encoded = ''
    for eachletter in range(len(to_encode)):
        encoded += chr(ord(to_encode[eachletter]) + ord(passkey[eachletter - (len(passkey) * int(eachletter/len(passkey)))]))
    return encoded

# Encode a string with another string
def decode(to_decode, passkey):
    decoded = ''
    for eachletter in range(len(to_decode)):
        decoded += chr(ord(to_decode[eachletter]) - ord(passkey[eachletter - (len(passkey) * int(eachletter/len(passkey)))]))
    return decoded

## Generates a random password between 12 and 16 characters containing numbers / letters
def random_password():
    password = ''
    for _ in range(random.randint(12, 16)):
        password += chr(random.choice(list(range(48, 57, 1)) + list(range(65, 90, 1)) + list(range(97, 122, 1))))
    return password

## define hash password
def hash_password(password, salt):
    if salt is None:
        salt = secrets.token_hex(16)  # Generate a 16-byte (32-character) random salt
    password_salt = password + salt
    hashed_password = hashlib.sha256(password_salt.encode()).hexdigest()
    return hashed_password, salt

## Verify the password with hash
def verify_password(input_password, stored_hash, salt):
    input_hash, _ = hash_password(input_password, salt)
    return input_hash == stored_hash

## Menu Calls
### Execute program without argument
def main_menu():
    ### Open main menu
    while True:
        print("""Password management

1 - Create a new password database
2 - Open a password database
3 - Exit
              """)
        match input("Choose your option: "):
            case '1':
                try:
                    menu_open(True)
                except:
                    pass
            case '2':
                try:
                    menu_open(False)
                except:
                    pass
            case '3':
                sys.exit("Exit")
            case _:
                print("Invalid Option.")

def menu_open(new):
    while True:
        try:
            file = input("Type your file name (.pkl): ")
        except:
            break
        replace = "no"
        if os.path.exists(file) and new:
            if input("File selected exist. Do you want to replace it? (yes or no) ") == "yes":
                replace = "yes"
            else:
                raise TypeError
        if (not os.path.exists(file)) and new == False:
            if input("File selected does not exist. Do you want to create it? (yes or no) ") == "yes":
                new = True
            else:
                break
        try:
            open_database(file, new, replace, getpass.getpass("Password: "))
            passwords_menu()
        except ValueError:
            print("File name is not valid.")
            break
        except TypeError:
            print("File is not valid.")
            break
        except SystemError:
            print("Password is invalid.")
            break

def passwords_menu():
    ### Menu to list the passwords
    while True:
        print(password_database.filename + " - Password list.")
        print("1 - Add password")
        print("2 - Remove password")
        print("3 - Update password")
        print("4 - Print password")
        print(view_tags())
        print("")
        print("5 - Exit")
        a = input("Choose your option: ")
        if a == "1":
            update_menu("add")
        elif a == "2":
            update_menu("remove")
        elif a == "3":
            update_menu("update")
        elif a == "4":
            tag = input("Type the tag to be printed: ")
            try:
                print(view_tag_pass(tag))
                print("Press any key to continue...")
                input()
                os.system('clear')
            except:
                print("Tag does not exist.")
        elif a == "5":
            sys.exit()
        else:
            print("Invalid option.")

def update_menu(action):
    while True:
        try:
            passwordname = input("Type the tag to " + action + ": ")
        except:
            break
        if action in ["add", "update"]:
            password = getpass.getpass("Password (or enter for Random password): ")
            if len(password) == 0:
                password = random_password()
        else:
            password = ""
        try:
            update_passwords(passwordname, action, password)
            break
        except FileExistsError:
            print("Tag already exist.")
            break
        except FileNotFoundError:
            print("Tag does not exist.")
            break
        except SystemError:
            print("Tag not valid.")
            break

## Arguments interpretation
def arguments_process():
    # Default Dictionary to deal with argument
    argument = {"help": "False"
                , "key": ""
                , "tag": ""
                , "password": ""
                , "filename": ""
                , "replace": False
                , "new": False
                , "view_tag": "False"
                , "update": "False"
                , "action": ""
                , "view_password": "False"}
    argument = check_args_input(argument)
    if argument["action"] == "exit":
        sys.exit("Argument " + argument["update"] + " is invalid. Use -h for help.")
    elif argument["action"] == "exit invalid":
        print("Invalid usage. Use -h for help.")
    process_args(argument)

def process_args(argument):
    if argument["help"] == "True":
        help_print()
    if (argument["filename"] == ""):
        sys.exit("Filename Not Defined. Use -h for help.")
    if argument["key"] == "":
        sys.exit("Key Password is missing. Use -h for help.")
    try:
        open_database(argument["filename"], argument["new"], argument["replace"], argument["key"])
    except FileNotFoundError:
        sys.exit(argument["filename"] + " does not exist.")
    except ValueError:
        sys.exit(argument["filename"] + " name is not valid. It shall be .pkl. Use -h for help.")
    except TypeError:
        sys.exit(argument["filename"] + " is not valid.")
    except FileExistsError:
        sys.exit(argument["filename"] + " already exists. Use -h for help.")
    except SystemError:
        sys.exit("Password is incorrect. Use -h for help.")
    if argument["view_tag"] == "True":
        open_database(argument["filename"], False, False, argument["key"])
        print(view_tags())
        sys.exit()
    if argument["update"] == "True" and argument["action"] == "remove":
        try:
            update_passwords(argument["tag"], "remove", argument["password"])
        except FileExistsError:
            sys.exit("Tag already exist.")
        except FileNotFoundError:
            sys.exit("Tag does not exist.")
    if argument["view_password"] == "True":
        try:
            print(argument["tag"] + " : " + view_tag_pass(argument["tag"]))
            print("Press any key to continue...")
            input()
            os.system('clear')
        except:
            sys.exit("Tag does not exist.")
        sys.exit()
    if argument["password"] == "" and argument["action"] != "remove" and argument["action"] != "":
        sys.exit("Missing password. Use -h for help.")
    if argument["update"] == "True":
        try:
            update_passwords(argument["tag"], argument["action"], argument["password"])
        except FileExistsError:
            sys.exit("Tag already exist.")
        except FileNotFoundError:
            sys.exit("Tag does not exist.")

def check_args_input(args):
    argument = args
    count_op = 0
    for arg in range(1, len(sys.argv)):
        if matches:=re.search("^(-h)", sys.argv[arg]):
            argument["help"] = "True"
        elif matches:=re.search("^(-n)", sys.argv[arg]):
            argument["new"] = True
        elif matches:=re.search("^(-R)", sys.argv[arg]):
            argument["replace"]  = True
        elif matches:=re.search("^(-db:)(.*)", sys.argv[arg]):
            argument["filename"] = matches[2]
        elif matches:=re.search("^(-l)", sys.argv[arg]):
            argument["view_tag"] = "True"
            count_op = count_op + 1
        elif matches:=re.search("^(-k:)(.*)", sys.argv[arg]):
            argument["key"] = matches[2]
        elif matches:=re.search("^(-t:)(.*)", sys.argv[arg]):
            argument["tag"] = matches[2]
        elif matches:=re.search("^(-v)", sys.argv[arg]):
            argument["view_password"] = "True"
            count_op = count_op + 1
        elif (matches:=re.search("^(-a)", sys.argv[arg])):
            argument["update"] = "True"
            argument["action"] = "add"
            count_op = count_op + 1
        elif matches:=re.search("^(-rm)", sys.argv[arg]):
            argument["update"] = "True"
            argument["action"] = "remove"
            count_op = count_op + 1
        elif matches:=re.search("^(-u)", sys.argv[arg]):
            argument["update"] = "True"
            argument["action"] = "update"
            count_op = count_op + 1
        elif matches:=re.search("^(-p:)(.*)", sys.argv[arg]):
            argument["password"] = matches[2]
        elif matches:=re.search("^(-pr)", sys.argv[arg]):
            argument["password"] = random_password()
        else:
            argument["action"] = "exit"
            argument["update"] = arg
            break
    if count_op > 1:
        argument["action"] = "exit invalid"
    return argument

def help_print():
    ### Print help
    print("""Help - Password Database
usage:  python cypherpass.py
            it will open an interactive menu to manage the passwords
        python cypherpass.py [option]
-h                  : List the usage option.
-n                  : Create a new database defined on -db:filename. If not included, filename will be assumed as existent.
-R                  : It will replace an existent file when creating a new database without confirmation.
-db:filename.pkl    : Define the filename to be used.
-l                  : List all password tags.
-k:key              : add the "key" to decode the passwords.
-t:tag              : select a specific tag.
-v                  : view the password of a specific tag.
-a                  : add a new password with a defined tag.
-rm                 : remove the defined tag.
-u                  : update the defined tag. It needs -p:password.
-p:password         : password definition for add/update.
-pr                 : use a random password

example:
          python cypherpass.py -h
          python cypherpass.py -n -R -db:mypassword.pkl
          python cypherpass.py -db:mypassword.pkl -k:key -l
          python cypherpass.py -db:mypassword.pkl -k:key -a -t:Gmail -p:mypassword
                  """)
    sys.exit()

if __name__ == "__main__":
    main()
