class Config:
    SECRET_KEY = '1fa7cb73463e71ee4974b4d40970c0ec69ed0b6e37a359222ff8a62c9e532fcf42eee9361915fefeb9bfa83a33'     # This the secret key for debug
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'     # Creates the sqlite database in the current directory
    MAIL_SERVER = 'smtp.googlemail.com'   # Sets the mail configurations
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'SOME-USERNAME'
    MAIL_PASSWORD = 'SOME-PASSWORD'