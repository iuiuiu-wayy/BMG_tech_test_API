class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgresdb:5432/postgres' # 'postgresql://postgres:project@localhost/JubliaDB'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '8382a02149664e938d2d9eaa58dfe3f3'

    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USERNAME = 'email@gmail.com'
    # MAIL_PASSWORD = 'password'
    # MAIL_DEFAULT_SENDER = 'email@gmail.com'
    # DEBUG = True
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # CELERY_BROKER_URL='redis://redis:6379'
    # CELERY_RESULT_BACKEND='redis://redis:6379'
    # TIMEZONE = 'Singapore'