__author__ = 'Justin'

# DESCRIPTION:
# This class set provides a convenient way to utilize multiple GoogleMaps API keys
#
# METHODS:
# (constructor): creates a 'keys' object from information saved to file
# (getKey): returns a usable API key
# (updateKey): updates usage for a specific key
# (saveKeys): saves key information to file
# (printKeys): prints key names and current usages



from datetime import datetime
from random import choice

class keys:
    def __init__(self,keystringsfile,usagefile,datesfile, maxuses):
        self.keysdict = {}
        self.keysfilename = keystringsfile
        self.usagesfilename = usagefile
        self.datesfilename = datesfile
        self.maxusage = maxuses
        with open(keystringsfile) as f:
            keystrings = f.read().splitlines()
        with open(usagefile) as g:
            usages_ = g.read().splitlines()
        usages = []
        for use in usages_:
            usages.append(int(use))
        with open(datesfile) as h:
            dates = [tuple(map(int, i.split(','))) for i in h]
        for keystring,usage,date in zip(keystrings,usages,dates):
            self.keysdict[keystring] = key(keystring,usage,date)
        self.updateAllKeys()

    def updateKey(self,keystring,amount):
        currentkey = self.keysdict[keystring]
        now = datetime.now()
        currentdate = [now.day,now.month,now.year]
        if(currentkey.date == currentdate ):
            currentkey.usage += amount
        else:
            currentkey.usage = 0
            currentkey.date = currentdate

    def updateAllKeys(self):
        now = datetime.now()
        currentdate = [now.day,now.month,now.year]
        for keystring,currentkey in self.keysdict.items():
            if(currentkey.date != currentdate ):
                currentkey.usage = 0
                currentkey.date = currentdate

    def getKey(self,usage):
        maxiter = 100
        iter = 0
        while(iter < maxiter):
            keystring = choice(self.keysdict.keys())
            currentkey = self.keysdict[keystring]
            if(currentkey.pause > 0):
                currentkey.pause -= 1
                print('minus 1')
            else:
                if(currentkey.usage < self.maxusage):
                    self.updateKey(currentkey.name,usage)
                    return currentkey.name
                iter+=1

    def setDefective(self,keystring,amount):
        self.keysdict[keystring].pause += amount

    def printKeys(self):
        for keystring in self.keysdict:
            currentkey = self.keysdict[keystring]
            print('KeyName:',currentkey.name)
            print('KeyUsage:',currentkey.usage)
            print('KeyDate:',currentkey.date)

    def saveKeys(self):
        f = open(self.keysfilename,'w')
        g = open(self.usagesfilename,'w')
        h = open(self.datesfilename,'w')
        for keystring in self.keysdict:
            f.write(self.keysdict[keystring].name+'\n')
            g.write(str(self.keysdict[keystring].usage)+'\n')
            h.write(str(self.keysdict[keystring].date)[1:-1]+'\n')
        f.close()
        g.close()
        h.close()

    def __del__(self):
        self.saveKeys()

class key:
    def __init__(self,string,pastuses,pastdate):
        now = datetime.now()
        self.name = string
        self.date = [now.day,now.month,now.year]
        self.pause = 0
        if(pastdate != (now.day,now.month,now.year)):
            self.usage = 0
        else:
            self.usage = pastuses

