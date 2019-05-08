import sys
import os
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)
import config as config


class Objects:
    __tablename__ = config.table_name
    __conn__ = config.conn
    __cursor__ = __conn__.cursor()

    def __init__(self,*args):
        pass
        #if args:
        #    self.__tablename__= args[0]
        #    self.__conn__ = args[1]
        #    self.__cursor__ = args[2]

    class Object:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

        class Meta:
            verbose_name = "Message"

        def __str__(self):
            return '%s' % (self.id)

    def all(self):
        results = []
        pairs = []
        #pairer = []
        sql = "SELECT * FROM {}".format(self.__tablename__)
        #print(sql)
        try:
            result = self.__cursor__.execute(sql)
        except Exception as e:
            print(e)
            return []
        else:
            result = result.fetchall()
            if len(result) < 0:
                return []
            #print(result)
            #print(config.columns)
            for each in result:
                obj = self.Object()
                count = 0
                for i in each:
                    obj.__setattr__(config.columns[count],i)
                    pairs.append((config.columns[count],i))
                    count+=1
                results.append(obj)
                del obj
            #print(pairs)
            return results

    def filter(self,**kwargs):
        results = []
        pairs= []
        if kwargs:
            sql = "SELECT * FROM {}".format(self.__tablename__)
            for index, (key, value) in enumerate(kwargs.items(), 1):
                if index < 2:
                    sql += " WHERE {} = '{}'".format(key, value)
                else:
                    sql += " AND {} = '{}'".format(key, value)
        else:
            sql = "SELECT * FROM {}".format(self.__tablename__)
        #print(sql)
        try:
            result = self.__cursor__.execute(sql)
        except Exception as e:
            print(e)
            return []
        else:
            if result is None:
                return []
            for each in result:
                obj = self.Object()
                count = 0
                for i in each:
                    obj.__setattr__(config.columns[count],i)
                    pairs.append((config.columns[count],i))
                    count += 1
                results.append(obj)
                del obj
            #print(pairs)
            return results
    def get(self,**kwargs):
        results = []
        pairs= []
        if kwargs:
            sql = "SELECT * FROM {}".format(self.__tablename__)
            for index, (key, value) in enumerate(kwargs.items(), 1):
                if index < 2:
                    sql += " WHERE {} = '{}'".format(key, value)
                else:
                    sql += " AND {} = '{}'".format(key, value)
        else:
            sql = "SELECT * FROM {}".format(self.__tablename__)
        #print(sql)
        try:
            result = self.__cursor__.execute(sql)
        except Exception as e:
            print(e)
            return []
        else:
            if result is None:
                return []
            for each in result:
                obj = self.Object()
                count = 0
                for i in each:
                    obj.__setattr__(config.columns[count],i)
                    pairs.append((config.columns[count],i))
                    count += 1
                results.append(obj)
                del obj
            #print(pairs)
            return results[0]

    def update(self,id,**kwargs):
        if kwargs:
            sql = "UPDATE {} SET ".format(self.__tablename__)
            for index,(key,value) in enumerate(kwargs.items(),1):
                if index < 2:
                    sql += "{}='{}'".format(key, value)
                else:
                    sql += ",{} ='{}'".format(key, value)
            sql += " WHERE id = '{}'".format(id)
            #print(sql)
            try:
                self.__cursor__.execute(sql)
            except Exception as e:
                # print(e)
                return False
            else:
                self.__conn__.commit()
                return True

    def delete(self,**kwargs):
        #results = []
        #pairs= []
        if kwargs:
            sql = "DELETE FROM {}".format(self.__tablename__)
            for index, (key, value) in enumerate(kwargs.items(), 1):
                if index < 2:
                    sql += " WHERE {} = '{}'".format(key, value)
                else:
                    sql += " AND {} = '{}'".format(key, value)
        else:
            user = input("Are you sure you want to delete everything?:y/N ")
            if user == "y":
                sql = "DELETE * FROM {}".format(self.__tablename__)
            else:
                return
        # print(sql)
        try:
            self.__cursor__.execute(sql)
        except Exception as e:
            # print(e)
            return False
        else:
            self.__conn__.commit()
            return True
            # if result is None:
            #     return []
            # for each in result:
            #     obj = self.Object()
            #     count = 0
            #     for i in each:
            #         obj.__setattr__(config.columns[count],i)
            #         pairs.append((config.columns[count],i))
            #         count += 1
            #     results.append(obj)
            #     del obj
            # #print(pairs)
            # return results[0]


class models:
    class CharField:
        def __init__(self, max_length,**option):
            self.max_length = max_length

    class IntegerField:
        def __init__(self, **options):
            self.__dict__.update(options)

    class FloatField:
        def __init__(self):
            pass
