# coding: utf-8
import platform
import ConfigParser
import os

def read_config(file_name):
    current_path = os.path.dirname(__file__)
    file_name = os.path.join(current_path, file_name)
    config = ConfigParser.ConfigParser()
    with open(file_name) as f:
        config.readfp(f)
    return config


def init_config():
    user_file = "users.ini"
    user_config = read_config(user_file)
    current_user = platform.node()
    init_file = user_config.get("users", current_user)
    config = read_config(init_file)
    return config


if __name__ == "__main__":
    config = init_config()
    print config
    redis_host = config.get("redis", "host")
    print redis_host
    

    