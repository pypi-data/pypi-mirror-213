from os import environ
from getpass import getpass
import dotenv

quos = lambda str_iter: ",".join([f"'{s}'" for s in str_iter])


def constr(**kwargs):
    """kwargs
    ---
    host: db host address
    port: db port
    db_name: db name
    username: username
    password: password !!!가능하면 코드에 비밀번호는 넣지 않는게 좋음!!!

    no default values. 넣지 않은 값이 있으면 input 으로 물어봄.

    !!!가능하면 env파일을 코드 실행폴더에 별도로 생성해서 사용하는 것이 좋음!!!
    envfile: envfile path. env 파일을 지정할 경우 kwargs로 입력한 값보다 env에 있는 값을 먼저 적용함.

    .db.env.template

    host=localhost
    port=5432
    db_name=postgres
    username=nanangqq
    password=password

    """
    if kwargs.get("envfile"):
        dotenv.load_dotenv(kwargs.get("envfile"))

    keys = ["host", "port", "db_name", "username"]
    db = {}

    for key in keys:
        db[key] = environ.get(key) or kwargs.get(key) or input(f"{key}? ")

    db["password"] = environ.get("password") or getpass(
        f"password for {db['username']}@{db['host']}? "
    )

    result = f"postgresql://{db['username']}:{db['password']}@{db['host']}:{db['port']}/{db['db_name']}"

    if kwargs.get("envfile"):
        for key in keys:
            if key in environ:
                environ.pop(key)
    return result
