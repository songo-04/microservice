from pydantic import BaseModel

class SimpleTaskModel(BaseModel):
    task_name : str
    task_date_begin : str
    task_date_ending : str
    task_desc : str
    userId : str = None
    
class SimpleTaskModelUpdate(BaseModel):
    task_name : str = None
    task_date_begin : str = None
    task_date_ending : str = None
    task_desc : str = None 