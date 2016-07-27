from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username',validators = [DataRequired()])
    password = PasswordField('password',validators = [DataRequired()])
    remember_me = BooleanField('remember_me',default = False)

class SignUpForm(Form):
    username = StringField('username',validators = [DataRequired()])
    password = PasswordField('password',validators = [DataRequired()])
    nickname = StringField('nickname',validators = [DataRequired()])
    emailid = StringField('emailid',validators = [DataRequired()])
    college = StringField('college',validators = [DataRequired()])

class PostForm(Form):
    post = StringField('post',validators=[DataRequired()])
    anon = BooleanField('anon',default = False)
    teacher = StringField('teacher',validators=[DataRequired()])
    subject = StringField('subject',validators=[DataRequired()])
    college = StringField('college')
    grade = StringField('grade')
    rating = StringField('rating')

class TeacherForm(Form):
    teacher = StringField('teacher')

class CollegeForm(Form):
    college = StringField('college',validators = [DataRequired()])

class CTeacherForm(Form):
    cteacher  = StringField('cteacher',validators = [DataRequired()])
    
    #rating = IntegerField('rating',validators=[DataRequired()])
    #homework = BooleanField('anon',default = False)
    
    
