import os
from  utils.soutils import color
from utils.Download import DownloadFile

class DownloadSectionCourse(DownloadFile):
    def __init__(self, url):
        self.url = url
        self.downloads = []
        self.error = []

    def saveFile(self, fullPathSave): 
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
                                    "title": link.text
                                })
                            else: 
                                self.error.append({
                                    "title": link.text
                                })
                                color.red(f"El archivo {link.text} no se encuentra disponible")

                        except KeyboardInterrupt:
                            color.red(f"Error al obtener {link.text}")
                            self.error.append({
                                "title": link.text
                            })
                            if os.path.isfile(f"{fullPathSave}/{link.text}"):
                                os.remove(f"{fullPathSave}/{link.text}")
                            break
                    else: color.orange(f"Ya se descargo {link.text}")
            else: color.red("No se encontraron archivos para descargar")
        except:
            color.red("Error al obtener los links")

class DownloadAllCourse(DownloadFile):
    def __init__(self, url):
        self.url = url

    @property   
    def getFolders(self):
        soup = self.getHtml(self.url)
        try:
            folders = []

            # se obtienen las imagenes con el alt de directorio
            imgDir = soup.find_all('img', alt="[Directorio]")
            
            if len(imgDir) > 0:
                # se obtienen los links despues de la imagen de directorio
                for folder in imgDir:
                    folders.append({
                        "title": folder.find_next('a').text,
                        "url": f"{self.url}{folder.find_next('a').get('href')}"
                    })
            
            return folders
        except: color.red("Error al obtener las carpetas del curso")

    def saveAllFiles(self, fullPathSave: str):
        folders = self.getFolders

        # Descarga por cada carpeta del curso
        for folder in folders:
            soupFolderPage = self.getHtml(folder["url"])
            links = self.getFileLink(soupFolderPage)

            for line in range(len(folder["title"]) + 40): print(color.ORANGE + "=", end="")
            print(f"\n{color.ORANGE}[¡] Obteniendo archivos de la carpeta: {color.GREEN} {folder['title']}")
            for line in range(len(folder["title"]) + 40): print(color.ORANGE + "=", end="")
            print("\n")

            if links:
                for link in links:
                    fullLink = f"{folder['url']}{link.get('href')}"
                    print(fullLink)
            
            print("\n")

                    
