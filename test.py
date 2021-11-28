# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
# db = client['mydb']
# collection = db['users']
# user = {
#         'national_id': 10,
#         'username': 'k10',
#         'password': 54321,
#         'name': 'reza',
#         'last_name': 'babaei',
#         'email': 'example@gmail.com',
#         'phone': 912000000
#        }
# user_id = collection.insert_one(user).inserted_id
# print(user_id)

# national_code = '4579419618'
# while len(national_code) < 10:
#     national_code = '0' + national_code
#
# national_list = []
# for i in national_code:
#     national_list.append(int(i))
#
# national_list.reverse()
# sign_digit = national_list.pop(0)
# multiple_list = []
# counter = 2
# for digit in national_list:
#     multiple_list.append(digit * counter)
#     counter += 1
#
# sum_multiple_list = sum(multiple_list)
# num = sum_multiple_list % 11
#
# if num >= 2:
#     result = 11 - num
#     if result == sign_digit:
#         print('your national code is valid')
#     else:
#         print('your national code is invalid')
# else:
#     print('your national code is valid')








# {
#     "national_id": 1234567892,
#     "username": "k11",
#     "password": 54321,
#     "name": "reza",
#     "last_name": "babaei",
#     "email": "example@gmail.com",
#     "phone": 912000000
# }







