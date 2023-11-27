import requests
from flask import Flask,g,session
import config
from exts import db
from models import UserModel
from flask_migrate import Migrate
from auth import bp as auth_bp
from sc import bp as sc_bp
from tc import bp as tc_bp
from flask import Blueprint,render_template,request,redirect,url_for,session
from form import LoginForm
from models import UserModel
#/auth
bp=Blueprint("auth",__name__,url_prefix="/auth")
app=Flask(__name__)
#绑定配置文件
app.config.from_object(config)
import subprocess
db.init_app(app)

migrate=Migrate(app,db)

app.register_blueprint(auth_bp)
app.register_blueprint(sc_bp)
app.register_blueprint(tc_bp)
import unittest
class testDemo(unittest.TestCase):



    def test_01(self):
        urlname = "http://127.0.0.1:5000/auth/login"
        data = {'id':21301083,'password':123456789}
        res = requests.post(url=urlname,json=data)
        print(res.status_code)
        self.assertEqual(res.status_code,200)

    def test_02(self):
        urlname = "http://127.0.0.1:5000/tc/course"
        res = requests.get(url=urlname)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)

    def test_03(self):
        urlname = "http://127.0.0.1:5000/tc/teacher/1"
        res = requests.get(url=urlname)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)
    def test_04(self):
        urlname = "http://127.0.0.1:5000/tc/teacher/1/1"
        res = requests.get(url=urlname)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)
    def test_05(self):
        urlname = "http://127.0.0.1:5000/tc/teacher/1/1/state"
        res = requests.get(url=urlname)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)
    def test_06(self):
        urlname = "http://127.0.0.1:5000/tc/teacher/1/1/state/21301083"
        res = requests.get(url=urlname)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)

    def test_07(self):
        urlname = "http://127.0.0.1:5000/tc/teacher/1/1/analysis"
        res = requests.get(url=urlname)
        print(res.status_code)
        self.assertEqual(res.status_code, 200)







