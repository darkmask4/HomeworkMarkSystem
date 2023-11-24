from flask import Blueprint,render_template,request,session,url_for,redirect,jsonify
from models import UserModel,CourseModel,UCModel,LHomeworkModel,SHomeworkModel
from sqlalchemy import or_
from exts import db
from datetime import datetime

bp=Blueprint("sc",__name__,url_prefix="/sc")

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
            links=['student/'+str(id) for id in courses_id]
            zipped_data = zip(course_name, links)
            items = [{'name': name, 'lianjie': link} for name, link in zipped_data]
            return render_template("student.html",items=items)

@bp.route('/student/<int:course_id>',methods=['GET','POST'])
def student(course_id):
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            title_1=[]
            lid_1=[]
            titles=LHomeworkModel.query.filter_by(cid=course_id).all()
            for title in titles:
                shomework=SHomeworkModel.query.filter_by(lid=title.id,sid=user_id).first()
                if title.duedate1:
                    if title.duedate1<datetime.now() and shomework.state=='待互评':
                        shomework.state='互评过期'
                if title.duedate:
                    if title.duedate<datetime.now() and shomework.state=='待完成':
                        shomework.state='已过期'
                db.session.commit()
                lid_1.append(str(title.id))
                title_1.append(title.title+'('+shomework.state+')')
            zipped_data = zip(title_1, lid_1)
            items = [{'name': name, 'value':lid} for name,lid in zipped_data]
            return render_template("kecheng.html",items=items)
        
@bp.route('/update1/<int:lid>',methods=['GET','POST'])
def update1(lid):
    contents=LHomeworkModel.query.filter_by(id=lid).first()
    user_id=session.get("user_id")
    shomework=SHomeworkModel.query.filter_by(sid=user_id,lid=lid).first()
    new_value=contents.content
    newvalue=shomework.answer
    yijing=1
    if newvalue:
        yijing=2
    return jsonify({'new_value':new_value,'newvalue':newvalue,'yijing':yijing})
    
@bp.route('/discuse',methods=['GET','POST'])
def discuss():
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            return render_template("taolunqu.html")

#批改
@bp.route('/pigai/<int:lid>',methods=['GET','POST'])
def pigai(lid):
    if request.method=='GET':
        user_id=session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        else:
            a=1
            answer1=''
            answer2=''
            answer3=''
            answer4=''
            answer5=''
            answer6=''
            sno1=''
            sno2=''
            sno3=''
            sno4=''
            sno5=''
            sno6=''
            lhomework=LHomeworkModel.query.get(lid)
            cid=lhomework.cid
            answer=lhomework.answer
            max = SHomeworkModel.query.filter(SHomeworkModel.lid == lid,or_(SHomeworkModel.state == '待互评', SHomeworkModel.state == '已互评')).count()
            if lhomework.evaluation=='0':
                shomeworks = SHomeworkModel.query.filter(SHomeworkModel.lid == lid,or_(SHomeworkModel.state == '待互评', SHomeworkModel.state == '已互评'),SHomeworkModel.sid != user_id).order_by(SHomeworkModel.id).all()
                for shomework in shomeworks:
                    if a==1:
                        answer1=shomework.answer
                        sno1=shomework.sid
                    if a==2:
                        answer2=shomework.answer
                        sno2=shomework.sid
                    if a==3:
                        answer3=shomework.answer
                        sno3=shomework.sid
                    if a==4:
                        answer4=shomework.answer
                        sno4=shomework.sid
                    if a==5:
                        answer5=shomework.answer
                        sno5=shomework.sid
                    a=a+1
                return render_template("pigai.html",cid=cid,sno1=sno1,sno2=sno2,sno3=sno3,sno4=sno4,sno5=sno5,sno6=sno6,lid=lid,answer=answer,max=max-1,answer1=answer1,answer2=answer2,answer3=answer3,answer4=answer4,answer5=answer5,answer6=answer6)
            else:
                a=1
                lists = [int(char) for char in lhomework.evaluation]
                shomeworks = SHomeworkModel.query.filter(SHomeworkModel.lid == lid,or_(SHomeworkModel.state == '待互评', SHomeworkModel.state == '已互评')).order_by(SHomeworkModel.id).all()
                user_id_index = next((index for index, sh in enumerate(shomeworks) if sh.sid == user_id), None)
                for list in lists:
                    if a==1:
                        if user_id_index + list < len(shomeworks):
                            answer1=shomeworks[user_id_index + list].answer
                            sno1=shomeworks[user_id_index + list].sid
                        else:
                            answer1=shomeworks[user_id_index + list-len(shomeworks)].answer
                            sno1=shomeworks[user_id_index + list-len(shomeworks)].sid
                    if a==2:
                        if user_id_index + list < len(shomeworks):
                            answer2=shomeworks[user_id_index + list].answer
                            sno2=shomeworks[user_id_index + list].sid
                        else:
                            answer2=shomeworks[user_id_index + list-len(shomeworks)].answer
                            sno2=shomeworks[user_id_index + list-len(shomeworks)].sid
                    if a==3:
                        if user_id_index + list < len(shomeworks):
                            answer3=shomeworks[user_id_index + list].answer
                            sno3=shomeworks[user_id_index + list].sid
                        else:
                            answer3=shomeworks[user_id_index + list-len(shomeworks)].answer
                            sno3=shomeworks[user_id_index + list-len(shomeworks)].sid
                    if a==4:
                        if user_id_index + list < len(shomeworks):
                            answer4=shomeworks[user_id_index + list].answer
                            sno4=shomeworks[user_id_index + list].sid
                        else:
                            answer4=shomeworks[user_id_index + list-len(shomeworks)].answer
                            sno4=shomeworks[user_id_index + list-len(shomeworks)].sid
                    if a==5:
                        if user_id_index + list < len(shomeworks):
                            answer5=shomeworks[user_id_index + list].answer
                            sno5=shomeworks[user_id_index + list].sid
                        else:
                            answer5=shomeworks[user_id_index + list-len(shomeworks)].answer
                            sno5=shomeworks[user_id_index + list-len(shomeworks)].sid
                    if a==6:
                        if user_id_index + list < len(shomeworks):
                            answer6=shomeworks[user_id_index + list].answer
                            sno6=shomeworks[user_id_index + list].sid
                        else:
                            answer6=shomeworks[user_id_index + list-len(shomeworks)].answer
                            sno6=shomeworks[user_id_index + list-len(shomeworks)].sid
                    a=a+1
                return render_template("pigai.html",cid=cid,sno1=sno1,sno2=sno2,sno3=sno3,sno4=sno4,sno5=sno5,sno6=sno6,lid=lid,answer=answer,max=6,answer1=answer1,answer2=answer2,answer3=answer3,answer4=answer4,answer5=answer5,answer6=answer6)

#提交作业及修改作业
@bp.route('/post',methods=['GET','POST'])
def post():
    if request.method=='POST':
        data=request.json
        user_id=session.get("user_id")
        lid=data.get('lid')
        content=data.get('content')
        shomework=SHomeworkModel.query.filter_by(sid=user_id,lid=lid).first()
        shomework.answer=content
        shomework.state='已提交'
        db.session.commit()
        return jsonify({'message': '成功处理请求'})

#互评作业
@bp.route('/post2',methods=['GET','POST'])
def post2():
    if request.method=='POST':
        data=request.json
        user_id=session.get("user_id")
        lid=data.get('lid')
        sno1=data.get('sno1')
        sno2=data.get('sno2')
        sno3=data.get('sno3')
        sno4=data.get('sno4')
        sno5=data.get('sno5')
        sno6=data.get('sno6')
        grade1=data.get('grade1')
        grade2=data.get('grade2')
        grade3=data.get('grade3')
        grade4=data.get('grade4')
        grade5=data.get('grade5')
        grade6=data.get('grade6')
        # a=1
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sno1).first()
        if shomework.grade:
            shomework.grade=(int(grade1)+shomework.grade)/2
        else:
            shomework.grade=grade1
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sno2).first()
        if shomework.grade:
            shomework.grade=(int(grade2)+shomework.grade)/2
        else:
            shomework.grade=grade2
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sno3).first()
        if shomework.grade:
            shomework.grade=(int(grade3)+shomework.grade)/2
        else:
            shomework.grade=grade3
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sno4).first()
        if shomework.grade:
            shomework.grade=(int(grade4)+shomework.grade)/2
        else:
            shomework.grade=grade4
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sno5).first()
        if shomework.grade:
            shomework.grade=(int(grade5)+shomework.grade)/2
        else:
            shomework.grade=grade5
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=sno6).first()
        if shomework.grade:
            shomework.grade=(int(grade6)+shomework.grade)/2
        else:
            shomework.grade=grade6
        # shomeworks=SHomeworkModel.query.filter(SHomeworkModel.lid == lid,or_(SHomeworkModel.sid == sno1, SHomeworkModel.sid == sno2,SHomeworkModel.sid == sno3,SHomeworkModel.sid == sno4,SHomeworkModel.sid == sno5,SHomeworkModel.sid == sno6)).all()
        # for shomework in shomeworks:
        #     if shomework.grade:
        #         if a==1:
        #             shomework.grade=(int(grade1)+shomework.grade)/2
        #         if a==2:
        #             shomework.grade=(int(grade2)+shomework.grade)/2
        #         if a==3:
        #             shomework.grade=(int(grade3)+shomework.grade)/2
        #         if a==4:
        #             shomework.grade=(int(grade4)+shomework.grade)/2
        #         if a==5:
        #             shomework.grade=(int(grade5)+shomework.grade)/2
        #         if a==6:
        #             shomework.grade=(int(grade6)+shomework.grade)/2
        #     else:
        #         if a==1:
        #             shomework.grade=grade1
        #         if a==2:
        #             shomework.grade=grade2
        #         if a==3:
        #             shomework.grade=grade3
        #         if a==4:
        #             shomework.grade=grade4
        #         if a==5:
        #             shomework.grade=grade5
        #         if a==6:
        #             shomework.grade=grade6
        #     a=a+1
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=user_id).first()
        shomework.state='已互评'
        db.session.commit()
        return jsonify({'message': '成功处理请求'})

#判断作业是否截至
@bp.route('/judge/<int:lid>',methods=['GET','POST'])
def judge(lid):
    if request.method=='GET':
        a=False
        lhomework=LHomeworkModel.query.get(lid)
        if(lhomework.duedate>datetime.now()):
            a=True
        return jsonify({'message':str(a)})

@bp.route('/judge1/<int:lid>',methods=['GET','POST'])
def judge1(lid):
    if request.method=='GET':
        user_id=session.get("user_id")
        a=False
        shomework=SHomeworkModel.query.filter_by(lid=lid,sid=user_id).first()
        if shomework.state=='待互评':
            a=True
        return jsonify({'message':str(a)})