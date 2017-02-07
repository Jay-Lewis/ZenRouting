__author__ = 'Justin'

import gmapsKeys

# Load API Keys

APIkeys = gmapsKeys.keys('keys.txt','keyusages.txt','keydates.txt',2500)

APIkeys.printKeys()

key = APIkeys.getKey()

print('Given Key',key)

APIkeys.updateKey(key,2500)

APIkeys.printKeys()

key = APIkeys.getKey()

APIkeys.saveKeys()

APIkeys = gmapsKeys.keys('keys.txt','keyusages.txt','keydates.txt',2500)

APIkeys.printKeys()
