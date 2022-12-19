import os
import requests
import re
from tqdm import tqdm
from utils.soutils import color
from bs4 import BeautifulSoup

class DownloadFile: 

    @staticmethod
    def downloadFile(fullPathSave:str, link:str, fullLink:str):
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

    @staticmethod
    def getHtml(url):
        try:
            page = requests.get(url)
            return BeautifulSoup(page.content, 'html.parser')
        except: color.red("Error al obtener la pagina")

    # obtiene los links de los archivos con una expresion regular
    # que busca los archivos con extensiones especificas
    
    @staticmethod
    def getFileLink(soup):
        try:
            regexFiles = "([^\\s]+(\\.(?i)(mp4|pdf|html|zip|txt|url))$)"
            return soup.find_all(href=re.compile(regexFiles))
        except: color.red("Error al obtener los links")
    