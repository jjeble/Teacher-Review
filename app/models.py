from app import db

teacher_student_table = db.Table('teacher_student_table',db.Column('user_id', db.Integer,db.ForeignKey('user.id'), nullable=False),
                             db.Column('teacher_id',db.Integer,db.ForeignKey('teacher.id'),nullable=False),
                             db.PrimaryKeyConstraint('user_id', 'teacher_id'))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True) 
    nickname = db.Column(db.String(64), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    username = db.Column(db.String(80), index = True, unique = True)
    password = db.Column(db.String(80), index = True, unique = True)
    college =  db.Column(db.String(120),index = True)
    posts = db.relationship('Post',backref = 'author' , lazy='dynamic')
    teachers = db.relationship('Teacher',secondary = 'teacher_student_table',backref  ='user',lazy='dynamic')
    
    def written_about(self,teacher):
        if not self.has_written_about(teacher):
            self.teachers.append(teacher)
            return self


    def has_written_about(self,teacher):
        return self.teachers.filter(teacher_student_table.c.teacher_id==self.id).count()>0

    def followed_teachers(self):
        return Post.query.join(teacher_student_table,(teacher_student_table.c.user_id==Post.user_id)).filter(teacher_student_table.c.teacher_id==self.id).order_by(Post.timestamp.desc())

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    #teacher = db.Column(db.String(140))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    teacher_id = db.Column(db.Integer,db.ForeignKey('teacher.id'))
    grade = db.Column(db.String(5),index = True)
    rating = db.Column(db.String(5),index = True)
    anon = db.Column(db.String(4),index = True)
                               

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64), index = True)
    subject = db.Column(db.String(120), index = True)
    college = db.Column(db.String(120),index = True)
    posts = db.relationship('Post',backref = 'teacher' , lazy='dynamic')
    students = db.relationship('User',secondary = 'teacher_student_table',backref  ='teacher',lazy='dynamic')


    def beenwritten_about(self,user):
        if not self.hasbeen_written_about(user):
            self.students.append(user)
            return self


    def hasbeen_written_about(self,user):
        return self.students.filter(teacher_student_table.c.user_id==self.id).count()>0


   

