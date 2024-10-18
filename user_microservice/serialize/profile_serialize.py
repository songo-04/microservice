
def Decode_profile(data)-> dict:
    return {
        "name":data['name'],
        "surname":data['surname'],
        "address":data['address'],
        "_id":str(data['_id']),
        "email":data['email']
    }

def Decode_profiles(x)->list:
    return [Decode_profile(data) for data in x]

def Decode_user(data)-> dict:
    return {
        "user_name":data['user_name'],
        "user_email":data['user_email'],
    }