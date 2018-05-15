import os
from app import create_app, db
import unittest

# 单元测试暂时放在这里2018.5.15

class FlaskTestCase(unittest.TestCase):  # 继承unittest.TestCase
    def setUp(self):
            self.app = create_app('testing')
            self.app_context = self.app.app_context()
            self.app_context.push()
            db.create_all()
            self.client = self.app.test_client()

    def tearDown(self):
            db.session.remove()
            db.drop_all()
            self.app_context.pop()

    def test_login(self):
        respons = self.app.get('/index/')
        print(respons)
        self.assertTrue('hello' in respons.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
