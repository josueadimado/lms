import sys
import os
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)
from db import *
from objects import *


class Message(DBA):
    #print(__qualname__)
    id = models.IntegerField(PRIMARY_KEY=True)
    message = models.CharField(max_length=1000)
    response = models.CharField(max_length=1000)
    category = models.CharField(max_length=500)
    company = models.CharField(max_length=500)
    user_id = models.IntegerField()
    name = models.CharField(max_length=250)






#obj = Message()
#obj.create_all()

