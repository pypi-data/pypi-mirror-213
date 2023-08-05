import sys
import os

ap = os.path.abspath('./krutils')
print ('imported:' + ap)

sys.path.append(ap)

import logger
l = logger.getlogger(__file__)
# print (l)
l.debug('[%%]', 123)
l.info('[%%]', 1111111111)





