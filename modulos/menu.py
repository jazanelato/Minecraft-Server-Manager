from modulos.data import colorize, chooseInt
from os import system

def clear():
    system('cls')

def cprint(msg, color='default'):
    print(colorize(msg, color))

def line(size, caracter='-', color='default'):
    cprint(caracter*size, color)

def choices(options: list, color='default', back=False):
    if back:
        options.append('Voltar')
    
    print()
    for i, v in enumerate(options):
        cprint(f' {i+1}) \t{v}\n', color)
    return len(options)

def title(msg, caracter='-', color='default', size=0):
    if size == 0:
        menusize = len(msg) + 4
        line(menusize, caracter, color)
        cprint(f'  {msg}  ', color)
        line(menusize, caracter, color)
    else:
        spacing = int(size/2 - len(msg)/2)
        line(size, caracter, color)
        cprint(' '*spacing + msg, color)
        line(size, caracter, color)

def menu(titlename:str, options:list, size=0, color='default', choicecolor='default', choicemsg='', caracter='-', back=False):
    clear()
    title(titlename, caracter, color, size)
    choicesnumber = choices(options, color, back)
    line(size, caracter, color)
    if choicemsg != '':
        choice = chooseInt(range(1, choicesnumber+1), choicemsg, choicecolor)
        return choice
