from fastapi import FastAPI, Path, Query
from fastapi_pagination import Page, paginate, add_pagination
from pymongo import MongoClient
from pprint import pprint
from pydantic import BaseModel
from typing import Optional

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


def check_national_code(nat_code):
    national_code = str(nat_code)
    while len(national_code) < 10:
        national_code = '0' + national_code
    national_list = []
    for i in national_code:
        national_list.append(int(i))
    national_list.reverse()
    sign_digit = national_list.pop(0)
    multiple_list = []
    counter = 2
    for digit in national_list:
        multiple_list.append(digit * counter)
        counter += 1
    sum_multiple_list = sum(multiple_list)
    num = sum_multiple_list % 11

    if num < 2 and num == sign_digit:
        return {'national_id': 'valid'}
    elif num < 2 and num != sign_digit:
        return {'national_id': 'invalid'}
    else:
        return {'national_id': 'valid'}


samples = []
for user in cursor:
    user_id = user['_id']
    user['_id'] = str(user_id)
    samples.append(user)


class UserIn(BaseModel):
    national_id: int
    username: str
    password: str
    name: str
    last_name: str
    email: str
    phone: str


class UserOut(BaseModel):
    national_id: int
    username: str
    name: str
    last_name: str
    email: str
    phone: str


@app.get('/', response_model=Page[UserOut])
async def root():
    return paginate(samples)

add_pagination(app)


@app.get('/usr/{username}')
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
    return return_value


@app.get('/conn_usr/{national_id}')
async def get_connections_by_national_id(national_id):
    return_value = {}
    for item in samples:
        if item['national_id'] == int(national_id):
            return_value = {
                'phone': item['phone'],
                'email': item['email']
            }
    return return_value


@app.get('/user_op/del/{national_id}')
async def delete_user(national_id: int):
    delete_query = {'national_id': national_id}
    collection.delete_one(delete_query)
    return {'delete_operation': 'succeed'}


@app.post('/user_op/ins/', response_model=UserOut)
async def insert_user(user_in: UserIn):
    print(user_in )
    query = {
        "national_id": user_in.national_id,
        "username": user_in.username,
        "password": user_in.password,
        "name": user_in.name,
        "last_name": user_in.last_name,
        "email": user_in.email,
        "phone": user_in.phone
    }
    collection.insert_one(query)
    return user_in


@app.get('/user/validation/{username}')
async def check_validity_national_code(username):
    for item in samples:
        if item['username'] == username:
            return check_national_code(item['national_id'])
