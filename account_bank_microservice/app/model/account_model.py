from pydantic import BaseModel

class AccountModel(BaseModel):
    id_account : int = None
    account_name:str
    account_balance:float
    
    def serializer(data)->dict:
        return(
            {
                "id_account":data['id_account'],
                "account_name":data['account_name'],
                "account_balance":data['account_balance']
            }
        )