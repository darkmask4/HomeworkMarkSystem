import wtforms
from wtforms.validators import Length

class LoginForm(wtforms.Form):
    id = wtforms.StringField(validators=[Length(min=3, max=20, message="学工号格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])