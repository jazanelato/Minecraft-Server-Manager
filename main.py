from modulos.data import *
from modulos.menu import *
from private import *
from time import sleep
import os
import datetime

#   Constantes de configuração do Menu
menusize = 100

#   Definições
class Servidor():
    def __init__(self, serverlist:list, serverindex:int):
        self.name = serverlist[serverindex]
        self.path = f'{serverspath}\\{self.name}'
        self.files = os.listdir(self.path)
        self.version = os.listdir(f'{self.path}\\versions')[0]
        for file in self.files:
            if 'server.jar' in file or 'minecraft_server' in file:
                self.initfile = file
    
    def init(self):
        os.system(f'cd {self.path} & java -Xmx2048M -Xms2048M -jar {self.initfile} nogui')

    def backup(self):
        currentdate = datetime.date.today()
        backupname = f'{self.name} Backup {currentdate}.rar'
        if not os.path.exists(f'{backuppath}\\{self.name}'):
            os.mkdir(f'{backuppath}\\{self.name}')
        os.system(f'{rarpath} a -r -ep1 {backuppath}\\{self.name}\\"{backupname}" {self.path}')
        return backupname


while True: # Menu Principal
    menuoption = menu('Minecraft Server Manager', ['Gerenciamento', 'Listar Servidores', 'Sair'], menusize, 'green', 'yellow', 'Opção: ')

    match menuoption:
        case 1: # Gerenciamento
            servers = os.listdir(serverspath)
            menuoption = menu('Gerenciamento de Servidores - Selecionar Servidor', servers, menusize, 'green', 'yellow', 'Opção: ', back=True)
            if menuoption > len(servers):
                continue
            server = Servidor(servers, menuoption-1)
            
            while True: # Menu de Funções para o Servidor Selecionado
                menuoption = menu(f'Opções de Gerenciamento - {server.name}', ['Iniciar', 'Fazer Backup'], menusize, 'green', 'yellow', 'Opção: ',back=True)
                
                match menuoption:
                    case 1: # Iniciar
                        clear()
                        title(f'Iniciando Servidor - {server.name}', color='green', size=menusize)
                        server.init()
                    
                    case 2: # Backup
                        clear()
                        backupname = server.backup()
                        title(f'Backup Criado Com Exito! - {backupname}', color='green', size=menusize)
                        sleep(3)

                    case 3: # Voltar
                        break

        case 2: # Listagem
            servers = os.listdir(serverspath)
            menu('Servidores Disponiveis', servers, menusize, 'green')
            input(colorize('Pressione enter para continuar...', 'yellow'))

        case 3: # Sair
            clear()
            cprint('Encerrando Programa!', 'red')
            sleep(2)
            break
