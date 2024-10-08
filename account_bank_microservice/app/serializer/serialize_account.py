def Decode_account(data)-> dict:
    return {
        "account_name":data['account_name'],
        "account_balance":data['account_balance'],
        "id_account":data['id_account'],
        "_id":str(data['_id'])
    }

def Decode_account_list(x)-> list:
    return [Decode_account(data) for data in x]