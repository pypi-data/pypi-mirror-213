import pytest
from src.facebookApi import get

def test_get_data1():
    response = get('email,name')
    assert type (response) is list

def test_get_data2():
    response = get('gender,birthday')
    assert type (response) is list