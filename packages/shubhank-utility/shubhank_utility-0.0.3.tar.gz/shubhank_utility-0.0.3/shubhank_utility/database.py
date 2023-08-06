from pymongo import MongoClient, ReplaceOne, UpdateOne, UpdateMany, InsertOne, DeleteOne, DeleteMany

import logging
logging.basicConfig(level=logging.ERROR)


def insert_one(database_name, collection_name, data, client=MongoClient()):
    """
    This function is used to insert single data into the database. 
    It will only take dict of a record.
    """
    try:
        mydb = client[database_name]
        mycol = mydb[collection_name]
        mycol.insert_one(data)
    
    except Exception as e:
        print(e)
    
    finally:
        client.close()
        

def insert_many(database_name, collection_name, data, client=MongoClient()):
    """
    This function is used to insert all data into the database.
    It can take list of records as well as pandas dataframe.
    """
    try:
        mydb = client[database_name]
        mycol = mydb[collection_name]
        if not isinstance(data, list):
            mycol.insert_many(data.to_dict('records'), ordered=False)
        else:
            mycol.insert_many(data, ordered=False)
    
    except Exception as e:
        print(e)
    
    finally:
        client.close()
        

def fetch_one(database_name, collection_name, query={}, project=None, client=MongoClient()):
    """
    This function is used to fetch single data from the database.
    If query not provided, will return first record.
    """
    results = None
    try:
        db = client[database_name]
        col_name = db[collection_name]
        results = list(col_name.find( query, project ))

    except Exception as e:
        logging.error("\nerror: " + str(e) + "\n")

    finally:
        client.close()
        return results[0] if results else results
    

def fetch_all(database_name, collection_name, query={}, project=None, client=MongoClient()):
    """
    This function is used to fetch all data from the database based on query.
    if query not provided, whole collection will be returned.
    """
    results = None
    try:
        db = client[database_name]
        col_name = db[collection_name]
        results = list(col_name.find( query, project ))

    except Exception as e:
        logging.error("\nerror: " + str(e) + "\n")

    finally:
        client.close()
        return results
    

def delete_one(database_name, collection_name, query={}, client=MongoClient()):
    """
    This function is used to delete one record from the database. 
    """
    try:
        db = client[database_name]
        col_name = db[collection_name]
        col_name.delete_one( query )

    except Exception as e:
        logging.error("\nerror: " + str(e) + "\n")

    finally:
        client.close()
        

def delete_many(database_name, collection_name, query={}, client=MongoClient()):
    """
    This function is used to delete many records from the database based on query.
    If query not provided, all records will be deleted. 
    """
    try:
        db = client[database_name]
        col_name = db[collection_name]
        col_name.delete_many( query )

    except Exception as e:
        logging.error("\nerror: " + str(e) + "\n")

    finally:
        client.close()


def update_one(database_name, collection_name, query={}, update_value={}, client=MongoClient()):
    """
    This function is used to update one record in the database.
    """
    try:
        db = client[database_name]
        col_name = db[collection_name]
        value = {'$set': update_value}
        col_name.update_one(query, value)
        
    except Exception as e:
        logging.error("\nerror: " + str(e) + "\n")
            
    finally:
        client.close()


def update_one(database_name, collection_name, query={}, update_value={}, client=MongoClient()):
    """
    This function is used to update all record in the database based on query.
    """
    try:
        db = client[database_name]
        col_name = db[collection_name]
        value = {'$set': update_value}
        col_name.update_many(query, value)
        
    except Exception as e:
        logging.error("\nerror: " + str(e) + "\n")
            
    finally:
        client.close()
        

def replace_one(database_name, collection_name, query, update_data, client=MongoClient()):
    """
    This function is used to replace one record in the database with updated or new record.
    """
    try:
        db = client[database_name]
        col_name = db[collection_name]
        col_name.replace_one(query, update_data, upsert=True)
        
    except Exception as e:
        logging.error("\nerror: " + str(e) + "\n")
            
    finally:
        client.close()


def bulk_write(database_name, collection_name, data, client=MongoClient()):
    """
    This function is used to bulk write all the data provided.
    """
    try:
        mydb = client[database_name]
        mycol = mydb[collection_name]
        mycol.bulk_write(data)
    
    except Exception as e:
        print(e)
    
    finally:
        client.close()


def get_collection_names(database_name, client=MongoClient()):
    """
    This function is to get the list of collection names.
    """
    try:
        db = client[database_name]
        for col in db.list_collection_names():
            print(col)

    except Exception as e:
        print(e)
    
    finally:
        client.close()