import subprocess
from subprocess import Popen
from os import path
import time



pathOfFile=path.dirname(__file__)
pathToScriptClients = path.join(pathOfFile, "client.py")
pathToScriptServer = path.join(pathOfFile, "server.py")
server = ''
PROCESS = []
clients=[]

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        server = Popen(f"open -n -a Terminal.app '{pathToScriptServer}'", shell=True)
        PROCESS.append(server)
    elif ACTION == 'x':
        while PROCESS:
            instance = PROCESS.pop()
            instance.kill()



