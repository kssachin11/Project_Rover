import platform


styles = {
    'black': '\33[30m',
    'red': '\33[31m',
    'green': '\33[32m',
    'yellow': '\33[33m',
    'blue': '\33[34m',
    'magenta': '\33[35m',
    'cyan': '\33[36m',
    'light gray': '\33[37m',
    'dark gray': '\33[90m',
    'light red': '\33[91m',
    'light green': '\33[92m',
    'light yellow': '\33[93m',
    'light blue': '\33[94m',
    'light magenta': '\33[95m',
    'light cyan': '\33[96m',
    'white': '\33[97m',
    'bold': '\33[1m',
    'underline': '\33[4m',
    'default': '\33[0m'
}



def printDebug(str, color='black', bold=False, underline=False, level=0):
    if platform.system() == 'Windows':
        quad = ''
        for _ in range(level): quad += '   '
        print(f'{quad}{styles[color] + (styles["bold"] if bold else "")} o {(styles["underline"] if underline else "")}' + str.__str__() + '\33[0m')
    else: print(f'{quad} o ' + str.__str__())
