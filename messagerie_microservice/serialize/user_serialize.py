
def Decode_user(data)-> dict:
    return {
        "user_name":data['user_name'],
        "user_email":data['user_email'],
    }
    
def Decode_user_admin(data)->dict:
    return {
        "user_name":data['user_name'],
        "user_email":data['user_email'],
        "user_password":data['user_password'],
        "_id":str(data['_id']),
    }
    
def Decode_users_admin(x)-> list:
    return [Decode_user_admin(data) for data in x]  
  
def Decode_users(x)-> list:
    return [Decode_user(data) for data in x]