import sys
import os
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)
from models import Message
import config as config



obj = Message()


def migrate():
    if config.columns:
        print(obj.alter_table())
    else:
        print(obj.create_all())

migrate()