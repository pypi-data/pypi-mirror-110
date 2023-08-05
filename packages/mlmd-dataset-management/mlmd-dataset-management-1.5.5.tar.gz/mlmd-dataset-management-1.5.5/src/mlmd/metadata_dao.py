import dotenv
import mysql.connector as connector
import os

dotenv.load_dotenv("env/.env-dev")
def get_db_connection():
    connection = connector.connect(
    host=os.environ.get("MLMD_HOST"),
    user=os.environ.get("MLMD_USER"),
    password=os.environ.get("MLMD_PASSWORD"),
    database=os.environ.get("MLMD_DB")
    )
    return connection

connection = get_db_connection()
if connection is None:
    raise Exception("Cannot connect to mlmd database")

def execute_query(query, parameters_array, commit=True):
    global connection
    if connection.is_closed():
        connection = get_db_connection()
    dbcursor = connection.cursor()
    dbcursor.executemany(query, parameters_array)
    if commit:
        connection.commit()
    r = dbcursor.rowcount
    dbcursor.close()
    return r

def execute_select_query(query, parameters, commit=True):
    global connection
    if connection.is_closed():
        connection = get_db_connection()
    dbcursor = connection.cursor()
    dbcursor.execute(query, parameters)
    r = dbcursor.fetchall()
    if commit:
        connection.commit()
    dbcursor.close()
    return r

def insert_image_metadata_bulk(obj_arr, return_ids=False):
    """Insert multiple image image metadata

        Parameters:
        obj_arr (array): array of tuple of (image_name, tenant_id, dataset_id)

        Returns:
        Any
    """
    if len(obj_arr) <= 0:
        print("Nothing to insert")
        return False

    _query = """INSERT INTO image_metadata(image_name, tenant_id, dataset_id, annotation) VALUES (%s, %s, %s, %s) 
                ON DUPLICATE KEY UPDATE tenant_id=VALUES(tenant_id), dataset_id=VALUES(dataset_id), annotation=VALUES(annotation)"""
    if return_ids:
        global connection
        if connection.is_closed():
            connection = get_db_connection()
        connection.start_transaction()
        last_id = 0
        inserted_last_id_struct = execute_select_query("SELECT image_id from image_metadata order by image_id desc limit 1", None, commit=False)
        if len(inserted_last_id_struct) > 0:
            last_id = inserted_last_id_struct[0][0]
        execute_query(_query, obj_arr, commit=False)
        image_id_struct = execute_select_query("SELECT image_id FROM image_metadata where image_id > %s", (last_id,))
        connection.commit()
        return [image_id for (image_id,) in image_id_struct]

    return execute_query(_query, obj_arr)

def insert_image_log_bulk(obj_arr):
    """Insert multiple image log

        Parameters:
        obj_arr (array): array of tuple of (image_id, execution_id, version_id, dataset_id)

        Returns:
        Any
    """
    return execute_query("INSERT INTO image_log(image_id, execution_id, version_id, dataset_id) VALUES (%s, %s, %s, %s)", obj_arr)

def insert_tenants(obj_arr):
    return execute_query("INSERT IGNORE INTO tenant(tenant_name) VALUES (%s)", obj_arr)

def get_image_executions_by_version(version_id):
    data = execute_select_query("""SELECT im.image_id, im.image_name, ex.type_id FROM image_log il 
    LEFT JOIN image_metadata im ON il.image_id = im.image_id 
    LEFT JOIN Execution ex ON ex.id = il.execution_id
    WHERE il.version_id = %s ORDER BY il.id desc""", (version_id,))
    return [{"image_id": item[0], "image_name": item[1], "execution_id": item[2]} for item in data]

def get_image_by_dataset(dataset_id):
    return execute_select_query("SELECT * FROM image_metadata where dataset_id = %s", (dataset_id,))

def get_tenant_id(tenant_name):
    r = execute_select_query("SELECT id FROM tenant where tenant_name = %s", (tenant_name,))
    if len(r) > 0:
      return r[0][0]
    return None

def get_model_info_by_dataset(datasetname):
    r = execute_select_query("SELECT id, model_name, model_type, training_queue, training_dataset FROM model_info where training_dataset = %s", (datasetname,))    
    return [{"id":item[0], "model_name": item[1], "model_type": item[2], "training_queue":item[3]} for item in r]

