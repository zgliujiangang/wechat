# coding: utf-8
import platform
import ConfigParser


def read_config(file_name):
    config = ConfigParser.RawConfigParser()
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
    print dir(config)
    print config.sections()
    name = config.get("mysql", "name")
    print name
    

    