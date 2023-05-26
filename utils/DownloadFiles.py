import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
from  utils.soutils import color

class DownloadFile:
    def __init__(self, url):
        self.url = url
        self.downloads = []
        self.error = []

    @property
    def getHtml(self):
        try:
            page = requests.get(self.url)
            return BeautifulSoup(page.content, 'html.parser')
        except: color.red("Error al obtener la pagina")
    
    def saveFile(self, fullPathSave): 
        try: 
            soup = self.getHtml
            regexFiles = r"[^\s]+\.(mp4|pdf|html|zip)$"
            links = soup.find_all(href=re.compile(regexFiles, re.IGNORECASE))
            if links:

                for link in links:
                    fullLink = f"{self.url}{link.get('href')}"

                    if not os.path.isfile(f"{fullPathSave}/{link.text}"): 
                        try:
                            print("\n")
                            color.orange(f"Obteniendo: {link.text}")
                            response = requests.get(fullLink, stream=True)
                            print(color.ORANGE)
                            if response.status_code == 200:
                                total_size_in_bytes= int(response.headers.get('content-length', 0))
                                block_size = 1024 
                                progress_bar = tqdm(total=total_size_in_bytes, ascii=" ▖▘▝▗▚▞█", unit='iB', unit_scale=True)

                                with open(f"{fullPathSave}/{link.text}", 'wb') as file:
                                    for data in response.iter_content(block_size):
                                        progress_bar.update(len(data))
                                        file.write(data)
                                progress_bar.close()
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
        except e:
            print(e)
            color.red("Error al obtener los links")
