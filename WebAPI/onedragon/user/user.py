import json
from flask import jsonify
from flask_restful import Resource, reqparse
import util
from . import user_router_model
import pymysql
from flask_jwt_extended import create_access_token, jwt_required
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from datetime import timedelta

def db_init():
    db = pymysql.connect(
        host="127.0.0.1", user="pchome", password="momo", port=3306, db="backup"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

class Users(MethodResource):
    # Get all User
    @doc(description="Get Users info.", tags=["Users"])
    @use_kwargs(user_router_model.UserGetSchema, location="query")
    @marshal_with(user_router_model.UserGetResponse, code=200)
    def get(self, **kwargs):
        db, cursor = db_init()
        platform = kwargs.get("platform")
        name = kwargs.get("name")
        date = kwargs.get("date")

        table_name = "Momo_Flesh_Sale" if platform == "momo" else "pchome_sale"
        sql = f"SELECT date,time,name,discount,price FROM backup.{table_name}"
    
        conditions = []
        if name is not None:
            conditions.append(f"name LIKE '%{name}%'")
        if date is not None:
            conditions.append(f"date LIKE '%{date}%'")
        
        if conditions:
            sql += " WHERE " + " AND ".join(conditions) + ";"
        else:
            sql += ";"
            
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)