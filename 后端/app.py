from flask import Flask,g,session
import config
from exts import db
from models import UserModel
from flask_migrate import Migrate
from auth import bp as auth_bp
from sc import bp as sc_bp
from tc import bp as tc_bp

app=Flask(__name__)
#绑定配置文件
app.config.from_object(config)

db.init_app(app)

migrate=Migrate(app,db)

app.register_blueprint(auth_bp)
app.register_blueprint(sc_bp)
app.register_blueprint(tc_bp)

@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}

if __name__=='__main__':
    app.run()