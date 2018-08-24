from tweeter.authorizer import Authorizer
import pytest
import os

def test_has_password():
    auth = Authorizer("test")

    file = open(auth.path + "/test.enc", 'w+')
    file.write("test, test, test,test")

    output = auth.has_password()
    os.remove(auth.path + "/test.enc")

    assert output == True

def test_user_exists():
    auth = Authorizer("test")

    file = open(auth.path + "/test.csv", 'w+')
    file.write("test, test, test,test")

    output = auth.user_exists()
    os.remove(auth.path + "/test.csv")

    assert output == True

def test_split_keys():
    keys = [1, 4, 5, 6]
    auth = Authorizer()

    assert sum(auth.split_keys(keys)) == 16

