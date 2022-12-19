import os
import time

def logo():
    clear()
    logo = open("./logo.txt", "r")
    print(color.BLUE + logo.read())
    logo.close()

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def createDirectories(pathOrFolder: str):
    try:
        os.makedirs(pathOrFolder)
    except FileExistsError:
        color.orange(f"Ya hay una carpeta con este nombre, los datos se guardaran en esta direccion:")
        color.green(f"{pathOrFolder}\n")


def createPathLog(pathLog: str):
    if pathLog and os.path.isdir(pathLog):
        pthlg = f"{pathLog}/files.log" if not pathLog.endswith("/") else f"{pathLog}files.log" 
        
        logp = open("pathsavelog.txt", "w")
        logp.write(pthlg)
        logp.close()

        color.orange("Se guardo la ruta del log en:")
        color.green(pthlg)

        return pthlg
    elif not pathLog:
        try:
            logp = open("pathsavelog.txt", "r")
            pthlg = logp.read()
            
            color.orange("Guarando log en:")
            color.green(pthlg)
            logp.close()
            return pthlg
        except: 
            return "files.log"
    else: 
        color.red("No es una ruta valida para el log")
        return "files.log"
    

def createLog(dwf:list, errf: list, pathLog:str = ""):
    clear()
    logo()
    print("\n")
    try:
        if len(dwf) > 0 or len(errf) > 0:
            file = open(pathLog, "a")

            if len(dwf) > 0:
                print(f"\n{color.GREEN} Archivos descargados {color.RESET}\n")
                file.write("Archivos descargados\n")
                for f in dwf:
                    color.green(f"Nombre: {f['title']}")
                    file.write(f"Nombre: {f['title']}\n")
            
            if len(errf) > 0:
                color.red("Archivos no descargados")
                file.write("\nArchivos no descargados\n")

                for f in errf:
                    color.red(f"Nombre: { f['title'] }")
                    file.write(f"Nombre: { f['title'] }\n")
            file.close()
    except PermissionError: 
        color.red("No tienes permisos para crear un log en esta ruta, intenta con sudo")
    except: 
        color.red("Error al generar el log")

class color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

    @classmethod
    def red(cls, text):
        print(f"{cls.RED} [x] {text} {cls.RESET}")
    
    @classmethod
    def orange(cls, text):
        print(f"{cls.ORANGE} [¡] {text} {cls.RESET}")

    @classmethod
    def green(cls, text):
        print(f"{cls.GREEN} [+] {text} {cls.RESET}")