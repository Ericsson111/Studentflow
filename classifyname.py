import pandas as pd

data = pd.read_csv('name.csv', encoding= 'unicode_escape')
namedict = {}

class User:
    def __init__(self, namelist):
        self.self = self
        self.namelist = namelist

    def classifynamefunc(self, namelist):
        for names in namelist:
            if names[0] in namedict.keys():
                namedict[names[0]].append(names)
            else:
                namedict[names[0]] = []
                namedict[names[0]].append(names)
    
    def findnamefunc(self, targetName):
        dict_key = targetName[0]
        if dict_key in namedict.keys():
            if targetName in namedict[dict_key]:
                return f'{targetName} do exist in the database'
        else:
            return f'{targetName} do not exist in the database'

User = User(data['Name'])
User.classifynamefunc(data['Name'])
print(User.findnamefunc('Tarjan'))
