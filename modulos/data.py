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

def chooseInt(optionsrange:list, msg='', color='desault'):
    inp = readInt(msg, color)
    while inp not in optionsrange:
        print(colorize('Opção Invalida!', 'red'))
        inp = readInt(msg, color)
    return inp
