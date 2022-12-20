import os
import requests
import re
from tqdm import tqdm
from utils.soutils import color
from bs4 import BeautifulSoup

class DownloadFile: 
    REGEX_FILES = "([^\\s]+(\\.(?i)(mp4|pdf|html|zip|txt|url))$)"

    @classmethod
    def downloadFile(cls, fullPathSave:str, link:str, fullLink:str):
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
        
        if os.path.isfile(f"{fullPathSave}/{link.text}"):
            if total_size_in_bytes != os.path.getsize(f"{fullPathSave}/{link.text}"):
                color.red("Error al descargar el archivo")
                os.remove(f"{fullPathSave}/{link.text}")
                return False
        else:
            color.green(f"El archivo {link.text} se descargo")
            return True

    @classmethod
    def getHtml(cls, url):
        try:
            page = requests.get(url)
            return BeautifulSoup(page.content, 'html.parser')
        except: color.red("Error al obtener la pagina")

    # obtiene los links de los archivos con una expresion regular
    # que busca los archivos con extensiones especificas
    
    @classmethod
    def getFileLink(cls, soup):
        try:
            return soup.find_all(href=re.compile(cls.REGEX_FILES))
        except: color.red("Error al obtener los links")
    