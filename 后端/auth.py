from flask import Blueprint,render_template,request,redirect,url_for,session
from form import LoginForm
from models import UserModel
#/auth
bp=Blueprint("auth",__name__,url_prefix="/auth")

#/auth/login
#GET：从后端获取数据POST：将前端数据提交给后端
@bp.route("/login", methods=['GET', 'POST'])
def login():
     if request.method == 'GET':
         return render_template("denglu.html")
     else:
         form=LoginForm(request.form)
         if form.validate():
            id=form.id.data
            password=form.password.data
            user=UserModel.query.filter_by(id=id).first()
            if not user:
               print("用户在数据库中不存在！")
               return redirect(url_for("auth.login"))
            if user.password==password and user.role=="1":
               session['user_id'] = user.id
               return redirect(url_for("sc.course"))
            if user.password==password and user.role=="0":
               session['user_id'] = user.id
               return redirect(url_for("tc.course"))
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
         else:
             print(form.errors)
             return redirect(url_for("auth.login"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
         