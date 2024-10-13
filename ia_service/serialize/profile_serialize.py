
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