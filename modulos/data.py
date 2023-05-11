from os.path import exists, normpath

def colorize(msg, color='default'):
    '''
    -> colorize(msg, color='default')
        color:{
            white,
            red,
            green,
            yellow,
            blue,
            purple,
            cyan,
            grey
        }
        retorna a string formatada com os codigos de cores
    '''
    color = color.strip().lower()
    colors = {
        'default': '',
        'white': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'purple': '35',
        'cyan': '36',
        'grey': '37'
    }
    try:
        return f'\033[{colors[color]}m{msg}\033[m'
    except KeyError:
        return f'{msg}'

def readInt(msg='', color='default'):
    inp = input(colorize(msg, color))
    while not inp.isnumeric():
        print(colorize('O valor inserido não é um numero inteiro!', 'red'))
        inp = input(colorize(msg, color))
    return int(inp)

def chooseInt(optionsrange:list, msg='', color='default'):
    inp = readInt(msg, color)
    while inp not in optionsrange:
        print(colorize('Opção Invalida!', 'red'))
        inp = readInt(msg, color)
    return inp

def readyn(msg='', color='default'):
    inp = input(colorize(msg, color)).capitalize()
    while inp not in ['S', 'N']:
        print(colorize('Opção Invalida!', 'red'))
        inp = input(colorize(msg, color)).capitalize()
    return inp

def readdefstr(options:list, msg='', color='default'):
    inp = input(colorize(msg, color))
    while inp not in options:
        print(colorize('Opção Invalida!', 'red'))
        inp = input(colorize(msg, color))
    return inp

def readPath(msg='', color='default'):
    inp = input(colorize(msg, color))
    while not exists(inp):
        print(colorize('Caminho de diretorio invalido!', 'red'))
        inp = input(colorize(msg, color))
    splitedpath = inp.split('\\')
    for dir in splitedpath:
        if ' ' in dir:
            splitedpath[splitedpath.index(dir)] = f'"{dir}"'
    inp = normpath('\\'.join(splitedpath))
    return inp
