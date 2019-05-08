import sys
import os
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)
from db import *
from tokenizer import *
from models import Message
from datetime import datetime
from random import choice

class Parser:
    def __init__(self):
        self.name = "Jake"

    def take2nd(self,elem):
        return elem[1]

    def matcher(self,array, snt):
        # setting up lists
        ind = []
        all =[]
        # looping through words in a sentence
        # and matching against what we have
        for word in snt:
            for index,i in enumerate(array):
                if word in i:
                    """ we append any match's index to ind list"""
                    ind.append(index)

        #print(ind)
        dic = {}
        """ we now create a dictionary of the indices so as to eliminate duplicates """
        for i in ind:
            dic['{}'.format(i)]=i
        #print(dic)
        """ we loop through the dictionary items and update
        the dictionary with their number of occurences """
        for key,val in dic.items():
            dic[key]=(ind.count(val))
            """ we add their occurences to a list from
            which we later get the max """
            all.append((ind.count(val)))
        if all:
            high = max(all)
            #print(dic)
            """ we once again go back to our dictionary(updated) and
            fetch the key
            that has the max value """
            for key,val in dic.items():
                if val == high:
                    return array[int(key)]
        else:
            return


    def search(self,array, snt):
        # setting up lists
        ind = []
        all =[]
        found = []
        # looping through words in a sentence
        # and matching against what we have
        for word in snt:
            for index,i in enumerate(array):
                if word in i:
                    """ we append any match's index to ind list"""
                    ind.append(index)
                    if not word in found:
                        found.append(word)

        #print(ind)
        dic = {}
        """ we now create a dictionary of the indices so as to eliminate duplicates """
        for i in ind:
            dic['{}'.format(i)]=i
        #print(dic)
        """ we loop through the dictionary items and update
        the dictionary with their number of occurences """
        for key,val in dic.items():
            dic[key]=(ind.count(val))
            """ we add their occurences to a list from
            which we later get the max """
            all.append((ind.count(val)))
        got = {}
        got_list= []
        jlist=[]
        final=[]
        if all:
            high = max(all)
            #print(dic)
            """ we once again go back to our dictionary(updated) and
            fetch the key
            that has the max value """
            for key,val in dic.items():
                if val > 0:
                    #got.append(array[int(key)])
                    got[key]=val
                    got_list.append((key,val))
            got_list.sort(key=self.take2nd,reverse=True)
            for key,val in got_list:
                final.append(array[int(key)])
            return (found,final)
        else:
            return

    def change_name(self,new_name):
        self.name = new_name
        return "I like my new name, {}".format(self.name)

    def match(self, arr, snts):
        count = 0
        for i in arr:
            if i in snts:
                count += 1
        #if count == len(arr):
        if (count/len(arr)*1.0) >= 0.5:
            return True
        else:
            return False

    def alt(self, arr, snts):
        count = 0
        for i in arr:
            if i in snts:
                count += 1
        if count >= 1:
            return True
        else:
            return False

    def respond(self,reps):
        self.reps = reps
        #print ('{}> '.format(self.name) + self.reps)
        #print(self.reps)
        return self.reps

    def parse(self,res, snt,company,robot_name):
        # choices = {1:"greetings",2:"response to greetings",3:"questions about python",4:"I dont know",5:"conversation",
        #           6:"actions",7:"general questions about me",8:"questions about what i can do",9:"How I'm doing"}
        # python_cat = {1:"Installation of python",2:"Facts about python",3:"Python Tricks"}
        # thanks = ['Hey thanks',"I appreciate that","Thanks for improving me","I'm really grateful"]
        #print(mes)
        #print(res)
        #print(snt[0])


        #if self.match(res,snt):
         #   print(True)
         #   self.respond(choice(res))
        #elif self.alt()
        if len(res) > 0:
            #for key,value in self.actions().items():
                #print(snt)
             #   if self.match(value[2],snt):
             #       param = []
             #       for i in value[1]:
             #           user = input(i+": ")
             #           param.append(user)
             #       func = value[0]
             #       print(func)
             #       self.respond(func(self,param[:]))
             #   else:
                return (self.respond(reps=choice(res)),True)

                #print(value[2])
                #if snt[0] in value[2]:
                #    print(key)

        else:
            res = ["Sorry, I cannot answer that, maybe next time",
            "Hello there, I am not yet trained to answer that",
            "Hey, sorry, I cannot answer that now",
            "I am very sorry to disappoint you, I cannot reply that now",
            "I am still being trained so please forgive me, I cannot answer that",
            "Sometime in the future I will be able to answer that, fingers crossed"]
            reply = choice(res)
            #reply="I cannot answer"


            question = ""
            if len(snt) == 1:
                question += snt[0]
            else:
                for index,i in enumerate(snt,1):
                    if index == len(snt):
                        question += i+""
                    else:
                        question += i+ " "
            existing = Message.objects.filter(message=question)
            if len(existing) == 0:
                new = Message()
                new.message = question
                new.response = reply
                new.company=company.lower()
                new.name=robot_name.lower()
                new.category = "unanswered"
                new.save()


            return (self.respond(reps=reply),False)
            # self.respond(reps="still improving, i don't understand that for now")
            # user = input("Please teach me the answer: ")
            # print("""My Categories:\n""")
            # for key,value in choices.items():
            #     print("{}. {}".format(key,value))
            # cat = input("To what category does this answer belong?: ")
            # string = ""
            # for i in snt:
            #     string += i + " "
            # string = string.strip()
            # # date = datetime.now().date()
            # # time = datetime.now().time()
            # new = Message()
            # new.message = string
            # new.response = user
            # if choices[(int(cat))] == "questions about python":
            #     print("Please help me, what category does it belong in python?: \n")
            #     for key,value in python_cat.items():
            #         print("{}. {}".format(key,value))

            #     act_cat = input("Classify the action: ")

            #     new.category = python_cat[(int(act_cat))]
            # else:
            #     new.category = choices[(int(cat))]
            # new.save()
            # return choice(thanks)
            #self.db.create_error(string)
            #print(self.actions())

    def actions(self):
        actions = {}
        all = Parser.__dict__
        for name,value in all.items():
            if not name.startswith("__"):
                if "name" in name:
                    actions[name]=[value,['new_name'],['change','name','new','name']]
            #if keyword in name:
            #    value(self,"Theo")
        return actions


# exist = [['why', 'there','python'],['what', 'is', 'python', 'used', 'for']
# ,['what', 'is', 'python', 'programming','language']
# ,['hello','how','is','it'],['hello','how','are','you']]
# snt= input("Please type your message: ")
# print("\n")
# print("""Here is the most appropriate match from our database""")
# print(match(exist,snt.split(" ")))
# print("\n")
# print ("""Here is a search using your input""")
# searchrs = search(exist,snt.split(" "))

# print("Words matched:")
# if searchrs:
#     for i in searchrs[0]:
#         print(i)
#     print("\n")
#     print("Here are it's results:")
#     for i in searchrs[1]:
#         print(i)
# else:
#     print(None)


