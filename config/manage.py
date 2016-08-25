# coding: utf-8
import sys
import platform
from init import read_config


if __name__ == '__main__':
    action = sys.argv[1]
    user_file = "users.ini"
    user_config = read_config(user_file)
    with open(user_file, "wb") as f:
        if action == "set":
            filename = sys.argv[2]
            user_config.set("users", platform.node(), filename)
            user_config.write(f)
        elif action == "rm":
            user_config.remove_option("users", platform.node())
            user_config.write(f)
        else:
            raise ValueError(action)