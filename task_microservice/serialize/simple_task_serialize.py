
def Decode_simple_task(data)-> dict:
    return {
        "task_name":data['task_name'],
        "task_date_begin":data['task_date_begin'],
        "task_date_ending":data['task_date_ending'],
        "_id":str(data['_id'])
    }

def Decode_simple_task_list(x)-> list:
    return [Decode_simple_task(data) for data in x]