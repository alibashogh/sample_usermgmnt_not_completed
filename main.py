from fastapi import FastAPI, Path
from pymongo import MongoClient
from pprint import pprint

app = FastAPI()

client = MongoClient('localhost', 27017)
db = client['mydb']
collection = db['users']
cursor = collection.find({})
users = db.users

# user = {
#         'national_id': 332334,
#         'username': 'hamed',
#         'password': 54321,
#         'name': 'reza',
#         'last_name': 'babaei',
#         'email': 'example@gmail.com',
#         'phone': 912000000
#        }
# user_id = users.insert_one(user).inserted_id


samples = []
for user in cursor:
    user_id = user['_id']
    user['_id'] = str(user_id)
    samples.append(user)


@app.get('/')
async def root():
    return samples


@app.get('/user/{username}')
async def get_specific_user_by_username(username: str):
    return_value = {}
    for item in samples:
        if item['username'] == username:
            return_value = {
                'national_id': item['national_id'],
                'username': item['username'],
                'password': item['password'],
                'name': item['name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'phone': item['phone']
            }
        else:
            return_value = {"request_failed": "No user with this username"}
            return return_value
    return return_value


@app.get('/user/conn/{national_id}')
async def get_connections_by_national_id(
        national_id: int = Path(..., title='communication to user', gt=0)

):
    return_value = {}
    for item in samples:
        if item['national_id'] == national_id:
            return_value = {
                'phone': item['phone'],
                'email': item['email']
            }
        else:
            return_value = {"request_failed": "No user with this national_id"}
            return return_value
    return return_value


@app.get('/user/del/{national_id}&{sign}')
async def operation_on_users(national_id: int, sign: str):
    if sign.upper() == 'D':
        delete_query = {'national_id': national_id}
        collection.delete_one(delete_query)
        return {'delete_operation': 'succeed'}
    # elif sign.upper() == 'I':


