from os import path
from subprocess import PIPE, Popen
import shlex
from config import settings

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
        command = f'pg_dump -h {settings.database_hostname} -d {settings.database_name} -U {settings.database_username} > {filename}'
        # pg_dump -U postgres -h localhost -F c -b -v -f rounds.dump chapito
        # pg_dump -U postgres -h localhost -F c -b -v -f games.dump chapito
        # pg_dump -U postgres -h localhost -F c -b -v -f players.dump chapito
        
        p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE)
        
        password_bytes = f'{settings.database_password}\n'.encode('utf-8')

        print("Database dumped")
        return p.communicate(input=password_bytes)
        
    ## Not finished ##
    def import_database():
        filename = input("Enter export file name: ")
        #command = f'pg_restore -h {settings.database_hostname} -U {settings.database_username} -f {filename}'
        command = f'cat {filename} |psql -U {settings.database_username}'

        # pg_restore -U postgres -h localhost -d chapito -v -t rounds export.dump
        # pg_restore -U postgres -h localhost -d chapito -v -t games export.dump
        # pg_restore -U postgres -h localhost -d chapito -v -t players export.dump

        p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE)

        password_bytes = f'{settings.database_password}\n'.encode('utf-8')

        print("Database imported")
        return p.communicate(input=password_bytes)
        
    functions = [show_rules, dump_database, import_database]