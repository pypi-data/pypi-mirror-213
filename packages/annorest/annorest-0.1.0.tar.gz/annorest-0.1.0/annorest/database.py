#!/usr/bin/env python
# coding: utf-8

import pymongo

# =============================================================================
# 連線資料庫 2021.12.29更新
# =============================================================================
def connect(DATABASE_CFG=None, dbUrl = None):
    if DATABASE_CFG is None and dbUrl is None:
        print("【error】請輸入連線資料庫的參數")
        return -1
    if dbUrl is None:
        host = DATABASE_CFG.get("host", "localhost")
        port = DATABASE_CFG.get("port", 27017)
        user = DATABASE_CFG.get("user", "")
        password = DATABASE_CFG.get("passwd", "")
        auth_source = DATABASE_CFG.get("auth_source", "admin")
        database = DATABASE_CFG.get("database", None)
        if database is None:
            dbUrl = "mongodb://{user}:{password}@{host}:{port}/?authSource={auth_source}".format(user=user, password=password, host = host,port = port, auth_source=auth_source)
        else:
            dbUrl = "mongodb://{user}:{password}@{host}:{port}/{database}?authSource={auth_source}".format(user=user, password=password, host = host,port = port, database=database, auth_source=auth_source)


    #連接資料庫
    try:
        myclient = pymongo.MongoClient(dbUrl)
    except Exception as e: 
        # logger.debug('Retry ' + str(i) + ' times. Retry url = ' + str(url)) 
        print(e)
        return -1
    else:
        print("【success】Connected successfully")
        
    #選擇資料庫
    # db = myclient[database]
    db = myclient
    return db
    # if collectionName == '':
    #     return db
    # else:
    #     #選擇collection
    #     collection = db[collectionName]#In MongoDB, a collection is not created until it gets content!

    #     #collection是否存在
    #     collst = db.list_collection_names()
    #     if collectionName in collst:
    #         print("【info】collection: " + collectionName + " 已存在！")
            
    #     else:
    #         print("【info】collection: " + collectionName + " 不存在！將在新增資料後自動建立")
    #     return collection

# db =  connect()
# main_coll = db[collection]

