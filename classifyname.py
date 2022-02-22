import pandas as pd
#Write comments mf
# k

'''
The classifynamefunc will be checking the first letter of the name and determine wether or not the key already exist
and all the name will be add to their own key(example: namedict = {'a': ['abc', 'adf', 'abz'], 'b': ['bfc', 'bgf', 'bge']})

The findnamefunc will first determine wether or not the first letter(key) is inside the namedict keys, if it is, return True
otherwise return False
'''

data = pd.read_csv('exampleName.csv', encoding= 'unicode_escape') # accessing exampleName.csv with pandas
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
