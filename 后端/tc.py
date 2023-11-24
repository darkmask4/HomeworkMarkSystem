from flask import Blueprint,render_template,request,session,url_for,redirect,jsonify
from models import UserModel,CourseModel,UCModel,LHomeworkModel,SHomeworkModel
from sqlalchemy import or_
from datetime import datetime
from exts import db
import random

bp=Blueprint("tc",__name__,url_prefix="/tc")

#选课程
@bp.route('/course',methods=['GET','POST'])
def course():
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            courses_id=[]
            course_name=[]
            coursesid=UCModel.query.filter_by(uid=user_id).all()
            for course in coursesid:
                courses_id.append(course.cid)
            coursesname=CourseModel.query.filter(or_(*[CourseModel.id == course_id for course_id in courses_id])).all()
            for course in coursesname:
                course_name.append(course.coursename)
            links=['teacher/'+str(id) for id in courses_id]
            zipped_data = zip(course_name, links)
            items = [{'name': name, 'lianjie': link} for name, link in zipped_data]
            return render_template("student.html",items=items)

#选作业
@bp.route('/teacher/<int:course_id>',methods=['GET','POST'])
def teacher(course_id):
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            course_1=CourseModel.query.filter_by(id=course_id).first()
            course=course_1.coursename
            return render_template("jiaoshike.html",course=course,course_id=course_id)

#作业数据
@bp.route('/homework-data/<int:course_id>')
def get_homework_data(course_id):
    homeworkid=[]
    homeworklist=[]
    homeworks=LHomeworkModel.query.filter_by(cid=course_id).all()
    for homework in homeworks:
        homeworklist.append(homework.title)
        homeworkid.append(homework.id)
    links=[str(course_id)+'/'+str(id) for id in homeworkid]
    zipped_data=zip(homeworkid,homeworklist,links)
    homework_data=[{'id': id,'name':name,'lianjie': link}for id,name,link in zipped_data]
    return jsonify(homework_data)

#添加作业
@bp.route('/submit1',methods=['GET','POST'])
def submit1():
    if request.method=='GET':
        item_count = LHomeworkModel.query.count()
        if item_count>0:
            count = LHomeworkModel.query.order_by(LHomeworkModel.id.desc()).first().id+1
            return jsonify({'count':str(count)})
        else:
            return jsonify({'count':0})
    if request.method=='POST':
        item_count = LHomeworkModel.query.count()
        if item_count>0:
            count = LHomeworkModel.query.order_by(LHomeworkModel.id.desc()).first().id
        else:
            count=0
        data = request.json
        homework_name = data.get('homeworkName')
        cid=data.get('course_id')
        new_homework=LHomeworkModel(id=count+1,cid=cid,title=homework_name)
        
        s_ids=[]
        sids=UserModel.query.filter_by(role='1').all()
        for sid in sids:
            s_ids.append(sid.id)
        s_id=UCModel.query.filter(or_(*[UCModel.uid == u_id for u_id in s_ids]),UCModel.cid==cid).all()
        s_ids=[]
        for sid in s_id:
            s_ids.append(sid.uid)
        item_count1 = SHomeworkModel.query.count()
        if item_count1>0:
            count1=SHomeworkModel.query.order_by(SHomeworkModel.id.desc()).first().id
        else:
            count1=0
        for s_id1 in s_ids:
            new_homework1=SHomeworkModel(id=count1+1,sid=s_id1,cid=cid,lid=count+1,state='待发布')
            db.session.add(new_homework1)
            count1=count1+1
        db.session.add(new_homework)
        db.session.commit()
        return jsonify({'message': '成功处理请求'})

#删除作业
@bp.route('/delete1',methods=['GET','POST'])
def delete1():
    if request.method=='POST':
        data=request.json
        id=data.get('id')
        item=LHomeworkModel.query.get(id)
        items=SHomeworkModel.query.filter_by(lid=id).all()
        for item1 in items:
            db.session.delete(item1)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})

#清空作业
@bp.route('/delete2',methods=['GET','POST'])
def delete2():
    if request.method=='POST':
        data=request.json
        cid=data.get('cid')
        items=LHomeworkModel.query.filter_by(cid=cid).all()
        items1=SHomeworkModel.query.filter_by(cid=cid).all()
        for item in items:
            db.session.delete(item)
        for item in items1:
            db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Items deleted successfully'})

#作业内容
@bp.route('/teacher/<int:course_id>/<int:lid>',methods=['GET','POST'])
def content(course_id,lid):
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            lhomework=LHomeworkModel.query.get(lid)
            content=lhomework.content
            answer=lhomework.answer
            yijing=1
            if content:
                yijing=2
                if answer:
                    yijing=3
            return render_template("xiangqing.html",course_id=course_id,lid=lid,content=content,answer=answer,yijing=yijing)

#完成情况
@bp.route('/teacher/<int:course_id>/<int:lid>/state',methods=['GET','POST'])
def state(course_id,lid):
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            lhomework=LHomeworkModel.query.get(lid)
            shomeworks=SHomeworkModel.query.filter_by(lid=lid).all()
            for shomework in shomeworks:
                if lhomework.duedate1:
                    if lhomework.duedate1<datetime.now() and shomework.state=='待互评':
                        shomework.state='互评过期'
                if lhomework.duedate:
                    if lhomework.duedate<datetime.now() and shomework.state=='待完成':
                        shomework.state='已过期'
            db.session.commit()
            return render_template("zhuangtai.html",lid=lid,course_id=course_id)

#成绩分析
@bp.route('/teacher/<int:course_id>/<int:lid>/analysis',methods=['GET','POST'])
def analysis(course_id,lid):
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            return render_template("fenxi.html",lid=lid,course_id=course_id)

#发布作业
@bp.route('/post1',methods=['GET','POST'])
def post1():
    if request.method=='POST':
        data=request.json
        lid=data.get('lid')
        content=data.get('content')
        duedate=data.get('duedate')
        lhomework=LHomeworkModel.query.get(lid)
        lhomework.content=content
        lhomework.duedate=duedate
        shomeworks=SHomeworkModel.query.filter_by(lid=lid).all()
        for shomework in shomeworks:
            shomework.state='待完成'
        db.session.commit()
        return jsonify({'message': 'Items post successfully'})
    
#召回作业
@bp.route('/callback1',methods=['GET','POST'])
def callback1():
    if request.method=='POST':
        data=request.json
        lid=data.get('lid')
        lhomework=LHomeworkModel.query.get(lid)
        lhomework.content=None
        lhomework.duedate=None
        lhomework.duedate1=None
        lhomework.answer=None
        lhomework.evaluation=None
        shomeworks=SHomeworkModel.query.filter_by(lid=lid).all()
        for shomework in shomeworks:
            shomework.answer=None
            shomework.grade=None
            shomework.state='待发布'
        db.session.commit()
        return jsonify({'message': 'Items callback successfully'})

#互评和发布标准答案
@bp.route('/evaluate/<int:lid>',methods=['GET','POST'])
def evaluate(lid):
    if request.method=='GET':
        a=False
        lhomework=LHomeworkModel.query.get(lid)
        if(lhomework.duedate<datetime.now()):
            a=True
        return jsonify({'message':str(a)})
    if request.method=='POST':
        data=request.json
        answer=data.get('answer')
        duedate=data.get('duedate')
        lhomework=LHomeworkModel.query.get(lid)
        lhomework.duedate1=duedate
        lhomework.answer=answer
        shomeworks=SHomeworkModel.query.filter_by(lid=lid,state='已提交').all()
        a=0
        for shomework in shomeworks:
            shomework.state='待互评'
            a=a+1
        print(a)
        if a>6:
            random_numbers = random.sample(range(1, a), 6)
            result_string = "".join(map(str, random_numbers))
            lhomework.evaluation=result_string
        else:
            lhomework.evaluation='0'
        db.session.commit()
        return jsonify({'message': 'Items post successfully'})

#互评取消
@bp.route('/callback2',methods=['GET','POST'])
def callback2():
    if request.method=='POST':
        data=request.json
        lid=data.get('lid')
        lhomework=LHomeworkModel.query.get(lid)
        lhomework.duedate1=None
        lhomework.answer=None
        lhomework.evaluation=None
        shomeworks=SHomeworkModel.query.filter(SHomeworkModel.lid == lid,SHomeworkModel.state.in_(['待互评', '已互评'])).all()
        for shomework in shomeworks:
            shomework.state='已提交'
        db.session.commit()
        return jsonify({'message': 'Items callback successfully'})

#学生数据
@bp.route('/student-data/<int:lid>')
def get_student_data(lid):
    links=[]
    sno=[]
    sname=[]
    state=[]
    grade=[]
    shomeworks=SHomeworkModel.query.filter(SHomeworkModel.lid == lid).order_by(SHomeworkModel.sid).all()
    for shomework in shomeworks:
        sno.append(shomework.sid)
        state.append(shomework.state)
        grade.append(shomework.grade)
        links.append('state/'+str(shomework.sid))
    students=UserModel.query.filter(or_(*[UserModel.id == u_id for u_id in sno])).order_by(UserModel.id).all()
    for student in students:
        sname.append(student.name)
    zipped_data=zip(sno,sname,state,grade,links)
    student_data=[{'sno': id,'name':name,'state':state,'grade':grade,'lianjie': link}for id,name,state,grade,link in zipped_data]
    return jsonify(student_data)
    
#学生具体情况
@bp.route('/teacher/<int:course_id>/<int:lid>/state/<int:sid>',methods=['GET','POST'])
def state1(course_id,lid,sid):
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            sname=UserModel.query.get(sid).name
            shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sid).first()
            state=shomework.state
            grade=shomework.grade
            content=shomework.answer
            return render_template("xueshengzuoye.html",course_id=course_id,lid=lid,sid=sid,name=sname,state=state,grade=grade,content=content)
        
#教师评分
@bp.route('/grade',methods=['GET','POST'])
def grade():
    if request.method=='POST':
        data=request.json
        lid=data.get('lid')
        sid=data.get('sid')
        grade=data.get('grade')
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sid).first()
        shomework.grade=grade
        db.session.commit()
        return jsonify({'message': 'Items callback successfully'})
    
#作业数据
@bp.route('/grade-data/<int:lid>')
def get_grade_data(lid):
    names=['小于60','60-70','71-80','81-90','91-100']
    values=[0,0,0,0,0]
    homeworks=SHomeworkModel.query.filter_by(lid=lid).all()
    for homework in homeworks:
        if homework.grade:
            if homework.grade<60:
                values[0]=values[0]+1
            if homework.grade>=60 and homework.grade<=70:
                values[1]=values[1]+1
            if homework.grade>70 and homework.grade<=80:
                values[2]=values[2]+1
            if homework.grade>80 and homework.grade<=90:
                values[3]=values[3]+1
            if homework.grade>90 and homework.grade<=100:
                values[4]=values[4]+1
    zipped_data=zip(values,names)
    homework_data=[{'value': value,'name':name}for value,name in zipped_data]
    return jsonify(homework_data)