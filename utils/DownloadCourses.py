import os
import time
from  utils.soutils import color, createDirectories, createLog
from utils.Download import DownloadFile

class DownloadSectionCourse(DownloadFile):
    def __init__(self, url):
        self.url = url
        self.downloads = []
        self.error = []

    def saveFile(self, fullPathSave, pathLog): 
        try: 
            soup = self.getHtml(self.url)
            links = self.getFileLink(soup)

            if links:
                for link in links:
                    fullLink = f"{self.url}{link.get('href')}"
                    if not os.path.isfile(f"{fullPathSave}/{link.text}"): 
                        try:
                            print("\n")
                            color.orange(f"Obteniendo: {link.text}")

                            # Se empieza el proceso de descarga y se comprueba el estado de la respuesta
                            # Si todo esta bien respode con verdadero y sino con falso
                            dowlnloadF = self.downloadFile(fullPathSave, link, fullLink)
                            
                            if dowlnloadF:
                                color.green(f"El archivo {link.text} se descargo")
                                self.downloads.append({
                                    "title": link.text,
                                    "hour": time.strftime("%H:%M:%S"),
                                    "date": time.strftime("%d/%m/%Y"),
                                })
                            else: 
                                self.error.append({
                                    "title": link.text,
                                    "hour": time.strftime("%H:%M:%S"),
                                    "date": time.strftime("%d/%m/%Y"),
                                })
                                color.red(f"El archivo {link.text} no se encuentra disponible")

                        except KeyboardInterrupt:
                            color.red(f"Error al obtener {link.text}")
                            self.error.append({
                                "title": link.text,
                                "hour": time.strftime("%H:%M:%S"),
                                "date": time.strftime("%d/%m/%Y"),
                            })
                            if os.path.isfile(f"{fullPathSave}/{link.text}"):
                                os.remove(f"{fullPathSave}/{link.text}")
                            createLog(self.downloads, self.error, pathLog)
                            break
                    else: color.orange(f"Ya se descargo {link.text}")
            else: color.red("No se encontraron archivos para descargar")
        except:
            color.red("Error al obtener los links")

class DownloadAllCourse(DownloadFile):
    def __init__(self, url):
        self.url = url
        self.downloads = []
        self.error = []

    @property   
    def getFolders(self):
        
        # obteneindo el html de la pagina
        soup = self.getHtml(self.url)

        try:
            folders = []

            # se obtienen las imagenes con el alt de directorio
            imgDir = soup.find_all('img', alt="[Directorio]")
            
            if len(imgDir) > 0:
                for folder in imgDir:
                    title = folder.find_next('a').text
                    url = f"{self.url}{folder.find_next('a').get('href')}"
                    
                    if title and url: 
                        folders.append({
                            "title":title,
                            "url":url
                        })
                    else: color.red("Error al obtener la url de la carpeta")
            return folders
        except: color.red("Error al obtener las carpetas del curso")

    def saveAllFiles(self, fullPathSave: str):
        folders = self.getFolders
        # Descarga por cada carpeta del curso
        if folders and len(folders) > 0:

            for folder in folders:
                try:
                    # Se obtiene el html de la carpeta
                    soupFolderPage = self.getHtml(folder["url"])
                    
                    # Se obtienen los links de los archivos
                    links = self.getFileLink(soupFolderPage)

                    for _ in range(len(folder["title"]) + 40): print(color.ORANGE + "=", end="")
                    print(f"\n{color.ORANGE}[¡] Obteniendo archivos de la carpeta: {color.GREEN} {folder['title']}")
                    for _ in range(len(folder["title"]) + 40): print(color.ORANGE + "=", end="")
                    print("\n")

                    if links:
                        # Se crea una carpeta con el nombre de la seccion del curso
                        fullPathSaveFolder = f"{fullPathSave}/{folder['title']}"
                        createDirectories(fullPathSaveFolder)

                        for link in links:
                            fullLink = f"{folder['url']}{link.get('href')}"
                            
                            if not os.path.isfile(f"{fullPathSaveFolder}/{link.text}"): 
                                    color.orange(f"Obteniendo: {link.text}")

                                    # Se empieza el proceso de descarga y se comprueba el estado de la respuesta
                                    # Si todo esta bien respode con verdadero y sino con falso
                                    dowlnloadF = self.downloadFile(fullPathSaveFolder, link, fullLink)
                                    
                                    if dowlnloadF:
                                        color.green(f"El archivo {link.text} se descargo")
                                        self.downloads.append({
                                            "folderName": folder["title"],
                                            "pathFolder": fullPathSaveFolder,
                                            "title": link.text,
                                            "hour": time.strftime("%H:%M:%S"),
                                            "date": time.strftime("%d/%m/%Y")
                                        })
                                    else: 
                                        self.error.append({
                                            "folderName": folder["title"],
                                            "pathFolder": fullPathSaveFolder,
                                            "title": link.text,
                                            "hour": time.strftime("%H:%M:%S"),
                                            "date": time.strftime("%d/%m/%Y")
                                        })
                                        color.red(f"El archivo {link.text} no se encuentra disponible")
                            else: color.orange(f"Ya se descargo {link.text}")
                except KeyboardInterrupt: 
                    color.red(f"Error al obtener {link.text}")
                    self.error.append({
                        "folderName": folder["title"],
                        "pathFolder": fullPathSaveFolder,
                        "title": link.text,
                        "hour": time.strftime("%H:%M:%S"),
                        "date": time.strftime("%d/%m/%Y"),
                    })
                    if os.path.isfile(f"{fullPathSaveFolder}/{link.text}"):
                        os.remove(f"{fullPathSaveFolder}/{link.text}")
                    
                    createLog(
                        self.downloads, 
                        self.error, 
                        f"{fullPathSave}/files.log", 
                        "full"
                    )

                    break
                """
                    Crea un log con los archivos descargados y los que no se pudieron descargar
                    Cada que se descargue una carpeta completa
                """
                createLog(
                    self.downloads,
                    self.error,
                    f"{fullPathSaveFolder}/{folder['title']}/{folder['title']}.log",
                    "full"
                )
        else: color.red("No se encontraron carpetas para descargar")
    