import csv
import sys
sys.path.append("..")
import types
import time
import aminofix as af
import json
import os
from .log import Log
from .input import Input
from constant import PATH_TO_SAVE

import mysql.connector
from pymongo import MongoClient


class MongoDatabase:
    __slots__ = ('currDb')


    def __init__(self, link: str, databaseName: str):
        Log.print_info_msg('Try to connect to database...')
        currConnection = MongoClient(link)
        self.currDb = currConnection[databaseName]
        Log.print_info_msg('Connection is created')


    def __del__(self):
        Log.print_info_msg('Try to close connection...')
        currDb.close()
        Log.print_info_msg('Connection is closed')

    
    def createCollection(self, collectionName: str) -> None:
        Log.print_info_msg('Try to create collection...')
        self.currDb.createCollection(name=collectionName)
        Log.print_info_msg('Collection is created')


    def insertData(self, collectionName: str, users: list) -> None:
        Log.print_info_msg('Try to insert data...')
        currCollection = currDb[collectionName] 
        currCollection.insert_many(users)
        Log.print_info_msg('Data is added')


class SqlDatabase:
    __slots__ = ('currDb')


    def __init__(self, host: str, username: str, password: str, database: str):
        Log.print_info_msg('Try to connect to database...')
        self.currDb = mysql.connector.connect(
                        host=host,
                        user=username,
                        password=password,
                        database=database
                    ).cursor()
        Log.print_info_msg('Connection is created')


    def __del__(self):
        Log.print_info_msg('Try to close connection...')
        currDb.close()
        Log.print_info_msg('Connection is closed')


    def createTable(self, tableName: str, tableColumnsNames: dict) -> None:
        Log.print_info_msg(f'Try to create table \'{tableName}\'...')

        tableCreationQuery = f'CREATE TABLE {tableName} ('

        for currColumnName, currColumnsType in tableColumnsNames.items():
            tableCreationQuery += f'{currColumnName} {currColumnsType}, '

        tableCreationQuery = tableCreationQuery[:-2]
        tableCreationQuery += ')'

        self.currDb.cursor().execute(tableCreationQuery)
        self.currDb.commit()
        Log.print_info_msg('Table is created')


    # @user: list of dicts (!!!)
    def insertData(tableName: str, users: list) -> None:
        Log.print_info_msg('Try to instert data in table \'{tableName}\'...')

        columnNames = list(users[0].keys())
        
        tupleValuesToInsert = []
        for currUser in users:
            tupleValuesToInsert.append(tuple(currUser.values()))

        columnNamesValuesQuery = "%s," * len(columnNames)
        columnNamesValuesQuery = columnNamesValuesQuery[:-1]  
        
        tableInstertionQuery = f'INSERT INTO {tableName} VALUES ({columnNamesValuesQuery})'

        self.currDb.cursor().executemany(tableInstertionQuery)
        self.currDb.commit()
        Log.print_info_msg('Data is added')


class Save:
    @staticmethod
    def saveMongo(collectionName: str, users: list) -> None:
        Log.print_warning_msg(f'Current amount of users - {len(users)}')
        Log.print_warning_msg('Make sure your database is created and running')
        
        dataBase = None
        while True:
            link = Input.input('Link for mongo. (Example - mongodb://localhost:27017/)')

            try:
                dataBase = MongoDatabase(link)
                break
            except:
                Log.print_error_msg(f'Something went wrong: { e }')
    
        dataBase.createCollection(collectionName)
        dataBase.insertData(collectionName, users)


    @staticmethod
    def saveSql(tableName: str, users: list) -> None:
        Log.print_warning_msg(f'Current amount of users - {len(users)}')
        Log.print_warning_msg('Make sure your database is created')

        while True:
            host = Input.input('Host')
            username = Input.input('Username')
            password = Input.input('Password')
            database = Input.input('Database name')

            try:
                dataBase = SqlDatabase(host, username, password, database)
                break
            except mysql.connector.Error as e:
                Log.print_error_msg(f'Something went wrong: { e }')
        
        tableColumns = {}
        for columnName, columnType in users[0].items():
            if type(columnType) == str:
                tableColumns[columnName.upper()] = 'VARCHAR(36)'
            elif type(columnType) == int:
                tableColumns[columnName.upper()] = 'SMALLINT'

        dataBase.createTable(tableName, tableColumns)
        dataBase.insertData(tableName, users)


    @staticmethod
    def saveJson(fileName: str, users: list) -> None:
        Log.print_warning_msg(f'Current amount of users - {len(users)}')

        fileName += '.json'
        pathToSaveFile = PATH_TO_SAVE + fileName 

        with open(pathToSaveFile, 'w', encoding='UTF8') as f:
            f.write(json.dumps(users, indent=4))

        Log.print_info_msg(f'Data is saved. Filename - \"{fileName}\"')
        Input.input('Press any key too continue...')


    @staticmethod
    def saveCsv(fileName: str, users: list) -> None:
        Log.print_warning_msg(f'Current amount of users - {len(users)}')

        fileName += '.csv'
        pathToSaveFile = PATH_TO_SAVE + fileName 

        fieldnamesCsv = list(users[0].keys())

        with open(pathToSaveFile, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnamesCsv)
            writer.writeheader()
            writer.writerows(users)

        Log.print_info_msg(f'Data is saved. Filename - \"{fileName}\"')
        Input.input('Press any key too continue...')


    @staticmethod
    def chooseSaveType() -> types.FunctionType:
        functions = {
            '1': Save.saveCsv,
            '2': Save.saveJson
        }
    
        Log.print_info_msg('\n1. In csv\n2. In json')
        ch = Input.input('Choice (1 | 2): ')

        return functions.get(ch)


async def login(email: str, password: str, useRandomDeviceId: bool = False) -> af.asyncfix.Client:
    client = af.asyncfix.Client()
        
    await client.login(email, password)
    Log.print_info_msg('Logged in')
        
    return client


async def chooseCom(client: af.asyncfix.Client) -> af.asyncfix.SubClient:
    try:
        clientList = await client.sub_clients(size=100)
    except Exception as e:
        Log.print_error_msg(exception=e)
        raise e

    i = 1
    for name, comID, uc in zip(clientList.name, clientList.comId, clientList.usersCount):
        print(f"{i}: {name}\n\tId: {comID}\n\tNumber of users: {uc}")
        i += 1

    community = int(Input.input(f'Choose a community (1 - {i-1})'))
    comId = clientList.comId[community - 1]
    
    try:
        subClient = af.asyncfix.SubClient(comId=comId, profile=client.profile, deviceId=client.device_id)
    except Exception as e:
        Log.print_error_msg(exception=e)
        raise e
    
    return subClient
