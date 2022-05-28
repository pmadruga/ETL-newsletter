import os
from dotenv import dotenv_values


abs_path = os.path.abspath(os.path.dirname(__file__))
ENV = dotenv_values(f"{abs_path}/.env")
for item in ENV:
    print(item)
