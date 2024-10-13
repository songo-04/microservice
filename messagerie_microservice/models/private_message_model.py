from pydantic import BaseModel # type: ignore
class PrivateMessageModel(BaseModel):
    sender_id:str = None
    receiver_id:str = None
    messages:str
    
def decode_message_private(data)-> dict:
    return{
        "sender_id":data['sender_id'],
        "receiver_id":data['receiver_id'],
        "messages":data['messages'],
        "_id":str(data['_id']),
    }
    
def decode_message_private_list(x)-> list:
    return [decode_message_private(data) for data in x]