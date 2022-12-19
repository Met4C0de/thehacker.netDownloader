import os
import argparse 

from utils.soutils import clear, color, createDirectories, createLog, createPathLog, logo
from utils.DownloadFiles import DownloadSectionCourse, DownloadAllCourse

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
                    type=bool,
                    default=False,
                    required=False,
                    help='Descarga el curso completo')

args = parser.parse_args()

if __name__ == "__main__":
    try:
        logo()
        print(f'\n\033[?25l{color.ORANGE}', end="") # oculta el cursor

        pathSaved = args.folder_save
        pathLog = createPathLog(args.pathlog) 
        
        if os.path.isdir(pathSaved):
            downSectionC  = DownloadSectionCourse(args.url)
            downSectionFullC = DownloadAllCourse(args.url)

            if not args.full_course:
                if args.author and not args.section:
                    createDirectories(f"{pathSaved}/{args.author}")
                    downSectionC.saveFile(f"{pathSaved}/{args.author}")

                elif args.author and args.section:
                    createDirectories(f"{pathSaved}/{args.author}/{args.section}")
                    downSectionC.saveFile(f"{pathSaved}/{args.author}/{args.section}")
                else:
                    createDirectories(pathSaved)
                    downSectionC.saveFile(pathSaved)
                createLog(downSectionC.downloads, downSectionC.error, pathLog)
            else:
                if args.author and not args.section:
                    createDirectories(f"{pathSaved}/{args.author}")
                    downSectionFullC.saveAllFiles(f"{pathSaved}/{args.author}")
                # crear un log personalisado para el curso completo
                
        else: color.orange("No es una ruta valida para almacenar el curso")

    except KeyboardInterrupt: 
        color.red("Saliendo...")
        createLog(downSectionC.downloads, downSectionC.error, pathLog)
    finally:
        print(f'\n\033[?25h', end="") # muestra el cursor
