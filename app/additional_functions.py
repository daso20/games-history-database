from os import path
from subprocess import PIPE, Popen
import shlex
from config import settings
from utils import file_exists

class AdditionalFunctions():
    options = ["Show rules", "Dump database", "Import database", "Back"]
    length = len(options)

    def show_rules():
        basepath = path.dirname(__file__)
        rules_path = path.abspath(path.join(basepath, "..", "rules.txt"))
        
        with open(rules_path, "r") as file:
            data = file.read()
            print(data)

    ## Not finished ##
    def dump_database():
        filename = input("Enter file name for export: ")
        command = f'pg_dump -Fc {settings.database_name} > {filename}'
        
        p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE)
        
        password_bytes = f'{settings.database_password}\n'.encode('utf-8')

        print("Database dumped")
        return p.communicate(input=password_bytes)
        
    ## Not finished ##
    def import_database():
        filename = input("Enter export file: ")
        #call(f'pg_restore -d {settings.database_name} {filename}', shell=True)
        print("Database imported")

    functions = [show_rules, dump_database, import_database]