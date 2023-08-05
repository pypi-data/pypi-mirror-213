import sys
import os

ap = os.path.abspath(os.path.dirname(os.path.dirname('./../krutils')))
# print (ap)

sys.path.append(ap)

from krutils import futils

print (futils.get_file_path_fr('logger.json'))
print (futils.get_file_path_fr('test_logger.py'))


# futils.test()

# sss = futils._get_file_path_next_me()
# print(sss)



