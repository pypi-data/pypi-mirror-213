##########################################
##      FILE, DIRECTORIES
##########################################
def _get_file_path_next_me() -> str():
    ''' 나자신(이 파일) 이후에 존재하는 스택(호출자)의 파일경로를 리턴'''
    import inspect
    for sfp in inspect.stack():
        if sfp[1] == __file__:
            found_me_yn = 'Y'
        elif found_me_yn == 'Y':
            return sfp[1]

    return None




def get_file_path_fr(file_name: str) -> str:
    '''
    config_file_path = get_file_path_ftr('config.json')
    > get file path following through root
    > file_name을 최상위 디렉토리까지 올라가며 찾는다.
    > 첫번째 확인된 경로를 리턴한다.
    '''
    if file_name == None or len(file_name.strip()) == 0:
        raise Exception('찾고자하는 파일명을 입력해 주세요')

    import os
    caller_file = _get_file_path_next_me()
    curr_dir = os.path.dirname(caller_file)
    # print("curr_dir[{0}]".format(curr_dir))

    file_path = ""
    for ii in range(100):
        # print(curr_dir, file_name, "찾는중이다")

        if (os.path.isfile(file_name) == True):      # 가상환경에서는 디렉토리정보가 없다!!?
            file_path = file_name
            # print("찾았다!", file_path)
            break
        elif (os.path.isfile(os.path.join(curr_dir, file_name)) == True):
            file_path = os.path.join(curr_dir, file_name)
            # print("찾았다!", file_path)
            break
        else:
            # print("상위로 찾아 올라간다[{0}]->[{1}]".format(curr_dir, os.path.abspath(os.path.join(curr_dir, '..'))))
            # root까지 확인된 경우 : 더이상 찾을 수 없을 때
            if (curr_dir == os.path.abspath(os.path.join(curr_dir, '..'))):
                # print("못찾았다!")
                #raise Exception(file_name + " 파일을 찾을 수 없습니다.")
                return None
            else:
                curr_dir = os.path.abspath(os.path.join(curr_dir, '..'))

    # print("find_first_file_to_root() -> [{0}]".format(file_path))
    return file_path


















##########################################
##      DATA 형식으로 변환
##########################################
def get_json_file_path_fr(file_name: str) -> dict():

    if file_name == None or len(file_name.strip()) == 0:
        raise Exception('찾고자하는 파일명을 입력해 주세요')

    data_file_path = get_file_path_fr(file_name)

    if (data_file_path == None):
        raise Exception('지정한 파일을 찾을 수 없습니다 [{0}]'.format(file_name))

    import json
    with open(data_file_path, encoding='UTF8') as df:
        json_data = json.load(df)

    return json_data




































