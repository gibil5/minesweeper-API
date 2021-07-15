import pytest  

def x_test_username(user_1):
    print('test_username')
    assert user_1.username == 'test-user'

def x_test_new_user(new_user):
    print('test_new_user')
    print(new_user.first_name)
    assert new_user.first_name == 'MyName'
