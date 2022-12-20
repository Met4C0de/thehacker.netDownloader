import os
import argparse 

from utils.soutils import color, createDirectories, createLog, createPathLog, logo
from utils.DownloadCourses import DownloadSectionCourse, DownloadAllCourse

parser = argparse.ArgumentParser(
    description='Script para descargar cursos de elhacker.net'
)

parser.version = '1.0'

parser.add_argument('-url',
                    type=str,
                    required=True,
                    help='Url del curso')
parser.add_argument('-fs', '--folder-save',
                    type=str,
                    required=True,
                    help='Ruta donde se guardara el curso')
parser.add_argument('-a', '--author',
                    type=str,
                    required=False,
                    help='Autor del curso')
parser.add_argument('-s', '--section',
                    type=str,
                    required=False,
                    help='Seccion del curso')
parser.add_argument('-pl', '--pathlog',
                    type=str,
                    required=False,
                    help='Ruta donde se guardara el log')
parser.add_argument('-full', '--full-course',
                    action='store_true',
                    help='Descargar el curso completo')


args = parser.parse_args()

if __name__ == "__main__":
    
    logo()
    print(f'\n\033[?25l{color.ORANGE}', end="") # oculta el cursor

    pathSaved = args.folder_save
    
    if os.path.isdir(pathSaved):
        if not args.full_course:
            pathLog = createPathLog(args.pathlog) 
            downSectionC  = DownloadSectionCourse(args.url)
            
            if args.author and not args.section:
                createDirectories(f"{pathSaved}/{args.author}")
                downSectionC.saveFile(f"{pathSaved}/{args.author}", pathLog)

            elif args.author and args.section:
                createDirectories(f"{pathSaved}/{args.author}/{args.section}")
                downSectionC.saveFile(f"{pathSaved}/{args.author}/{args.section}", pathLog)
            else:
                createDirectories(pathSaved)
                downSectionC.saveFile(pathSaved, pathLog)

            createLog(downSectionC.downloads, downSectionC.error, pathLog, "generic")

        else:
            downSectionFullC = DownloadAllCourse(args.url)

            if args.author:
                createDirectories(f"{pathSaved}/{args.author}")
                downSectionFullC.saveAllFiles(f"{pathSaved}/{args.author}")
            
    else: color.orange("No es una ruta valida para almacenar el curso")
    print(f'\n\033[?25h', end="") # muestra el cursor
