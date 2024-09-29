from fastapi import APIRouter,HTTPException,status,Depends
from bson import ObjectId

from models.simple_task_model import SimpleTaskModel,SimpleTaskModelUpdate
from config.config import simple_task_collection
from utils.is_auth import is_authenticate
from serialize.simple_task_serialize import Decode_simple_task_list,Decode_simple_task
from utils.verification import is_exist,is_authorize,is_empty

simple_task_route = APIRouter(
    prefix='/api/task/simple'
)

@simple_task_route.post('/')
async def create_simple_task(data : SimpleTaskModel,is_auth : dict=Depends(is_authenticate)):
    userId = is_auth['userId']
    new_task = SimpleTaskModel( 
        task_name = data.task_name,
        task_date_begin = data.task_date_begin,
        task_date_ending = data.task_date_ending,
        task_desc = data.task_desc,
        userId = userId
    )
    new_task = dict(new_task)
    simple_task_collection.insert_one(new_task)
    return {
        "message" : "simple task added",
        "status"  : status.HTTP_201_CREATED
    }

@simple_task_route.get('/')
async def get_all_simple_task(is_auth : dict=Depends(is_authenticate)):
    userId = is_auth['userId']
    simples_tasks = simple_task_collection.find({'userId' : userId})
    is_exist(simples_tasks)
    simples_tasks = Decode_simple_task_list(simples_tasks)
    is_empty(simples_tasks)
    task_list = Decode_simple_task_list(simples_tasks)
    return task_list

@simple_task_route.get('/{_id}')
async def get_one_simple_task(_id : str,is_auth : dict=Depends(is_authenticate)):
    userId = is_auth['userId']
    simple_task  = simple_task_collection.find_one({'_id' : ObjectId(_id)})
    is_exist(simple_task)
    is_authorize(simple_task['userId'],userId)
    return Decode_simple_task(simple_task)

@simple_task_route.patch('/{_id}')
async def update_simple_task(_id : str, data_form : SimpleTaskModelUpdate,is_auth : dict = Depends(is_authenticate)):
   userId = is_auth['userId']
   req = dict(data_form.model_dump(exclude_unset=True))
   simple_task = simple_task_collection.find_one({'_id':ObjectId(_id)})
   is_exist(simple_task)
   is_authorize(simple_task['userId'],userId)
   simple_task_collection.find_one_and_update({"_id":ObjectId(_id)},{"$set":req})
   return {
       "message" : "updated",
       "status"  : status.HTTP_202_ACCEPTED 
   }
@simple_task_route.delete('/{_id}')
async def delete_simple_task(_id : str,is_auth : dict = Depends(is_authenticate)):
   userId = is_auth['userId']
   simple_task = simple_task_collection.find_one({'_id':ObjectId(_id)})
   is_exist(simple_task)
   is_authorize(simple_task['userId'],userId)
   simple_task_collection.find_one_and_delete({'_id':ObjectId(_id)})
   return {
        "message":"deleted !!!",
        "status":status.HTTP_200_OK
    }