import json
from lib.parser import Parser
from lib.tokenizer import *
from lib.models import Message
import time


class StartChat:
    # Asks user for input
    def __init__(self,):
        #self.command = input("Waiting for your input> ")
        self.name = "Jake"

    def take2nd(self,elem):
        return elem[1]

    def matcher(self,array, snt):
        # setting up lists
        ind = []
        all =[]
        final_dict = {'0':0}
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
            for key,val in dic.items():
                    if val == high:
                        our_sentence = array[int(key)]
            # Calculating number of words gotten right
            ratio = high/(len(snt)*1.0)
            #print("Ratio: ",ratio)
            if ratio >= 0.5:
                """ we once again go back to our dictionary(updated) and
                fetch the key
                that has the max value """
                final_dict[our_sentence]=ratio
                return final_dict
                # for key,val in dic.items():
                #     if val == high:
                #         return array[int(key)]
            else:
                return
        else:
            return

    def my_searcher(self,all_from_db,user):
        my_dict = {}
        for index,each in enumerate(all_from_db):
            ratio = self.ratio_match(user,each)
            if ratio >= .5:
                #my_dict.clear()
                my_dict[each]=ratio
        return my_dict


    def ratio_match(self,user,existing):
        from difflib import SequenceMatcher as sm
        return sm(None,user,existing).ratio()

    def my_matcher(self, all_msgs,new_msg,bot_ratio=0.5):
        my_dict = {'0':0}
        for index,each_msg in enumerate(all_msgs):
            ratio = self.ratio_match(new_msg,each_msg)
            if ratio > bot_ratio and ratio > list(my_dict.values())[0]:
                my_dict.clear()
                my_dict[each_msg]=ratio
        return my_dict


    def get_specific(self,tokens,robot_name,bot_ratio):
        robot_name=robot_name.lower()
        all_obj = Message.objects.filter(name=robot_name)
        all_msgs = []
        for each in all_obj:
            all_msgs.append(each.message)
        """Using our matcher function to get the closest match"""
        closest = self.my_matcher(all_msgs,tokens,bot_ratio)
        if list(closest.keys())[0] == '0':
            res = []
        else:
            matched = list(closest.keys())[0]
            all_matched_from_db = Message.objects.filter(message=str(matched),name=robot_name)
            # print("All from database:", all )
            res = []
            if len(all_matched_from_db) == 1:
                category = all_matched_from_db[0].category
                if category != "unanswered":
                    msgs_from_cat = Message.objects.filter(category=category,name=robot_name)
                    for i in msgs_from_cat:
                        res.append(i.response)
                else:
                    res = []
            elif len(all_matched_from_db)>1:
                for i in all_matched_from_db:
                    if i.category != "unanswered":
                        res.append(i.response)
            else:
                res = []

        return res


    def start(self,userinput,robot_name):
        """Tokenization of input from user to strip unnecessary punctuations"""
        tokens = Tokenizer().tokenize(userinput)
        res = []
        """Tokenization returns a list of chunks of words, we put them together here"""
        checker = ""
        for index,i in enumerate(tokens):
            if len(tokens)<2:
                checker +=i+""
            else:
                if not index == len(tokens)-1:
                    checker += i + " "
                else:
                    checker += i + ""

        checker = checker.lower()
        # company=Company.objects.get(robot_name=robot_name)
        company = "pywe"
        res = self.get_specific(tokens=checker,robot_name=robot_name,bot_ratio=0.6)
        # if len(res) == 0:
        #     company=Company.objects.get(robot_name="pywebot")
        #     res = self.get_specific(tokens=checker,robot_name="pywebot",bot_ratio=company.robot_ratio)

        # try:
        #     company=Company.objects.get(robot_name=robot_name)
        # except:
        #     company=""
        # else:

            # company.robot_traffic += 1
            # company.save()
            # company = company.name
        return Parser().parse(res=res,snt=tokens,company="pywe",robot_name=robot_name)
play = True
while play:
    message = input("Say Something:")
    robot = "pywebot"
    output = StartChat().start(message,robot)
    print(output[0])
    ask = input("Wanna chat? n/y:")
    if ask.lower() =="y":
        play = True
    else:
        play = False