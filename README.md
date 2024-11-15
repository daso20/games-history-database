
# Program to interact with database of players and played games
Available menus on the program: **players**, **games** and **additional_functions**

The rules of the game can be defined in the "rules.txt" file

## Deployment
The Python modules specified in the _requirements.txt_ file need to be installed into the working environment in order to run the scripts. This requires to previously install the dependencies for **psycopg2**. This depends on the Linux flavor the project will be deployed on. For example:
- For **Ubuntu/Debian**:
```
sudo apt-get update
sudo apt-get install libpq-dev python3-dev build-essential
```
- For **CentOS/RHEL**:
```
sudo yum install postgresql-devel python3-devel gcc
```

A Postgres database instance is required to store and manage the data. An _.env_ file needs to be created in the main directory of the project to access the database. It requires the following parameters:
```
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USERNAME=
DATABASE_PASSWORD=
```

## Usage
The following command can be used to start the program:
```
python app
```

The different menus can be accessed by entering an integer assigned to them. For example, in the 'main' menu, the following options are shown:
```
1. Change to 'players' menu
2. Change to 'games' menu
3. Additional functions
4. Exit
Enter a value:
```

If I want to go to the 'games' menu, I would simply enter '2' on the prompt.
