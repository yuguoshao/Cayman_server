from pywinauto import application
import time
import os
from webdav3.client import Client
from webdav3.exceptions import LocalResourceNotFound
import paramiko
from scp import SCPClient
from win32com.shell import shell,shellcon

class meet_record:
   #'所有员工的基类'
   # #empCount = 0
   Recording = False
   timeout=0


   def __init__(self, meet_path = 'C:\\Users\\Administrator\\Desktop\\txhy.bat', obs_path="C:\\Users\\Administrator\\Desktop\\ocam.exe", video_path="D:\\Cayman\\video\\"):
      self.meet_path = meet_path
      self.obs_path = obs_path
      self.video_path = video_path

      self.shell=application.Application(backend="uia").connect(class_name="Shell_TrayWnd")
      #self.shell['Pane']['运行中的应用程序Pane'].child_window(title="腾讯会议 - 1 个运行窗口").click_input()#前台腾讯会议
      #self.shell['Pane']['运行中的应用程序Pane'].child_window(title="OBS Studio - 1 个运行窗口".click_input()#前台OBS
      #self.salary = salary
      #Employee.empCount += 1
   
   def in_meet(self,MeetNumber,MeetPwd=None):
      try:
         #print "Total Employee %d" % Employee.empCount
         #self.app=application.Application(backend="uia").start(self.meet_path)
         try:
            self.app = application.Application(backend="uia").connect(class_name="TXGuiFoundation")
         except:
            os.startfile(self.meet_path)
         time.sleep(8)#启动腾讯会议等待5s
         self.app = application.Application(backend="uia").connect(class_name="TXGuiFoundation")
         #连接腾讯会议窗口
         self.app.Dialog.加入会议.click_input()#点击加入会议
         time.sleep(3)

         #self.app["腾讯会议(JoinWnd)"].child_window(title="MeetingCodeFrame", control_type="Pane").click_input()
         #time.sleep(3)
         ##################
         #try:
         #   self.app["腾讯会议(JoinWnd)"].Join_meeting_clear_meeting_number.click_input()
         #   time.sleep(1)
         #   self.app["腾讯会议(JoinWnd)"].child_window(title="MeetingCodeFrame", control_type="Pane").click_input()
         #  time.sleep(3)
         #except:
         #   pass
            
         self.app["腾讯会议(JoinWnd)"].meetingCode.会议号Edit.type_keys(MeetNumber)
         time.sleep(3)
         #输入会议号码
         self.app["腾讯会议(JoinWnd)"].Join_meeting_Join_meetingButton.click_input()#点击加入会议

         if (MeetPwd != None):#若密码不为空，判断并加入会议
            time.sleep(3)

            try:
               self.app["腾讯会议(JoinWnd)"].child_window(title="ClientArea", control_type="Pane")
               self.app["腾讯会议(JoinWnd)"].ClientArea.入会密码Pane2.click_input()
               time.sleep(3)#3s等待窗口
               #app["腾讯会议(JoinWnd)"].ClientArea.print_control_identifiers()
               self.app["腾讯会议(JoinWnd)"].ClientArea.入会密码Pane2.入会密码Edit.type_keys(MeetPwd)
               self.app["腾讯会议(JoinWnd)"].ClientArea.加入Button.click_input()
            except:
               pass
            
         time.sleep(15)

      except:
         pass
      #判断是否进入会议
      try:
         self.app.window(title="腾讯会议(InMeetingWnd)", control_type="Window").wrapper_object()
         #self.app["腾讯会议(InMeetingWnd)"].ClientArea.wrapper_object()
         #self.app["腾讯会议(InMeetingWnd)"].child_window(title="离开会议", control_type="Button").wrapper_object()
         time.sleep(2)
         self.obs_start()
         #self.app["腾讯会议(InMeetingWnd)"].restore()
         #self.shell['Pane']['运行中的应用程序Pane'].child_window(title="腾讯会议 - 1 个运行窗口").click_input()#前台腾讯会议
      except:
         self.timeout=self.timeout+1
         self.out_meet()
         try:
            self.out_meet()
         except:
            pass
         if (self.timeout<5):
            time.sleep(10)
            print("重试进入会议")
            self.in_meet(MeetNumber,MeetPwd)

   def out_meet(self):#退出腾讯会议
      try:
         self.app["腾讯会议(InMeetingWnd)"].child_window(title="结束会议", control_type="Button").click_input()
         self.app["腾讯会议(InMeetingWnd)"].child_window(title="离开会议", control_type="Button").click_input()
      except:
         pass
      try:
         #self.app["腾讯会议(InMeetingWnd)"].restore()
         #self.shell['Pane']['运行中的应用程序Pane'].child_window(title="腾讯会议 - 1 个运行窗口").click_input()#前台腾讯会议
         self.app["腾讯会议(InMeetingWnd)"].child_window(title="离开会议", control_type="Button").click_input()
         self.app["腾讯会议(InMeetingWnd)"].ClientArea.child_window(title="离开会议", control_type="Button").click_input()
         #会议未自动结束离开
      except:
         pass
        
      time.sleep(5)
        #self.app.Dialog.restore()
        #self.shell['Pane']['运行中的应用程序Pane'].child_window(title="腾讯会议 - 1 个运行窗口").click_input()#前台腾讯会议
      self.app.Dialog.sys_close_button2.click_input()
        #关闭腾讯会议

   def check_meet(self):#会议进行状态检查
      while True:
         time.sleep(30)
         try:
            self.app["腾讯会议(InMeetingWnd)"].ClientArea.child_window(title="主持人离开会议，您已成为主持人。", control_type="Text").wrapper_object()
            self.app["腾讯会议(InMeetingWnd)"].ClientArea.知道了.click_input()
            self.end_meet()
            break
         except:
            pass
         try:
            self.app.window(title="腾讯会议(InMeetingWnd)", control_type="Window").wrapper_object()
            #self.app["腾讯会议(InMeetingWnd)"].ClientArea.wrapper_object()
            #self.app["腾讯会议(InMeetingWnd)"].child_window(title="离开会议", control_type="Button").wrapper_object()
         except:
            self.end_meet()
            break

   def obs_start(self):
      import os
      try:
         #self.obs = application.Application(backend="uia").connect(class_name="Qt5QWindowIcon")#连接obs
         self.obs = application.Application(backend="uia").connect(class_name="Hi! oCam")
      except:
         os.startfile(self.obs_path)
         time.sleep(5)
      #self.obs = application.Application(backend="uia").connect(class_name="Qt5QWindowIcon")#连接obs
      self.obs = application.Application(backend="uia").connect(class_name="Hi! oCam")#连接ocam
      ######ocam.Dialog.Toolbar.录制.#ocam.Dialog.Toolbar#ocam.Dialog.Toolbar.停止.click_input()
      #self.obs.Dialog.child_window(title="Start Recording", control_type="CheckBox").click_input()#开始录制
      time.sleep(1)
      self.obs.Dialog.Toolbar.录制.click_input()#开始录制ocam
      time.sleep(5)
        #self.obs.Dialog.minimize()  #不可最小化，最小化之后无法找到窗口  只能利用restore前台
        #self.app.Dialog.restore()#恢复腾讯会议前台状态

   def obs_end(self):
      #self.shell['Pane']['运行中的应用程序Pane'].child_window(title="OBS Studio - 1 个运行窗口").click_input()#前台OBS
      time.sleep(5)
      #self.obs.Dialog.restore()
      #self.obs.Dialog.child_window(title="Stop Recording", control_type="CheckBox").click_input()#结束录制
      self.obs.Dialog.Toolbar.停止.click_input()#结束录制
      print("结束录制")
      time.sleep(15)
      #self.obs.Dialog.child_window(title="Exit", control_type="Button").click_input()#关闭obs
        
      #try:
      #   self.obs.Dialog.child_window(title="Exit OBS?", control_type="Window").child_window(title="Yes Enter", control_type="Button").click_input()#重复点击
      #except:
      #   pass
        
   def open_meet(self,MeetNumber,MeetPwd=None):
      if (self.Recording == False):
         self.in_meet(MeetNumber,MeetPwd)
         self.check_meet()
         self.Recording = True
         return "开始录制任务"

      else:
         return "正在录制，无法执行双重任务"

   def end_meet(self):
      self.obs_end()
      self.out_meet()
      self.Recording = False
      self.Move_video()

   def Move_video(self):
      file_list=os.listdir(self.video_path)
      for f in file_list:
         path=self.video_path+f
         self.upload_ssh(path,f)

   def upload(self,path,f):

      options = {
         'webdav_hostname': "http://docker.peking.tjcpt.com:9999/dav",
         'webdav_login': "admin@cloudreve.org",
         'webdav_password': "h51qgUWXCuhTYOmCVJTW2jNlagWF3ixQ",
         'disable_check': True, #有的网盘不支持check功能
         }
            
      client = Client(options)
        # 我选择用时间戳为备份文件命名
        #file_name = str(math.floor(datetime.now().timestamp())) + '.bak'
      try:
         # 写死的路径，第一个参数是网盘地址
         client.upload("/course/"+f,path)
         # 打印结果，之后会重定向到log
         os.remove(path)
         print('upload at ' + f)
      except LocalResourceNotFound as exception:
         print('An error happen: LocalResourceNotFound ---'  + f)
            
   def upload_ssh(self,path,f):
      host = "docker.peking.tjcpt.com"  #服务器ip地址
      port = 22  # 端口号
      username = "root"  # ssh 用户名
      password = "HUSTsvo123456"  # 密码
    
      ssh_client = paramiko.SSHClient()
      ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
      ssh_client.connect(host, port, username, password)
      scpclient = SCPClient(ssh_client.get_transport())
      local_path = path
      remote_path = "/home/LNMP/wwwroot/default/cloud/uploads/1/course/"
      try:
         scpclient.put(local_path, remote_path)
         #os.remove(path)
         self.deltorecyclebin(path)
      except FileNotFoundError as e:
         print(e)
         print("系统找不到指定文件" + local_path)
      else:
         print("文件上传成功")
      ssh_client.exec_command("chmod 777 /home/LNMP/wwwroot/default/cloud/uploads/1/course/*")
      ssh_client.close()


   debug=False
   def deltorecyclebin(self,filename):
      print('deltorecyclebin', filename)
      # os.remove(filename) #直接删除文件，不经过回收站
      if True:
         res= shell.SHFileOperation((0,shellcon.FO_DELETE,filename,None, shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,None,None))  #删除文件到回收站
         if not res[1]:
            os.system('del '+filename)
