

# Define the database - we are working with
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@172.17.0.1:5434/estay'


# Secret key for signing cookies
SECRET_KEY = "secret"

#path model ML
PATH_MODEL_ML = 'models/'

PATH_DATA = 'data/'

UNIT_PRICE = 300000
