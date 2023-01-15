from flask import *
import os
import boto3 
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv
load_dotenv()
import uuid
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_database = os.getenv("MYSQL_DATABASE")
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key=os.getenv("AWS_SECRECT_ACCESS_KEY")
s3 = boto3.resource('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="ap-northeast-1")

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    host=mysql_host,
    user=mysql_username,
    password=mysql_password ,
    database=mysql_database,
    pool_name = "week1_pool",
    pool_size = 5,
    pool_reset_session = True,
)
@app.route("/api/images",methods=["POST"])
def updateImg():
    img=request.files["img"]
    data=request.form
    content = data["content"]
    
    img_filename = str(uuid.uuid4()) + ".jpg"
    s3.Bucket('homeworktest').put_object(Key=img_filename, Body=img)
    url="https://d25ygub1ioufsy.cloudfront.net/"+ img_filename
    connection_object = connection_pool.get_connection()
    mycursor=connection_object.cursor()
    try:
        mycursor.execute("INSERT INTO graphic (content, photo ) VALUES (%s, %s)" ,(content,url))
        connection_object.commit()
        
        mycursor.close()
        connection_object.close()
        data={
            "content":content,
            "photo":url
        }
        json_result=jsonify(data)
        return make_response(json_result,200) 
    except Exception as e:
        # print(e)
        data={
            "error": True,
            "message":e
        }
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result,500
   
@app.route("/api/images",methods=["GET"])
def checkImg():
    connection_object = connection_pool.get_connection()
    mycursor=connection_object.cursor(dictionary=True)
    try:
        mycursor.execute("SELECT * FROM graphic")
        results = mycursor.fetchall()

        mycursor.close()
        connection_object.close()
        json_result=jsonify(results)
        return make_response(json_result,200) 
    except Exception as e:
        data={
            "error": True,
            "message":e
        }
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result,500
   
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',)