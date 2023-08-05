

'''
다음과 같이 logging class로 대체하자
'''


import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(name)s] %(message)s')


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler('test_logging.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.debug('내 이름은 디버그 입니다.')
logger.info('내 이름은 인포 입니다.')
logger.error('내 이름은 에러 입니다.')
logger.warning('내 이름은 원 입니다.')




