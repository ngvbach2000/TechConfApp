import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="techconfdb.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="ushionguyen@techconfdb" #TODO: Update value
    POSTGRES_PW="Abcd1234@@@@"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'iGg57ZCUabdm866XbD2yxvgQPIU7QDn8IcJabGKTTVNBWiGg10y5Kw=='
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://notificationqueue.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=yrD4HcUY8sKFYM4JrvBrk6A65CHqr9ldcwer9QEC9D4=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'ngvbach2000@gmail.com'
    SENDGRID_API_KEY = '' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False