# # Example of a JWT in Python using PyJWT
# import jwt
# import datetime

# # Secret key to sign the token
# SECRET_KEY = 'mysecret'

# # Data to encode
# payload = {
#     'sub': 'user_id_123',
#     'name': 'John Doe',
#     'iat': datetime.datetime.utcnow(),
#     'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
# }

# # Create JWT
# token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# print(token)

# or Operator test
# Id = 222
# profile = "Mine"

# value = profile or Id

# print(value)
