from flask import Flask
from flask import request
#import datetime
from datetime import datetime
from datetime import timedelta
import json
from apscheduler.schedulers.background import BackgroundScheduler
from meet_record import *
scheduler = BackgroundScheduler()


app = Flask(__name__)

#@app.route('/', methods=['GET', 'POST'])
#def home():
#    return '<h1>自动会议录制</h1>'

@app.route('/', methods=['GET'])
def home():
    return '''<h1>自动会议录制</h1>
              <form action="/" method="post">
              <p>开始时间:<input name="starttime" value="年-月-日 小时:分钟"></p>
              <p>会议号码:<input name="meetnumber"></p>
              <p>入会密码:<input name="meetpwd"></p>
			  <p>授权码:<input name="pwd" type=password></p>
              <p><button type="submit">提交</button></p>
              </form>'''

@app.route('/', methods=['POST'])
def cron():
	if (request.form['pwd']=="FHGN#y*IBCEJWkNe"):
		# 需要从request对象读取表单内容：
		#if request.form['username']=='admin' and request.form['password']=='password':
		#    return '<h3>Hello, admin!</h3>'
		#
		meetnumber=request.form['meetnumber']
		meetnumber=meetnumber.replace(" ",'')
		meetpwd=request.form['meetpwd']
		if (request.form['starttime']=="年-月-日 小时:分钟"):
			runtime=datetime.now()+timedelta(seconds=30)
		else:
			runtime=datetime.strptime(request.form['starttime'], "%Y-%m-%d %H:%M")
		table=jsontable(meetnumber,meetpwd,runtime.strftime('%Y-%m-%d %H:%M:%S') )
		scheduler.add_job(job_func, 'date', run_date=runtime, args=[meetnumber,meetpwd])
		try:
			scheduler.start()
		except:
			pass

		return '<h3>成功加入</h3>'+'<h3>json存储序列</h3>'+'<br />'+str(table)+'<br />'+'<h3>cron序列</h3>'+'<br />'+str(scheduler.get_jobs())
	else:
		return '<h3>成功加入</h3>'
		
		
def job_func(meetnumber,meetpwd):
    app=meet_record()
    if (meetpwd != ''):
        app.open_meet(meetnumber,meetpwd)
    else:
        app.open_meet(meetnumber)

def jsontable(meetnumber,meetpwd,runtime):
    with open('crontable.json', 'r') as f:
        crontable = json.load(f)
        print("加载文件完成...")
    plus={'meetnumber':meetnumber,'meetpwd':meetpwd,'runtime':runtime}
    if (plus not in crontable):
        crontable.append(plus)
    with open("crontable.json","w") as f:
        json.dump(crontable,f)
        print("写入文件完成...")

    return crontable

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)