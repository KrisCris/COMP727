DB_USERNAME = 'iot'
DB_PASSWORD = 'iot'
DB_ADDRESS = 'localhost'
DB_PORT = '3306'
DATABASE = 'iot'
DB_CHARSET = 'utf8mb4'

HOST = '0.0.0.0'
PORT = 5000
DEBUG = True
ENV = 'development'


REPLY_CODES = {
    3: 'idle',
    2: 'Working stopped',
    1: 'Success',
    0: 'Error',
    -1: "Haven't finished since last work",
    -2: 'Should start a new work first'
}