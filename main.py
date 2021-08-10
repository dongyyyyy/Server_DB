from flask import Flask,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
import pymysql
import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget
import requests
app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록

conn = pymysql.connect(host='localhost',port=3306,user='pass',password='pass',db='face_recognition',charset='utf8')
curs = conn.cursor()


@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@app.route('/select_checks', methods=['POST'])
def select_checks():
    # params = json.loads(request.get_data(), encoding='utf-8')
    params = json.loads(request.get_data(),encoding='utf-8')
    print(params)
    name = params['name']
    query = params['select']
    # query = request.form.get('select')
    # name = request.form.get('name')
    print(f'name = {name} // query = {query}')
    curs.execute(query)
    # 데이타 Fetch
    rows = curs.fetchall()
    is_check = False
    # 아랫 부분 restful로 수정
    for row in rows:
        current_time = datetime.today().strftime('%Y-%m-%d')
        check_time = row[0].strftime('%Y-%m-%d')
        # print(f'current_time = {current_time} // check_time = {check_time}')
        if current_time == check_time:
            is_check = True
    if is_check:
        return_str = '이미 출석한 사람'
    else:
        sql = f"insert into checks(name) values(%s)"
        curs.execute(sql, (f'{name}'))
        conn.commit()
        return_str = '출근'
    return return_str

@app.route('/new_picture', methods=['POST'])
def new_picture():
    # params = json.loads(request.get_data(), encoding='utf-8')
    params = json.loads(request.get_data(),encoding='utf-8')
    name = params['name']
    query = params['select']

    curs.execute(query)
    # 데이타 Fetch
    rows = curs.fetchall()
    print(rows)
    str = '%d'%(len(rows))
    # print(len(rows))
    return str

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = MyApp()
    # sys.exit(app.exec_())
    app.run(debug=True, host='0.0.0.0', port=80)