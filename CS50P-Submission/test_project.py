import pytest
import sys
import project
import os

# Test Class
password_database = project.PasswordDatabase("")

def delete_files():
    os.remove("wrong.pkl")
    os.remove("test.pkl")

def test_check_class_PasswordDatabase():
    assert password_database.key == ""
    assert password_database.filename == ""
    assert "_hash" in password_database.passwords.keys()
    assert "_salt" in password_database.passwords.keys()

def test_save_key():
    password_database.key = "test"
    password_database.save_key()
    input_hash, _ = project.hash_password(password_database.key, password_database.passwords["_salt"])
    assert input_hash == password_database.passwords["_hash"]

def test_check_key():
    password_database.key = "wrong"
    if password_database.check_key():
        assert False
    else:
        assert True
    password_database.key = "test"
    assert password_database.check_key()

password_database = project.PasswordDatabase("")

# Testing Auxiliary functions
# encode(to_encode, passkey) and decode(to_decode, passkey)
# random_password()
# hash_password(password, salt) and verify_password(input_password, stored_hash, salt)

def test_encode():
    assert project.encode("aaaa", "a") == chr(97+97) + chr(97+97) + chr(97+97) + chr(97+97)
    assert project.encode("aaaa", "b") == chr(97+98) + chr(97+98) + chr(97+98) + chr(97+98)
    assert project.encode("aaaa", "ba") == chr(97+98) + chr(97+97) + chr(97+98) + chr(97+97)

def test_decode():
    assert project.decode(chr(97+97) + chr(97+97) + chr(97+97) + chr(97+97), "a") == "aaaa"
    assert project.decode(chr(97+98) + chr(97+98) + chr(97+98) + chr(97+98), "b") == "aaaa"
    assert project.decode(chr(97+98) + chr(97+97) + chr(97+98) + chr(97+97), "ba") == "aaaa"

def test_random_password():
    password1 = project.random_password()
    password2 = project.random_password()
    password3 = project.random_password()
    assert password1 != password2
    assert password2 != password3
    assert len(password1) >= 12
    assert len(password1) <= 16
    assert len(password2) >= 12
    assert len(password2) <= 16
    assert len(password3) >= 12
    assert len(password3) <= 16

# Testing business functions
# open_database(file, new, replace, key)
def test_open_database():
    # new file with wrong extention
    try:
        project.open_database("test.xxx", True, "no", "test")
        assert False
    except ValueError:
        assert True
    # creating a new file
    try:
        project.open_database("test.pkl", True, "yes", "test")
        assert True
    except ValueError:
        assert False
    # creating a new file, but the file exist
    try:
        project.open_database("test.pkl", True, "no", "test")
        assert False
    except FileExistsError:
        assert True
    # creating a new file and replacing
    try:
        project.open_database("test.pkl", True, "yes", "test")
        assert True
    except FileExistsError:
        assert False
    # open file, but it does not exist
    try:
        project.open_database("test2.pkl", False, "no", "test")
        assert False
    except FileNotFoundError:
        assert True
    # open file, wrong password
    try:
        project.open_database("test.pkl", False, "no", "wrong")
        assert False
    except SystemError:
        assert True
    # open file, wrong type
    with open("wrong.pkl", "x") as my_file:
        my_file.write("Add some text")
    try:
        project.open_database("wrong.pkl", False, "no", "wrong")
        assert False
    except TypeError:
        assert True
    # open file success
    try:
        project.open_database("test.pkl", False, "no", "test")
        assert True
    except SystemError:
        assert False
    delete_files()

# update_passwords(rotule, action, password)
def test_update_passwords():
    ## Add password
    try:
        project.update_passwords("email", "add", "password")
        assert project.view_rotule_pass("email")=="password"
    except SystemError:
        assert False
    ## Add failing
    try:
        project.update_passwords("email", "add", "password")
        assert False
    except FileExistsError:
        assert True
    ## Update password
    try:
        project.update_passwords("email", "update", "password2")
        assert project.view_rotule_pass("email")=="password2"
    except SystemError:
        assert False
    ## Update not existent
    try:
        project.update_passwords("email2", "update", "password2")
        assert False
    except FileNotFoundError:
        assert True
    ## remove password
    try:
        project.update_passwords("email", "remove", "")
        assert True
    except SystemError:
        assert False
    ## remove not existent
    try:
        project.update_passwords("email", "remove", "")
        assert False
    except FileNotFoundError:
        assert True
