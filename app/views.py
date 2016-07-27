from flask import render_template, flash, redirect, session, url_for, request, g,abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm,SignUpForm,PostForm, TeacherForm, CollegeForm, CTeacherForm
from .models import User,Teacher,Post
import datetime
#from datetime import datetime, timedelta
from config import POSTS_PER_PAGE
from flask import Blueprint
from flask_paginate import Pagination
import math

#import bcrypt

t = 0
t1 = 0
t2 = 0
curname = ""
curcollege = ""
curcolname = ""
msg = ""

@lm.user_loader
def load_user(id):
    return User.query.get(id)

a = True
user2 = {'nickname': 'Guest'}
@app.route('/')
@app.route('/homepage')
@app.route('/homepage/<int:page>', methods=['GET', 'POST'])
def homepage(page = 1):
    global curcollege
    global curcolname
    curcollege = ""
    curcolname = ""
    global curname
    curname = ""
    adict = {}
    cdict = {}
    ddict = {}
    #page = 1
    #search = False
    #q = request.args.get('q')
    #if q:
        #search = True
    #page = request.args.get('page', type=int, default=1)
    qlist = []
    alist = []
    #user = {'nickname': 'Miguel'}
    #user = g.user
##    posts1 = [{'author':{'nickname':'Aman'},'body':'Hanuman gives average grades','teacher':{'name':'Hanuman'}},
##             {'author':{'nickname':'Rishi'},'body':'Himanshu is a good teacher','teacher':{'name':'Himanshu'}},
##             {'author':{'nickname':'Bumrah'},'body':'Rajesh is too boring','teacher':{'name':'Rajesh'}}]
    
    global a
    if a == True:
        
        return render_template('homepage.html',title="Homepage",user = user2,a=a)
    else:
        
        global user2
        user = User.query.filter_by(nickname = user2['nickname']).first()
        
        college = user.college
        p = Teacher.query.filter_by(college = user.college)
        
        if p == None:
            return render_template('homepage.html',title="Homepage",user = user2)
        else:
            for k in p:
                for j in k.posts.all():
                    adict[j] = datetimert(j.timestamp)
                    qlist.append(j)
                    if j.grade!=None:
                        cdict[j] = checkpanel(float(j.grade))
                        ddict[j] = checkpanel(float(j.rating))

           
            qlist.reverse()
            alist = [i for i in range(1,1+math.ceil(len(qlist)/3))]
            clist = qlist[(page-1)*3:(page*3)]
            
           
        
            return render_template('homepage.html',title="Homepage",user = user2,posts = clist,times= alist,page = page,adict = adict,cdict=cdict,ddict=ddict)
        
            
        

@app.route('/login',methods = ['GET','POST'])
def login():
    global curcollege
    global curcolname
    curcollege = ""
    curcolname = ""
    #if g.user is not None and g.user.is_authenticated:
        #return redirect(url_for('homepage'))
    global msg 
    form = LoginForm()
    if form.validate_on_submit():
        #login_user(user)
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(username = form.username.data).first()
        def userinfo():
            return user
        login_user(user)
        print(user)
        flash("Login requested for Username='%s',Password='%s'" % (user.username,user.password))
        if user:
            if user.password==form.password.data:
                global a
                a = False
                db.session.add(user)
                db.session.commit()
                flash("Login requested for Username='%s',Password='%s'" % (user.username,a))
                user2['nickname'] = user.nickname
                login_user(user,remember = True)
                msg = ""
                return redirect('/homepage')
            else:
                msg = "Login requested is invalid for the username requested. Please enter right details and try again"
                flash(msg)
                return redirect('/login')
    return render_template('login.html',title = "Sign In",form = form,msg=msg)

@app.route('/logout',methods = ['GET'])
def logout():
    global curname
    curname = ""
    logout_user()
    #user = current_user
    #db.session.add(user)
    #db.session.commit()
    #logout_user()
    global a
    a = True
    global user2
    user2['nickname'] = 'Guest'
    return redirect('/homepage')
    

                
        ##next = flask.request.args.get('next')
        #if not next_is_valid(next):
            #return flask.abort
       # flash("Login requested for Username='%s',Password='%s', remember_me=%s" % (form.username.data,str(form.password.data),str(form.remember_me.data)))
        #return redirect('/homepage')
    #return render_template('login.html',title = "Sign In",form = form)

@app.route('/signup',methods = ['GET','POST'])
def signup():
    
    form = SignUpForm()
    if form.validate_on_submit():
        flash("Login requested for Username='%s',Password='%s', email='%s',nickname='%s'" % (form.username.data,str(form.password.data),str(form.emailid.data),form.nickname.data))
        user2['nickname'] = form.nickname.data
        user1 = User(nickname=form.nickname.data, email=form.emailid.data, username = form.username.data,password=str(form.password.data),college = form.college.data)
        db.session.add(user1)
        db.session.commit()
        return redirect('/homepage')
    return render_template('signup.html',title = 'Sign Up',form = form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'),500

@app.route('/post',methods = ['GET','POST'])
#s@login_required
def post():
    global curcollege
    global curcolname
    curcollege = ""
    curcolname = ""
    global curname
    curname = ""
    form = PostForm()
    global user2
    user = User.query.filter_by(nickname = user2['nickname']).first()
    if form.validate_on_submit():
        
        teacher = Teacher(name=form.teacher.data,subject = form.subject.data,college= form.college.data)
        post = Post(body=form.post.data,timestamp = datetime.datetime.utcnow(),author=user,teacher=teacher,grade = form.grade.data,rating = form.rating.data,anon = str(form.anon.data))
        db.session.add(teacher)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('homepage'))
    return render_template('post.html',
                           title='Home',
                           form=form,
                           college=user.college)


@app.route('/teacher_search',methods = ['GET','POST'])
@app.route('/teacher_search/<int:page>', methods=['GET', 'POST'])
def teacher_search(page = 1):
    adict = {}
    global t
    global curcollege
    global curcolname
    curcollege = ""
    curcolname = ""
    t= t+1
    aset = set()
    bdict = {}
    cdict={}
    ddict={}
    posts1 = Post.query.all()
    for na in posts1:
        aset.add(na.teacher.name)
        bdict[na.teacher.name] = na.teacher.college
        
    qlist=[]
    alist = []
    clist = []
    form = TeacherForm()
    sum1 = 0
    sum2 = 0
        
    global curname
    global user2
    if form.teacher.data != None:
        name = form.teacher.data
        curname = name
    else:
        name = curname
   
    if t == 1:
        if form.validate_on_submit():
            flash(name)
            p = Teacher.query.filter_by(name = name)
            
            for k in p:
                
                #if k== None:
                    #flash("No teacher with this name exists in database")
                    #return redirect('/teacher_search')
                #else:
                for j in k.posts.all():
                        adict[j] = datetimert(j.timestamp)
                        cdict[j] = checkpanel(float(j.grade))
                        ddict[j] = checkpanel(float(j.rating))
                        qlist.append(j)
                        if j.grade != None:
                            sum1 = sum1+float(j.grade)
                            sum2 = sum2+float(j.rating)
                
                qlist.reverse()
                alist = [i for i in range(1,1+math.ceil(len(qlist)/2))]
                clist = qlist[(page-1)*2:(page*2)]
                
            
            redirect(url_for('teacher_search'))
            
    else:
        p = Teacher.query.filter_by(name = name)
        sum = 0
        for k in p:
            
            #if k== None:
                #flash("No teacher with this name exists in database")
                #return redirect('/teacher_search')
            #else:
            for j in k.posts.all():
                    qlist.append(j)
                    adict[j] = datetimert(j.timestamp)
                    if j.grade != None and j.rating !=None:
                        sum1 = sum1+float(j.grade)
                        sum2 = sum2+float(j.rating)
                        cdict[j] = checkpanel(float(j.grade))
                        ddict[j] = checkpanel(float(j.rating))
            qlist.reverse()
            alist = [i for i in range(1,1+math.ceil(len(qlist)/2))]
            clist = qlist[(page-1)*2:(page*2)]    
       
        redirect(url_for('teacher_search'))
    
        
    if len(qlist)>0:
    
        return render_template('search_teacher.html',title="Search Teacher",user = user2,form=form,posts = clist,posts1=sorted(aset),times=alist,cdict=cdict,ddict=ddict,avg = round(sum1/len(qlist)),avg1 = round(sum2/len(qlist)),num=len(qlist),page = page,adict = adict,bdict=bdict,image=((round(sum1/len(qlist))+round(sum2/len(qlist)))/2))
    else:
        return render_template('search_teacher.html',title="Search Teacher",user = user2,form=form,posts = clist,posts1=sorted(aset),times=alist,adict = adict,cdict=cdict,ddict=ddict)
        
    

@app.route('/college_search',methods = ['GET','POST'])
@app.route('/college_search/<int:page>', methods=['GET', 'POST'])
def college_search(page = 1):
    sum1 = 0
    sum2 = 0
    global t1
    global curcollege
    global t2
    #t2 = t2+1
    global curcolname
    global curname
    curname = ""
    college =None
    adict = {}
    t1 = t1+1
    aset = set()
    bset = set()
    form = CollegeForm()
    form1 = CTeacherForm()
    posts1 = Post.query.all()
    alist = []
    clist = []
    a1list = []
    c1list = []
    cdict={}
    ddict={}
    
    
    
    if form1.cteacher.data != None and form1.cteacher.data != "":
        
        name = form1.cteacher.data
        curcolname = name
    else:
        
        form1.cteacher.data = curcolname
        name = curcolname
    
    if (form.college.data != "" and form.college.data !=None):
        college = form.college.data
        
        curcollege = college
        form1.cteacher.data = ""
    else:
        #form1.cteacher.data = ""
        college = curcollege
        form.college.data=curcollege
   
        
        
    for na in posts1:
        aset.add(na.teacher.college)
    posts2 = Teacher.query.filter_by(college = curcollege)
    for na in posts2:
        bset.add(na.name)
        
    qlist=[]
    qmlist=[]
    
    
    
    
    
    global user2
    if t1 == 1:
        
        if form.validate_on_submit():
            
            #form1.cteacher.data = None
            
            flash(form1.cteacher.data )
    
            p = Teacher.query.filter_by(college = college)
            for k in p:
                
                #if k== None:
                    #flash("No teacher with this name exists in database")
                    #return redirect('/teacher_search')
                #else:
                for j in k.posts.all():
                        adict[j] = datetimert(j.timestamp)
                        qlist.append(j)
                        if j.grade!=None:
                            cdict[j] = checkpanel(float(j.grade))
                            ddict[j] = checkpanel(float(j.rating))
            qlist.reverse()
            alist = [i for i in range(1,1+math.ceil(len(qlist)/2))]
            
            clist = qlist[(page-1)*2:(page*2)]
            
           
            #redirect(url_for('college_search'))
            
            #return render_template('search_teacher.html',title="Homepage",user = user2,form = form,posts = qlist)
    else:
        
       
        pm = Teacher.query.filter_by(college = college)
        for k in pm:
            
            #if k== None:
                #flash("No teacher with this name exists in database")
                #return redirect('/teacher_search')
            #else:
            for j in k.posts.all():
                    adict[j] = datetimert(j.timestamp)
                    qlist.append(j)
                    if j.grade!=None:
                        cdict[j] = checkpanel(float(j.grade))
                        ddict[j] = checkpanel(float(j.rating))
        qlist.reverse()
        alist = [i for i in range(1,1+math.ceil(len(qlist)/2))]
        
        clist = qlist[(page-1)*2:(page*2)]
        #redirect(url_for('college_search'))
    
    if form1.cteacher.data != None and form1.cteacher.data != "":
    #mif 1<0:
        #if form1.validate_on_submit():
        flash("im freee")
        p = Teacher.query.filter_by(name = name,college=college)
        
        for k in p:
            
            #if k== None:
                #flash("No teacher with this name exists in database")
                #return redirect('/teacher_search')
            #else:
            for j in k.posts.all():
                    adict[j] = datetimert(j.timestamp)
                    qmlist.append(j)
                    if j.grade != None:
                       
                        sum1 = sum1+float(j.grade)
                        sum2 = sum2+float(j.rating)
        qmlist.reverse()
        a1list = [i for i in range(1,1+math.ceil(len(qmlist)/2))]
        
        c1list = qmlist[(page-1)*2:(page*2)]
        
        
        redirect(url_for('college_search'))
##    else:
##        
##           
##        flash(name)
##        flash(curcolname)
##        p = Teacher.query.filter_by(name = name,college=college)
##        flash("jayy")
##        for k in p:
##            
##            #if k== None:
##                #flash("No teacher with this name exists in database")
##                #return redirect('/teacher_search')
##            #else:
##            for j in k.posts.all():
##                    qmlist.append(j)
##                    if j.grade != None:
##                        flash("below is grade")
##                        flash(j.grade)
##                        sum1 = sum1+float(j.grade)
##                        sum2 = sum2+float(j.rating)
##        alist = [i for i in range(1,1+math.ceil(len(qmlist)/2))]
##        
##        clist = qmlist[(page-1)*2:(page*2)]
##        flash(clist)
##        redirect(url_for('college_search'))
            
    if len(qmlist)>0:        
          
        
        return render_template('college_search.html',title="Search College",user = user2,form=form,form1=form1,cdict=cdict,ddict=ddict,posts = c1list,posts1=aset,posts2=bset,times = a1list,avg = round(sum1/len(qmlist)),avg1 = round(sum2/len(qmlist)),num = len(qmlist),page=page,adict = adict,ifa="ifa",image=((round(sum1/len(qmlist))+round(sum2/len(qmlist)))/2))
    else:
        flash(len(qmlist))
        return render_template('college_search.html',title="Search College",user = user2,form=form,form1=form1,cdict=cdict,ddict=ddict,posts = clist,posts1=aset,posts2=bset,times = alist,pop = True,page=page,adict=adict)

def datetimert(dt):
    time1 = dt
    time2 = datetime.datetime.now() 
    elapsedTime = time2 - time1
    x = divmod(elapsedTime.total_seconds(), 60)
    if (x[0] > 0 and x[0] < 60):
        return str(int(x[0])) + " minutes"
    elif (x[0] >= 60 and x[0] < 1440):
        return str(int(x[0]/60)) +" hours"
    elif (x[0] > 1440 and x[0] < 525600):
        return str(int(x[0]/1440)) + " days"
    else:
        return str(int(x[0]/525600)) +  " years"

def checkcolor(image):
    if image<= 10 and image>7:
        return "green"
    elif image <= 7 and image >4:
        return "magenta"
    elif image <=4 and image >=0:
        return "red"
def checkpanel(image):
    if image<= 10 and image>7:
        return "success"
    elif image <= 7 and image >4:
        return "warning"
    elif image <=4 and image >=0:
        return "danger"
        
    
    
    

'''def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('INvalid try agaibn')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user'''
    
    





