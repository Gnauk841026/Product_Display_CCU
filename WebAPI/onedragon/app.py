from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager
from user.user import Users
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    # 假設您從資料庫查詢到了一些數據，並將其儲存在一個列表中
    rows = [{'date': '2024-03-31', 'time': '10:36:47', 'name': '示例商品名稱', 'Discount': '10%', 'price': '100'}]
    # 現在將這個列表作為參數傳遞給模板
    return render_template('index.html', rows=rows)



app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Awesome Project",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0.0",
            # Swagger setting to set authorization
            securityDefinitions={
                "bearer": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                }
            },
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
        "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",  # URI to access UI of API Doc
    }
)
docs = FlaskApiSpec(app)

api = Api(app)


api.add_resource(Users, "/users")
docs.register(Users)

if __name__ == "__main__":
    # Remembet to initial JWTManger before running app
    CORS(app)
    jwt = JWTManager().init_app(app)
    app.run(host="0.0.0.0", port=10101, debug=True)