##### 用户表存储系统
user_storage = {}

def add_user(user_id, user_info):
    # Code to add user information to the storage
    user_storage[user_id] = user_info

def get_user(user_id):
    # Code to retrieve user information from the storage
    return user_storage.get(user_id)

def get_all_users():
    # Code to retrieve all user information from the storage
    return user_storage

def delete_user(user_id):
    # Code to delete user information from the storage
    user_storage.pop(user_id, None)