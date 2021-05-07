from os import environ

MONGO_USER = environ['MONGO_USER']
MONGO_PASSWORD = environ['MONGO_PASSWORD']
MONGO_LINK1 = environ['MONGO_LINK1']
MONGO_DB_NAME = environ['MONGO_DB_NAME']
MONGO_URI = 'mongodb+srv://'+MONGO_USER+':'+MONGO_PASSWORD+MONGO_LINK1+MONGO_DB_NAME+'?retryWrites=true&w=majority'
SECRET_KEY = environ['SECRET_KEY']