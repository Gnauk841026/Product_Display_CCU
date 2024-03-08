import json
from flask import jsonify
from flask_restful import Resource, reqparse
import util
from . import user_router_model
import pymysql
from flask_jwt_extended import create_access_token, jwt_required
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from datetime import timedelta
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps


def db_init():
    db = pymysql.connect(
        host="127.0.0.1", user="root", password="root", port=3306, db="testdb"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

def role_required(*roles):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] not in roles:
                return {"msg": "Insufficient permissions"}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper



def get_access_token(user,role,id):
    token = create_access_token(
        identity={"user": user},
        additional_claims={"role":role,"id": id}, 
        expires_delta=timedelta(days=1)
    )
    return token

# Swagger setting for auto bring token in API
security_params = [{"bearer": []}]

class Login(MethodResource):
    @doc(description="login API", tags=["Login"])
    @use_kwargs(user_router_model.LoginSchema, location="form")
    @marshal_with(user_router_model.LoginResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account = kwargs["account"]
        password = kwargs["password"]
        sql = f"SELECT * FROM testdb.user WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        print(user)
        db.close()

        if user != ():
            role = user[0]["role"]
            user_id = user[0]["id"]
            token = get_access_token(account,role,user_id)
            return util.success({"token": token})

        return util.failure()


class Users(MethodResource):
    # Get all User
    @doc(description="Get Users info.", tags=["Users"], security=security_params)
    @use_kwargs(user_router_model.UserGetSchema, location="query")
    @marshal_with(user_router_model.UserGetResponse, code=200)
    @role_required('AM', 'SUBAM','NORMAL')
    @jwt_required()
    def get(self, **kwargs):
        db, cursor = db_init()
        name = kwargs.get("name")

        if name is not None:
            sql = f"SELECT * FROM testdb.user WHERE name LIKE '%{name}%';"
        else:
            sql = "SELECT * FROM testdb.user;"

        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)

    # Create User
    @doc(description="Create User.", tags=["User"], security=security_params)
    @use_kwargs(user_router_model.UserPostSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=200)
    @role_required('AM', 'SUBAM')
    @jwt_required()
    def post(self, **kwargs):
        db, cursor = db_init()

        sql = """

        INSERT INTO `testdb`.`user` (`name`,`gender`,`birth`,`note`)
        VALUES ('{}','{}','{}','{}');

        """.format(
            kwargs["name"], kwargs["gender"], kwargs["birth"], kwargs["note"]
        )

        result = cursor.execute(sql)

        db.commit()
        db.close()

        if result == 0:
            return util.failure()

        return util.success()


class User(MethodResource):
    @doc(description="Get Single user info.", tags=["User"],security=security_params)
    @marshal_with(user_router_model.UserGetResponse, code=200)
    @role_required('AM', 'SUBAM','NORMAL')
    @jwt_required()
    def get(self, id):
        verify_jwt_in_request()
        claims = get_jwt()
        user_id = claims["id"]  
        role = claims["role"]
        if role == 'NORMAL' and str(user_id) != str(id):
            return {"msg": "You are not allowed to modify other users' information."}, 403
        db, cursor = db_init()
        sql = f"SELECT * FROM testdb.user WHERE id = '{id}';"
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)

    @doc(description="Update User info.", tags=["User"], security=security_params)
    @use_kwargs(user_router_model.UserPatchSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=201)
    @role_required('AM', 'SUBAM','NORMAL')
    @jwt_required()
    def patch(self, id, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        user_id = claims["id"]  
        role = claims["role"]
        if role == 'NORMAL' and str(user_id) != str(id):
            return {"msg": "You are not allowed to modify other users' information."}, 403
        db, cursor = db_init()
        user = {
            "name": kwargs.get("name"),
            "gender": kwargs.get("gender"),
            "birth": kwargs.get("birth") or "1900-01-01",
            "note": kwargs.get("note"),
            "account": kwargs.get("account"),
            "password": kwargs.get("password"),
        }

        query = []
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)

        sql = """
            UPDATE `testdb`.`user`
            SET {}
            WHERE id = {};
        """.format(
            query, id
        )

        result = cursor.execute(sql)
        db.commit()
        db.close()
        if result == 0:
            return util.failure()

        return util.success()

    @doc(description="Delete User info.", tags=["User"], security=security_params)
    @marshal_with(None, code=204)
    @jwt_required()
    @role_required('AM')
    def delete(self, id):
        db, cursor = db_init()
        sql = f"DELETE FROM `testdb`.`user` WHERE id = {id};"
        cursor.execute(sql)
        db.commit()
        db.close()