import os
import unittest
print('lala')

from config import basedir
from app import app,db
from app.models import User,Teacher,Post
from datetime import datetime, timedelta

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    '''def test_nickname(self):
        user = User(nickname='joe',email='joe@yahoo.com',username = 'joey',password='joey',college='VIT')
        db.session.add(user)
        db.session.commit()'''
    def test_written_about(self):
        u1 = User(nickname='john', email='john@example.com',username = "jack",password = "jack",college="lol")
        u2 = Teacher(name='susan',subject = "jac",college="lo")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        u = u1.written_about(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.written_about(u2) is None
        assert u1.has_written_about(u2)
        assert u1.teachers.count() == 1
        #print("mwahahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhahahah"+str(u1.teachers.first().id))
        assert u1.teachers.first().name == 'susan'
        assert u2.students.count() == 1
        assert u2.students.first().nickname == 'john'

    def test_posts(self):
        u1 = User(nickname = 'john',email = "kokee",username = "kokee",password = "kokee",college="iit")
        u2 = User(nickname = 'susan',email = "kokeee",username = "kokeee",password = "kokeee",college="iit")
        u3 = Teacher(name = 'johhn',subject = "kokee",college = "iit")
        u4 = Teacher(name = 'johhan',subject = "koakee",college = "iait")
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        utcnow = datetime.utcnow()
        p1 = Post(body="post from userjodhn", author=u1, timestamp=utcnow + timedelta(seconds=1),teacher = u3)
        p2 = Post(body="post from usersusan", author=u2, timestamp=utcnow + timedelta(seconds=2),teacher = u4)
        p3 = Post(body="post2 fromuser jodhn ", author=u1, timestamp=utcnow + timedelta(seconds=3),teacher = u4)
        p4 = Post(body="post2 from usersusan", author=u2, timestamp=utcnow + timedelta(seconds=4),teacher = u3)
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()
        u1.written_about(u4)
        u1.written_about(u3)
        u2.written_about(u4)
        u2.written_about(u3)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        f2 = u2.followed_teachers().all()
        f1 = u1.followed_teachers().all()
        


if __name__ == '__main__':
    unittest.main()
        
