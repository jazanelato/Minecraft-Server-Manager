import os
import json
import time
import datetime
from modulos.menu import *
from modulos.data import *

# Variaveis de ambiente
menusize = os.get_terminal_size()[0]
basemenucolor = 'green'
compmenucolor = 'yellow'
config = dict()

# Classes
class Server():
    def __init__(self, serverlist: list, serverindex: int):
        self.name = serverlist[serverindex]
        self.path = f'{config["serverspath"]}\\{self.name}'
        self.files = os.listdir(self.path)
        self.propertiespath = f'{self.path}\\server.properties'
        for file in self.files:
            if 'minecraft_server' in file:
                self.initfile = file
                break
        self.properties = {'comments': []}
        with open(self.propertiespath, 'r') as file:
            rawdata = file.readlines()
        for line in rawdata:
            if line.startswith('#'):
                self.properties['comments'].append(line)
            else:
                line = line.replace('\n', '').split('=')
                self.properties[line[0]] = line[1]
        if 'MSM-Xmx' in self.properties.keys():
            self.maxmemory = self.getpropertievalue('MSM-Xmx')
        else:
            self.setproperties('MSM-Xmx', '1024', forceupdate=True)
        if 'MSM-Xms' in self.properties.keys():
            self.initmemory = self.getpropertievalue('MSM-Xms')
        else:
            self.setproperties('MSM-Xms', '1024', forceupdate=True)
    
    def init(self):
        os.system(f'cd {self.path} & java -Xmx{self.maxmemory}M -Xms{self.initmemory}M -jar {self.initfile} nogui')
    
    def backup(self):
        currentdate = datetime.date.today()
        if not os.path.exists(f'{config["backupspath"]}\\{self.name}'):
            os.mkdir(f'{config["backupspath"]}\\{self.name}')
        match config['compressortype']:
            case 1:
                backupname = f'{self.name}_Backup_{currentdate}.rar'
                os.system(f'{config["compressorpath"]} a -r -ep1 {config["backupspath"]}\\{self.name}\\"{backupname}" {self.path}')

            case 2:
                backupname = f'{self.name}_Backup_{currentdate}.zip'
                os.system(f"{config['compressorpath']} a {config['backupspath']}\\{self.name}\\{backupname} {self.path}")
        return backupname
    
    def getpropertievalue(self, propertiename:str):
        value = None
        for k,v in self.properties.items():
            if k == propertiename:
                value = v
                break
        return value

    def setproperties(self, propertiename:str, propertienewvalue:str, forceupdate=False):
        if propertiename in self.properties.keys() or forceupdate:
            self.properties.update({propertiename: propertienewvalue})
        else:
            return 1
        filebuf = list()
        for k,v in self.properties.items():
            if k == 'comments':
                for commentline in v:
                    filebuf.append(commentline)
            else:
                filebuf.append(f'{k}={v}\n')
        with open(self.propertiespath, 'w') as file:
            file.writelines(filebuf)


# Verificação e carregamento do config file
try:
    with open('.\\etc\\config.json', 'r') as configFile:
        config = json.load(configFile)
except:
    if not os.path.isdir('.\\etc'):
        os.mkdir('.\\etc')
    open('.\\etc\\config.json', 'x').close()

    # Preparando arquivo de configuração
    # Diretorio dos servidores
    title('Menu de Configuração', color=basemenucolor, size=menusize)
    cprint('Todos os caminhos inseridos não devem conter aspas, ex: C:\Program Files\...', basemenucolor)
    config['serverspath'] = readPath('Caminho da Pasta de Servidores: ', basemenucolor)
    cprint('ok!', compmenucolor)
    print()

    # Diretorio dos Backups
    config['backupspath'] = readPath('Caminho da Pasta de Backups: ', basemenucolor)
    cprint('ok!', compmenucolor)
    print()

    # Seleção do compactador e diretorio do compactador
    cprint('Seleção do compactador', basemenucolor)
    config['compressortype'] = chooseInt(range(0, choices(['WinRar', '7zip'], basemenucolor)+1), 'Opção: ', compmenucolor)
    config['compressorpath'] = readPath('Caminho do compactador de arquivos: ', basemenucolor)
    cprint('ok!', compmenucolor)
    print()

    cprint('Salvando Dados!', compmenucolor)
    with open('.\\etc\\config.json', 'w') as configFile:
        json.dump(config, configFile)
    cprint('Configurações Salvas com Sucesso!', compmenucolor)
    time.sleep(1.5)
    clear()

# Menu principal
while True:
    serversnamelist = list(os.listdir(config['serverspath']))
    menuserveropt = serversnamelist.copy()
    menuserveropt.append('Sair')
    clear()
    menuoption = menu('Minecraft Server Manager - MSM', menuserveropt, menusize, basemenucolor, compmenucolor, 'Opção: ')
    
    # Sair
    if menuoption == len(serversnamelist)+1:
        clear()
        title('Encerrando Programa!', color='red', size=menusize)
        time.sleep(1)
        break
    
    currentserver = Server(serversnamelist, menuoption-1)

    # Menu do Servidor
    while True:
        clear()
        menuoption = menu(f'Gerenciamento - {currentserver.name}', ['Iniciar', 'Alterar configurações', 'Fazer backup'], menusize, basemenucolor, compmenucolor, 'Opção: ', back=True)
        match menuoption:
            # Iniciar Servidor
            case 1:
                clear()
                title(f'Iniciando Servidor - {currentserver.name}', color=basemenucolor, size=menusize)
                currentserver.init()
            # Gerenciar Propriedades
            case 2:
                while True:
                    clear()
                    menuoption = menu(f'Gerenciador de Propriedades do Servidor - {currentserver.name}', [f'Alocação de Memoria - CV(Mb): Xmx:{currentserver.getpropertievalue("MSM-Xmx")}, Xms:{currentserver.getpropertievalue("MSM-Xms")}', f'Lotação Maxima CV(int): {currentserver.getpropertievalue("max-players")}', f'Modo Online CV(bool): {currentserver.getpropertievalue("online-mode")}', f'Dificuldade CV: {currentserver.getpropertievalue("difficulty")}', 'Outra'], menusize, basemenucolor, compmenucolor, 'Opção: ', back=True)
                    match menuoption:
                        # Alocação de Memoria
                        case 1:
                            clear()
                            title(f'Alocação de Memoria - {currentserver.name}', color=basemenucolor, size=menusize)
                            cprint(f'Valores atuais da alocação de memoria: Xmx(Alocação Maxima):{currentserver.getpropertievalue("MSM-Xmx")}, Xms(Alocação Inicial):{currentserver.getpropertievalue("MSM-Xms")}', basemenucolor)
                            maxmemory = input(colorize("XMx: ", compmenucolor))
                            menuoption = readyn(f'Usar alocação inicial recomendada {int(maxmemory)//2}Mb (S, N)? ', compmenucolor)
                            if menuoption == 'S':
                                initmemory = int(maxmemory)//2
                            else:
                                initmemory = input(colorize('Xms: ', compmenucolor))
                            currentserver.setproperties('MSM-Xmx', f'{maxmemory}')
                            currentserver.setproperties('MSM-Xms', f'{initmemory}')
                            cprint('OK!', compmenucolor)
                            time.sleep(1)
                        
                        # Lotação maxima
                        case 2:
                            clear()
                            title(f'Lotação Maxima - {currentserver.name}', color=basemenucolor, size=menusize)
                            cprint(f'Valor atual da lotação maxima: {currentserver.getpropertievalue("max-players")} Jogadores', basemenucolor)
                            propertyvalue = input(colorize('Lotação Maxima: ', compmenucolor))
                            currentserver.setproperties('max-players', propertyvalue)
                            cprint('OK!', compmenucolor)
                            time.sleep(1)
                        
                        # Modo online
                        case 3:
                            clear()
                            title(f'Modo Online - {currentserver.name}', color=basemenucolor, size=menusize)
                            cprint(f'Valor atual do modo online: {currentserver.getpropertievalue("online-mode")}', basemenucolor)
                            propertyvalue = input(colorize('Modo Online(bool): ', compmenucolor))
                            currentserver.setproperties('online-mode', propertyvalue)
                            cprint('OK!', compmenucolor)
                            time.sleep(1)
                        
                        # Dificuldade
                        case 4:
                            clear()
                            title(f'Dificuldade - {currentserver.name}', color=basemenucolor, size=menusize)
                            cprint(f'Valor atual da dificuldade(peaceful, easy, normal, hard): {currentserver.getpropertievalue("difficulty")}', basemenucolor)
                            propertyvalue = readdefstr(['peaceful', 'easy', 'normal', 'hard'], 'Dificuldade: ', compmenucolor)
                            currentserver.setproperties('difficulty', propertyvalue)
                            cprint('OK!', compmenucolor)
                            time.sleep(1)
                        
                        # Outra
                        case 5:
                            clear()
                            title(f'Outras Propriedades - {currentserver.name} | CUIDADO! Filtragem de dados desativada', color=basemenucolor, size=menusize)
                            propertykey = readdefstr(currentserver.properties.keys(), 'Nome da Propriedade: ', compmenucolor)
                            clear()
                            title(f'{propertykey} - {currentserver.name}', color=basemenucolor, size=menusize)
                            cprint(f'Valor(es) atual(is) da(o,s) {propertykey}: {currentserver.getpropertievalue(propertykey)}', basemenucolor)
                            propertyvalue = input(colorize(f'{propertykey}: ', compmenucolor))
                            currentserver.setproperties(propertykey, propertyvalue)
                            cprint('OK!', compmenucolor)
                            time.sleep(1)

                        # Voltar
                        case 6:
                            break

            # Backup
            case 3:
                clear()
                backupname = currentserver.backup()
                title(f'Backup Criado Com Exito! - {backupname}', color=basemenucolor, size=menusize)
                time.sleep(2)
            
            # Voltar
            case 4:
                break
