import sys


HELLO_TEXT = ('\t ________________________________________________________________',
            '\t|                                                                |',
            '\t| THIS program download photo avatars from vk.com to Yandex disk |',
            '\t|________________________________________________________________|',
            '',
            'Be sure, that you have added necessary tokens in file settings.ini',
            ''
        )
INPUT_M = 'Please input VK user ID:'
INPUT_ = '-> '
CHECK_M = 'Check your input and try again.'
EXIT_M = 'If you want to exit the program input EXIT.'
USER_M = 'This user doesn\'t exists.'
NUM_M = 'is not an integer >= 0.'
STEP2_M = 'Do you want to enter number of photos to download?'
STEP3_M = 'How many photos do you want to download?'
FIVE_M = 'It is 5 by defauilt.'
ENTER_M = 'You can press Enter to skip this step.[Yes/No]'
INNUM_M = "Input integer number >=1."

EXIT_ = ['EXIT', 'exit']
YES_ = ['YES', 'Yes', 'Y', 'yes', 'y']
NO_ = ['NO', 'No', 'N', 'no', 'n']


def user_input():
    print(INPUT_, end='')
    return input()


def is_next_step_2(input_:str) -> bool:
    if input_ in EXIT_:
        return False
    if input_.isdigit() and int(input_) < sys.maxsize:
        return True
    else:
        print(f"{input_} {NUM_M} {CHECK_M} {EXIT_M}")
    return False


def is_next_step_3(input_:str) -> bool:
    if input_ in EXIT_:
        return None
    if len(input_) == 0 or input_ in NO_:
        return False
    if input_ in YES_:
        return True
    print(f"{CHECK_M} {EXIT_M}")
    return None
  

def is_loop_end(input_:str) -> bool:
    if input_ in EXIT_:
        return False
    if input_.isdigit() and int(input_) >= 1:
        return True
    print(f"{INNUM_M} {CHECK_M} {EXIT_M}")
    return False


def dialog_with_user() -> tuple:
    for s in HELLO_TEXT:
        print(s)
    
    input_ = ''
    step = 1
    print(INPUT_M)
    while input_ not in EXIT_:
        if step == 1:
            input_ = user_input()
            if is_next_step_2(input_):
                step = 2
                user_id = int(input_)
        elif step == 2:
            print(f"{STEP2_M} {FIVE_M} {ENTER_M}")
            input_ = user_input()
            is_ = is_next_step_3(input_)
            if is_ == None:
                continue
            elif not is_:
                number = 5
                break
            else:
                step = 3
        elif step == 3:
            print(f"{STEP3_M} ({FIVE_M})")
            input_ = user_input()
            if is_loop_end(input_):
                number = int(input_)
                break

    if input_ in EXIT_:
        return None, None
    return user_id, number 


if __name__ == "__main__":
    user_id, number = dialog_with_user()
    print()
    print(f'user_id = {user_id}\nnumber = {number}')
