from exts import db

class UserModel(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(100),nullable=False)

class CourseModel(db.Model):
    __tablename__="course"
    id=db.Column(db.Integer,primary_key=True)
    coursename=db.Column(db.String(100),nullable=False)

class UCModel(db.Model):
    __tablename__="uc"
    uid=db.Column(db.Integer,primary_key=True)
    cid=db.Column(db.Integer,primary_key=True)

class LHomeworkModel(db.Model):
    __tablename__="lhomework"
    id=db.Column(db.Integer,primary_key=True)
    cid=db.Column(db.Integer,nullable=False)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.String(1000),nullable=True)
    #提交截止时间
    duedate=db.Column(db.DateTime,nullable=True)
    #批阅任务截止时间
    duedate1=db.Column(db.DateTime,nullable=True)
    answer=db.Column(db.String(1000),nullable=True)
    evaluation=db.Column(db.String(1000),nullable=True)


class SHomeworkModel(db.Model):
    __tablename__="shomework"
    id=db.Column(db.Integer,primary_key=True)
    sid=db.Column(db.Integer,nullable=False)
    cid=db.Column(db.Integer,nullable=False)
    lid=db.Column(db.Integer,primary_key=True)
    answer=db.Column(db.String(1000),nullable=True)
    grade=db.Column(db.Integer,nullable=True)
    #待完成/已提交/已过期/待批阅/学生批阅/教师批阅
    state=db.Column(db.String(100),nullable=False)