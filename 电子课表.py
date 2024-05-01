import subprocess
import sys

def install_module(module):
    try:
        __import__(module)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module,'-i','https://pypi.tuna.tsinghua.edu.cn/simple'])

# 使用示例
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.messagebox as tkm
    import time as TIME
    import traceback,os,json,threading,pyautogui
    from datetime import datetime, time
    from ctypes import *  # 获取屏幕上某个坐标的颜色
    from ctypes import windll

    from PIL import Image, ImageTk
    import sched
except ImportError:
    install_module("tkinter")
    install_module("time")
    install_module("traceback")
    install_module("os")
    install_module("json")
    install_module("threading")
    install_module("datetime")
    install_module("ctypes")


def get_color(x, y):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)  # 获取颜色值
    pixel = gdi32.GetPixel(hdc, x, y)  # 提取RGB值
    r = pixel & 0x0000ff
    g = (pixel & 0x00ff00) >> 8
    b = pixel >> 16
    return [r, g, b]

def RGB_to_Hex(tmp):
    strs = '#'
    for i in tmp:
        num = int(i)#将str转int
        #将R、G、B分别转化为16进制拼接转换并大写
        strs += str(hex(num))[-2:].replace('x','0').upper()
        
    return strs

def is_color_dark(hex_color):
    # 将十六进制颜色转换为RGB值
    red = int(hex_color[1:3], 16)
    green = int(hex_color[3:5], 16)
    blue = int(hex_color[5:7], 16)
    
    # 计算颜色的亮度
    brightness = (red * 299 + green * 587 + blue * 114) / 1000
    
    # 判断颜色的深浅
    if brightness < 128:
        print(brightness)
        return True
    else:
        print(brightness)
        return False


#TIME.sleep(2)

'''class TimeWindow_Date(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.title("电子课表")
        self.screenWidth = self.winfo_screenwidth()  # 获取显示区域的宽度
        self.screenHeight = self.winfo_screenheight()  # 获取是否�示�域的高宽数据
        print(self.screenWidth,self.screenHeight)
        width = 120  # 设定窗口宽度
        height = self.screenHeight/26  # 设定窗口高度
        left,top = self.screenWidth - 130,5
        gca=get_color(left, top)
        gcb=get_color(left+170, top+60)
        gcc=RGB_to_Hex((int((gca[0]+gcb[0])/2),int((gca[1]+gcb[1])/2),int((gca[2]+gcb[2])/2)))
        if is_color_dark(gcc):
            self.font_color='white'
        else:
            self.font_color='black'

        self.time_label1 = tk.Label(self, font=("Arial", 14),fg=self.font_color,bg=gcc)
        self.time_label1.pack()

        self.geometry("%dx%d+%d+%d" % (width, height, left, top))
        self.configure(background=gcc)
        self.attributes('-alpha', 0.7)
        self.resizable(0, 0)
        self.update_time()
        self.overrideredirect(True)

    def update_time(self):
        current_time1 = TIME.strftime("%Y-%m-%d", TIME.localtime())
        self.time_label1.config(text=current_time1)
        self.after(1000, self.update_time)  # 每隔1秒更新时间'''


class TimetableWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.screenWidth = self.winfo_screenwidth()  # 获取显示区域的宽度
        self.screenHeight = self.winfo_screenheight()  # 获取是否�示�域的高宽数据
        print(self.screenWidth,self.screenHeight)
        
        width = 240  # 设定窗口宽度  120
        height = self.screenHeight/26  # 设定窗口高度
        left,top = self.screenWidth - 150,int(self.screenHeight/172.8)+30
        gca=get_color(left, top)
        print(gca)
        gcc=RGB_to_Hex((int((gca[0])),int((gca[1])),int((gca[2]))))
        if is_color_dark(gcc):
            font_color='white'
        else:
            font_color='black'
        self.theme_d={'lightcolour':('black','white'),'deepcolour':('white','black'),'multicolour':(font_color,gcc)}
        fn=os.getcwd()
        with open(fn+'\\Schedule_Info\\profile.json','r') as readweek:
            read_week = json.load(readweek)
            theme=read_week['theme']
        
        self.gcc=self.theme_d[theme][1]
        self.font_color=self.theme_d[theme][0]



        
        self.time_label2 = tk.Label(self, font=("Arial", 14),fg='#FF0000',bg=self.gcc)
        self.time_label2.pack()

        self.geometry("%dx%d+%d+%d" % (width, height, left, top))
        self.configure(background=self.gcc)
        self.attributes('-alpha', 0.7)
        self.resizable(0, 0)
        self.update_time()
        self.overrideredirect(True)
        self.wm_attributes('-topmost',1)
        #以上部分是实时时间窗口创建



        #self.event=threading.Event()
        self.root_set= tk.Toplevel()             #程序编辑窗口
        self.root= tk.Toplevel()              #科目信息显示主窗口
        self.width = 240  # 设定 信息显示主窗口 窗口宽度  120
        self.height = self.screenHeight/13*11  # 设定 信息显示主窗口 窗口高度
        self.left = self.screenWidth - 150
        self.top = int(self.screenHeight/12)
        
        self.root.geometry("%dx%d+%d+%d" % (self.width,self.height, self.left, self.top))
        self.root.configure(background=self.gcc)
        self.root.attributes('-alpha', 0.6)
        self.root.resizable(0, 0)
        self.root.overrideredirect(True)
        self.left=self.screenWidth - 30
        self.width=50#25
        self.root_set.geometry("%dx%d+%d+%d" % (self.width,self.height, self.left, self.top))
        if self.gcc=='black':
            self.gcc1='grey'
            self.root_set.configure(background='grey')
        else:
            self.gcc1=self.gcc
            self.root_set.configure(background=self.gcc)
        self.root_set.attributes('-alpha', 0.7)
        self.root_set.resizable(0, 0)
        self.root_set.overrideredirect(True)

        self.localtime=TIME.localtime(TIME.time())
        self.tm_wday=int(self.localtime[6])+1
        self.tm_wday_dict={1:'星期一',2:'星期二',3:'星期三',4:'星期四',5:'星期五',6:'星期六',7:'星期七'}
        if int(self.localtime[-2])<125:
            self.sl=1
        elif int(self.localtime[-2])>125:
            self.sl=2
        self.tm_yday_dict={1:'春夏作息',2:'秋冬作息'}



        self.a,self.b,self.c,self.d,self.e,self.f,self.g,self.h,self.i,self.j,self.k,self.l,self.m,self.n=0,0,0,0,0,0,0,0,0,0,0,0,0,0

        


    def is_time_in_range(self,start_time, end_time, target_time):
        # 将时间字符串转换为datetime对象
        start = datetime.strptime(start_time, "%H:%M:%S").time()
        end = datetime.strptime(end_time, "%H:%M:%S").time()
        target = datetime.strptime(target_time, "%H:%M:%S").time()

        # 判断目标时间是否在时间段内
        if start <= target <= end:
            return True
        else:
            return False
        
    def change_time_shape(self,time_tulpe):
        hour_int,minute_int=int(time_tulpe[0]),int(time_tulpe[1])
        if hour_int<10:
            hour_str='0'+str(hour_int)
        else:
            hour_str=str(hour_int)
        if minute_int<10:
            minute_str='0'+str(minute_int)
        else:
            minute_str=str(minute_int)
        new_name_shape=hour_str+':'+minute_str+':'+'00'
        return new_name_shape

    def time_convert(self,time_str):
        # 分割时间字符串，得到时、分、秒三个部分
        hour_str, minute_str, second_str = time_str.split(':')
        # 将时、分、秒三个部分转换为整数类型
        hour = int(hour_str)
        minute = int(minute_str)
        second = int(second_str)
        # 返回一个由时、分组成的元组
        return (hour, minute)


    def KBBJ(self): 
        '''TimetableWindow函数,创建课表编辑页面''' 
        def Var_Week_Queding():
            '''在subjectlb中显示选中星期的课时信息'''
            fn_json=fn+'\\Schedule_Info\\%s\\%s.json'%(var_zxsj.get(),var_week.get())
            try:
                with open(fn_json,'r') as readweek:
                    read_week = json.load(readweek)
                subjectlb.delete(0,tk.END)
                subjectlb_list={}
                for ind,inf in read_week.items():                                   #获取并修改该天课时信息格式
                    subjectlb_list[int(ind)-1]=ind+'    '+inf['科目']+':'+inf['上课时间']+'-'+inf['下课时间']
                for indli,infli in subjectlb_list.items():                          #向listbox中插入信息
                    subjectlb.insert(indli,infli)


            except NameError:
                tkm.showinfo('提示','选择作息时间后再进行操作')
            except json.decoder.JSONDecodeError:
                tkm.showwarning('提示','暂无课表信息')
                with open(fn_json,'w') as writeweek:
                    write_week = {}
                    write_week[1]={'科目':'语文','上课时间':'7:00:00','下课时间':'7:40:00'}
                    json.dump(write_week,writeweek)
            except Exception as e:
                tkm.showerror('ERROR',traceback.format_exc())

        def Var_Subject_Queding():
            '''课表信息创建或更新的功能函数'''
            week_inf=var_week.get()
            subject_inf=Var_Subject.get()
            subject_index_inf=Var_Subject_Index.get()
            if subject_inf=='科目' or subject_index_inf=='课时':
                tkm.showinfo('提示','漏填信息')
                return
            st1,st2=zuoxishijian_aw[int(subject_index_inf)-1][0][0],zuoxishijian_aw[int(subject_index_inf)-1][0][1]
            ft1,ft2=zuoxishijian_aw[int(subject_index_inf)-1][1][0],zuoxishijian_aw[int(subject_index_inf)-1][1][1]
            
            '''if int(st1)>int(ft1) or (int(st1)>int(ft1) and int(st2)>int(st1)) or (int(st1)==int(ft1) and int(st2)==int(st1)):
                print(st1,st2,ft1,ft2)
                tkm.showinfo('提示','时间填写有误')
                return'''

            starttime_inf=self.change_time_shape((st1,st2))
            finishtime_inf=self.change_time_shape((ft1,ft2))
            zxsj_inf=var_zxsj.get()
            
            #tkm.showinfo('提示','%s %s %s %s %s %s'%(week_inf,subject_inf,subject_index_inf,zxsj_inf,starttime_inf,finishtime_inf))
            fn_json=fn+'\\Schedule_Info\\秋冬作息\\%s.json'%week_inf        #获取当天当前的信息
            with open(fn_json,'r') as readweek:
                read_week = json.load(readweek)
        
            
            if subject_index_inf in read_week.keys():           #更新信息
                result = tkm.askokcancel('提示', '已有第%s节课的信息,是否选择修改?'%subject_index_inf)
                if result:
                    with open(fn_json,'w') as writeweek:                        #写入课时信息
                        write_week = read_week
                        write_week[subject_index_inf]={'科目':subject_inf,'上课时间':starttime_inf,'下课时间':finishtime_inf}
                        json.dump(write_week,writeweek)
                    subjectlb.delete(0,tk.END)          #清空listbox信息以重新插入
                    subjectlb_list={}
                    for ind,inf in write_week.items():                                   #获取并修改该天课时信息格式
                        subjectlb_list[int(ind)-1]=str(ind)+'    '+inf['科目']+':'+inf['上课时间']+'-'+inf['下课时间']
                    for indli,infli in subjectlb_list.items():                          #向listbox中插入信息
                        subjectlb.insert(indli,infli)
                    Var_Subject_Index.set(int(subject_index_inf)+1)
            else:               #新建课时信息
                subject_index_inf1=subject_index_inf
                if int(subject_index_inf) == 14:
                    subject_index_inf='13'
                    subject_index_inf1='14'
                Var_Subject_Starttime1.set(zuoxishijian_aw[int(subject_index_inf)][0][0])       #上下课时间Combobox控件 初始设置
                Var_Subject_Starttime2.set(zuoxishijian_aw[int(subject_index_inf)][0][1])
                Var_Subject_Finishtime1.set(zuoxishijian_aw[int(subject_index_inf)][1][0])
                Var_Subject_Finishtime2.set(zuoxishijian_aw[int(subject_index_inf)][1][1])
                with open(fn_json,'w') as writeweek:                        #写入课时信息
                    write_week = read_week
                    write_week[int(subject_index_inf1)]={'科目':subject_inf,'上课时间':starttime_inf,'下课时间':finishtime_inf}
                    json.dump(write_week,writeweek)
                subjectlb.delete(0,tk.END)          #清空listbox信息以重新插入
                subjectlb_list={}
                for ind,inf in write_week.items():                                   #获取并修改该天课时信息格式
                    subjectlb_list[int(ind)-1]=str(ind)+'    '+inf['科目']+':'+inf['上课时间']+'-'+inf['下课时间']
                for indli,infli in subjectlb_list.items():                          #向listbox中插入信息
                    subjectlb.insert(indli,infli)
                Var_Subject_Index.set(int(subject_index_inf1)+1)
                #Var_Subject_Index_DEL.set()
  
        def Var_delete_Queding():
            week_inf=var_week.get()
            VSID=Var_Subject_Index_DEL.get()
            fn_json=fn+'\\Schedule_Info\\秋冬作息\\%s.json'%week_inf
            with open(fn_json,'r') as readweek:
                read_week = json.load(readweek)
            print(read_week.keys())
            if VSID == '0':
                result = tkm.askokcancel('确定 | 取消', ' ')
                if result:
                    with open(fn_json,'w') as writeweek:
                        write_week = {}
                        json.dump(write_week,writeweek)
                    subjectlb.delete(0,tk.END)
            else:
                if VSID not in read_week.keys():
                    tkm.showinfo('提示','未发现第%s节课的信息'%VSID)
                
                else:
                    if int(VSID)==14:
                        VSID='13'
                    Var_Subject_Starttime1.set(zuoxishijian_aw[int(VSID)-1][0][0])
                    Var_Subject_Starttime2.set(zuoxishijian_aw[int(VSID)-1][0][1])
                    Var_Subject_Finishtime1.set(zuoxishijian_aw[int(VSID)-1][1][0])
                    Var_Subject_Finishtime2.set(zuoxishijian_aw[int(VSID)-1][1][1])
                    with open(fn_json,'w') as writeweek:
                        write_week = read_week
                        write_week.pop(VSID)
                        json.dump(write_week,writeweek)
                    subjectlb.delete(0,tk.END)
                    subjectlb_list={}
                for ind,inf in write_week.items():                                   #获取并修改该天课时信息格式
                    subjectlb_list[int(ind)-1]=ind+'    '+inf['科目']+':'+inf['上课时间']+'-'+inf['下课时间']
                for indli,infli in subjectlb_list.items():                          #向listbox中插入信息
                    subjectlb.insert(indli,infli)


        fn=os.getcwd()
        leaf=tk.Tk()                #课表编辑子页面创建
        leaf.title("课表编辑")
        leaf.iconbitmap(fn+'\\ico\\p1.ico')
        leaf.geometry("900x550")#%(int(self.screenWidth*0.521),int(self.screenHeight*0.579))
        leaf.configure(background='white')
        leaf.attributes('-alpha', 0.96)
        leaf.resizable(0, 0)





        subjectlb=tk.Listbox(leaf,height=20,width=52)             #课时信息显示窗口      
        subjectlb.place(x=50,y=50)

        var_week=tk.StringVar(leaf)         #星期选择下拉控件
        Var_Week=tk.OptionMenu(leaf,var_week,'星期一','星期二','星期三','星期四','星期五','星期六','星期七')
        wsf=['星期一','星期二','星期三','星期四','星期五','星期六','星期七']
        var_week.set(wsf[self.localtime[6]])        #根据具体时间设置 星期选择下拉控件 初始设置
        Var_Week.place(x=550,y=160)
        var_zxsj=tk.StringVar(leaf)                 #
        Var_Zxsj=tk.OptionMenu(leaf,var_zxsj,'春夏作息','秋冬作息')
        var_zxsj.set('秋冬作息')
        #Var_Zxsj.place(x=550,y=30)
        Var_Week_button = tk.Button(leaf , text="显示" , command=Var_Week_Queding ,width=8, font=("宋体", 14 ))
        Var_Week_button.place(x=750,y=160)#670 160


        with open(fn+'\\Schedule_Info\\%s\\%s.json'%(var_zxsj.get(),var_week.get()),'r') as readweek:        #获得当天的课表信息作为初始化信息
            read_week_initialization = json.load(readweek)
        Var_Week_Queding()                                          #打开课表编辑后自动显示当天课表信息

        var_subject=tk.StringVar()
        Var_Subject=ttk.Combobox(leaf,textvariable=var_subject,value=('语文','数学','英语','政治','历史','物理','化学','地理','生物','生涯','体育','信息','单美双音','体育活动','休息','语文周考','数学周考','英语周考','物理周考','化学周考','生物周考','公共自习'),width=10,height=5)
        Var_Subject.set('科目')
        Var_Subject.place(x=550,y=240)
        Var_Subject_Index_List=(1,2,3,4,5,6,7,8,9,10,11,12,13,14)
        global var_subject_index
        var_subject_index=tk.StringVar()
        Var_Subject_Index=ttk.Combobox(leaf,textvariable=var_subject_index,value=Var_Subject_Index_List,width=10,height=5)
        Var_Subject_Index.set('课时')
        Var_Subject_Index.place(x=550,y=270)

        a=(6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22)      #上下课时间Combobox控件 小时数范围
        b=[]                                                    #上下课时间Combobox控件 分钟数范围
        for i in range(0,60):
            b.append(i)
        b=tuple(b)

        zuoxishijian_ss=[]               #
        zuoxishijian_aw=[((7,15),(7,35)),((7,45),(8,25)),((8,35),(9,15)),((9,40),(10,20)),((10,30),(11,10)),((11,20),(12,00)),((14,35),(15,15)),((15,25),(16,5)),((16,20),(17,0)),((17,10),(17,50)),((18,45),(19,25)),((19,35),(20,15)),((20,25),(21,20)),((21,35),(22,35))]

        trg=1
        for i in self.RWA:
            if i != trg:
                Var_Subject_Starttime1_initialization=zuoxishijian_aw[trg][0][0]       #上课时间Combobox控件 初始设置
                Var_Subject_Starttime2_initialization=zuoxishijian_aw[trg][0][1]        #上课时间Combobox控件 初始设置
                Var_Subject_Finishtime1_initialization=zuoxishijian_aw[trg][1][0]        #下课时间Combobox控件 初始设置
                Var_Subject_Finishtime2_initialization=zuoxishijian_aw[trg][1][1]        #下课时间Combobox控件 初始设置
                Var_Subject_Index.set(trg)
                break
            elif i == 14:
                Var_Subject_Starttime1_initialization=zuoxishijian_aw[0][0][0]       #上课时间Combobox控件 初始设置
                Var_Subject_Starttime2_initialization=zuoxishijian_aw[0][0][1]        #上课时间Combobox控件 初始设置
                Var_Subject_Finishtime1_initialization=zuoxishijian_aw[0][1][0]        #下课时间Combobox控件 初始设置
                Var_Subject_Finishtime2_initialization=zuoxishijian_aw[0][1][1]        #下课时间Combobox控件 初始设置
            trg+=1
        
        
        
        
        
        
        var_subject_starttime1=tk.StringVar()
        Var_Subject_Starttime1=ttk.Combobox(leaf,textvariable=var_subject_starttime1,value=a,width=10,height=5)
        Var_Subject_Starttime1.set(Var_Subject_Starttime1_initialization)
        #Var_Subject_Starttime1.place(x=450,y=170)
        var_subject_starttime2=tk.StringVar()
        Var_Subject_Starttime2=ttk.Combobox(leaf,textvariable=var_subject_starttime2,value=b,width=10,height=5)
        Var_Subject_Starttime2.set(Var_Subject_Starttime2_initialization)
        #Var_Subject_Starttime2.place(x=550,y=170)


        var_subject_finishtime1=tk.StringVar()
        Var_Subject_Finishtime1=ttk.Combobox(leaf,textvariable=var_subject_finishtime1,value=a,width=10,height=5)
        Var_Subject_Finishtime1.set(Var_Subject_Finishtime1_initialization)
        #Var_Subject_Finishtime1.place(x=450,y=220)
        var_subject_finishtime2=tk.StringVar()
        Var_Subject_Finishtime2=ttk.Combobox(leaf,textvariable=var_subject_finishtime2,value=b,width=10,height=5)
        Var_Subject_Finishtime2.set(Var_Subject_Finishtime2_initialization)
        #Var_Subject_Finishtime2.place(x=550,y=220)


        Var_Subject_Queding_button = tk.Button(leaf , text="新建/更新" , command=Var_Subject_Queding ,width=8, font=("宋体", 14 ))
        Var_Subject_Queding_button.place(x=750,y=250)

        var_subject_index_del=tk.StringVar()
        Var_Subject_Index_List_Del=Var_Subject_Index_List+(0,)
        Var_Subject_Index_DEL=ttk.Combobox(leaf,textvariable=var_subject_index_del,value=Var_Subject_Index_List_Del,width=10,height=5)
        Var_Subject_Index_DEL.set('课时')
        #Var_Subject_Index_DEL.place(x=500,y=350)

        Var_Subject_Queding_button2 = tk.Button(leaf , text="删除" , command=Var_delete_Queding ,width=8, font=("宋体", 13 ))
        #Var_Subject_Queding_button2.place(x=650,y=350)



        author_label = tk.Label(leaf, text="软件作者: 高2026届 赵晨羽", bg='white', font=("宋体", 14 ))
        author_label.place(x=100, y=500)

        

        

        #EXIT=tk.Button(leaf,text='退出软件',command=EXit,width=8,font=("Arial",13))
        #EXIT.place(x=680,y=440)#440



        Using_Tutorials=tk.Button(leaf,text='使用教程',command='',width=8,font=("Arial",14))
        Using_Tutorials.place(x=750,y=490)

        leaf.mainloop()

    def kmxs(self):
        '''TimetableWindow函数,在程序主窗口中创建科目信息Lable控件''' 
        if int(self.localtime[4])+50 <60:
            localtime_hour=self.localtime[3]
            localtime_mintue=str(int(self.localtime[4])+50)
        elif int(self.localtime[4])+50 >=60:
            localtime_hour=str(int(self.localtime[3])+1)
            localtime_mintue=str(50+int(self.localtime[4])-60)

        self.localtime_cs=self.change_time_shape((self.localtime[3],self.localtime[4]))
        self.localtime_cs_next=self.change_time_shape((localtime_hour,localtime_mintue))
        fn_json=os.getcwd()+'\\Schedule_Info\\%s\\%s.json'%(self.tm_yday_dict[self.sl],self.tm_wday_dict[self.tm_wday])
        try:
            with open(fn_json,'r') as readweek:
                read_week = json.load(readweek)
                shangwujieshu1=read_week['1']['上课时间']
                shangwujieshu2=read_week['6']['下课时间']
                xiawujieshu1=read_week['7']['上课时间']
                xiawujieshu2=read_week['10']['下课时间']
                wanshangjieshu1=read_week['11']['上课时间']
                wanshangjieshu2=read_week['14']['下课时间']
        except json.decoder.JSONDecodeError:
            tkm.showwarning('提示','暂无课表信息')
            
            with open(fn_json,'w') as writeweek:
                write_week = {}
                for g in range(1,15):
                    write_week[g]={'科目':'语文','上课时间':'7:00:00','下课时间':'7:40:00'}
                json.dump(write_week,writeweek)
            with open(fn_json,'r') as readweek:
                read_week = json.load(readweek)
                
                read_week['1']['上课时间']
                shangwujieshu2=read_week['6']['下课时间']
                xiawujieshu1=read_week['7']['上课时间']
                xiawujieshu2=read_week['10']['下课时间']
                wanshangjieshu1=read_week['11']['上课时间']
                wanshangjieshu2=read_week['14']['下课时间']

        
        #对课时信息字典进行排序  
        rwa=sorted(read_week.keys())                  #获取字典的键
        RWA=[]                                         #将rwa中的str元素转化为int元素                         
        for i in rwa:
            RWA.append(int(i))
        self.RWA=sorted(RWA)                           #RWA为rwa的元素int化 self.RWA为升序后的RWA 为了在KBBJ中调用故设为self.
        self.read_week_afx={}                              #通过RWA的键将read_week中对应的值复制到self.read_week_afx
        for k in self.RWA:
            self.read_week_afx[str(k)]=read_week[str(k)]


        #创建科目显示控件
        self.zaodu=tk.Label(self.root,text='早  读',bg=self.gcc,font=("Arial",16),height=1,fg=self.font_color)
        self.zaodu.pack()
        self.sil1=tk.Label(self.root,text=self.read_week_afx['1']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil1.pack()
        self.zaoshang=tk.Label(self.root,text='早  课',bg=self.gcc,font=("Arial",16),height=1,fg=self.font_color)
        self.zaoshang.pack()
        self.sil2=tk.Label(self.root,text=self.read_week_afx['2']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil2.pack()
        self.sil3=tk.Label(self.root,text=self.read_week_afx['3']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil3.pack()
        self.sil4=tk.Label(self.root,text=self.read_week_afx['4']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil4.pack()
        self.sil5=tk.Label(self.root,text=self.read_week_afx['5']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil5.pack()
        self.sil6=tk.Label(self.root,text=self.read_week_afx['6']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil6.pack()
        self.zhongwu=tk.Label(self.root,text='午  课',bg=self.gcc,font=("Arial",16),height=2,fg=self.font_color)
        self.zhongwu.pack()
        self.sil7=tk.Label(self.root,text=self.read_week_afx['7']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil7.pack()
        self.sil8=tk.Label(self.root,text=self.read_week_afx['8']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil8.pack()
        self.sil9=tk.Label(self.root,text=self.read_week_afx['9']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil9.pack()
        self.sil10=tk.Label(self.root,text=self.read_week_afx['10']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil10.pack()
        self.xiawu=tk.Label(self.root,text='晚  课',bg=self.gcc,font=("Arial",16),height=2,fg=self.font_color)
        self.xiawu.pack()
        self.sil11=tk.Label(self.root,text=self.read_week_afx['11']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil11.pack()
        self.sil12=tk.Label(self.root,text=self.read_week_afx['12']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil12.pack()
        self.sil13=tk.Label(self.root,text=self.read_week_afx['13']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil13.pack()
        self.sil14=tk.Label(self.root,text=self.read_week_afx['14']['科目'],bg=self.gcc,font=("黑体",16),fg=self.font_color)
        self.sil14.pack()

    def update_lesson(self):
        '''TimetableWindow函数,更新实时科目信息,判断并导出red_lesson'''
        j_d={'语文':'chinese','数学':'math','英语':'english','物理':'physics','化学':'chemistry','生物':'biology','政治':'biology','历史':'history','地理':'geography','其他':'others',}
        def red_lesson(li):
            '''导出red_lesson'''
            with open(os.getcwd()+'\\Schedule_Info\\red_lesson.json','w') as writeweek:
                if li['科目'] not in j_d.keys():                 #将录入信息的中文转换为英文
                    jkm='others'
                else:
                    jkm=j_d[li['科目']]
                J={'lesson_information':jkm,'start_time':li['上课时间'],'finish_time':li['下课时间'],}
                json.dump(J,writeweek) 
        def Time_character_concatenation(time:tuple,time_slot:int):
            '''在07:00:00格式的时间字符串中拼接一个时间段   time_slot+time[1]不能>=120'''
            if time[1]+time_slot <60:
                localtime_hour=time[0]
                localtime_mintue=str(time[1]+time_slot)
            elif time[1]+time_slot >=60:
                localtime_hour=str(time[0]+1)
                localtime_mintue=str(time_slot+time[1]-60)
            return self.change_time_shape((localtime_hour,localtime_mintue)) 
        def zxh(s,b):
            '''最小化所有窗口,恢复课表窗口'''
            pyautogui.keyDown('winleft')    # winleft
            pyautogui.press('d')    # 按下 d
            pyautogui.keyUp('winleft')   # 释放 winleft
            self.root.deiconify()
            self.root_set.deiconify()
            self.deiconify()
        
        self.localtime=TIME.localtime(TIME.time())     
        self.localtime_cs=self.change_time_shape((self.localtime[3],self.localtime[4]))   
        
        '''print(1,self.is_time_in_range(self.read_week_afx['1']['上课时间'],self.read_week_afx['1']['下课时间'],self.localtime_cs))
        print(2,self.is_time_in_range(self.read_week_afx['2']['上课时间'],self.read_week_afx['2']['下课时间'],self.localtime_cs))
        print(3,self.is_time_in_range(self.read_week_afx['3']['上课时间'],self.read_week_afx['3']['下课时间'],self.localtime_cs))
        print(4,self.is_time_in_range(self.read_week_afx['4']['上课时间'],self.read_week_afx['4']['下课时间'],self.localtime_cs))
        print(5,self.is_time_in_range(self.read_week_afx['5']['上课时间'],self.read_week_afx['5']['下课时间'],self.localtime_cs))
        print(6,self.is_time_in_range(self.read_week_afx['6']['上课时间'],self.read_week_afx['6']['下课时间'],self.localtime_cs))
        print(7,self.is_time_in_range(self.read_week_afx['7']['上课时间'],self.read_week_afx['7']['下课时间'],self.localtime_cs))
        print(8,self.is_time_in_range(self.read_week_afx['8']['上课时间'],self.read_week_afx['8']['下课时间'],self.localtime_cs))
        print(9,self.is_time_in_range(self.read_week_afx['9']['上课时间'],self.read_week_afx['9']['下课时间'],self.localtime_cs))
        print(10,self.is_time_in_range(self.read_week_afx['10']['上课时间'],self.read_week_afx['10']['下课时间'],self.localtime_cs))
        print(11,self.is_time_in_range(self.read_week_afx['11']['上课时间'],self.read_week_afx['11']['下课时间'],self.localtime_cs))
        print(12,self.is_time_in_range(self.read_week_afx['12']['上课时间'],self.read_week_afx['12']['下课时间'],self.localtime_cs))
        print(13,self.is_time_in_range(self.read_week_afx['13']['上课时间'],self.read_week_afx['13']['下课时间'],self.localtime_cs))
        print(14,self.is_time_in_range(self.read_week_afx['14']['上课时间'],self.read_week_afx['14']['下课时间'],self.localtime_cs))
        print(self.localtime_cs)'''

        #以下获取每节课下课时间+10分钟的时间
        time1_1=Time_character_concatenation(self.time_convert(self.read_week_afx['1']['下课时间']),10)
        time2_1=Time_character_concatenation(self.time_convert(self.read_week_afx['2']['下课时间']),10)
        time3_1=Time_character_concatenation(self.time_convert(self.read_week_afx['3']['下课时间']),10)
        time4_1=Time_character_concatenation(self.time_convert(self.read_week_afx['4']['下课时间']),10)
        time5_1=Time_character_concatenation(self.time_convert(self.read_week_afx['5']['下课时间']),10)
        time6_1=Time_character_concatenation(self.time_convert(self.read_week_afx['6']['下课时间']),10)
        time7_1=Time_character_concatenation(self.time_convert(self.read_week_afx['7']['下课时间']),10)
        time8_1=Time_character_concatenation(self.time_convert(self.read_week_afx['8']['下课时间']),10)
        time9_1=Time_character_concatenation(self.time_convert(self.read_week_afx['9']['下课时间']),10)
        time10_1=Time_character_concatenation(self.time_convert(self.read_week_afx['10']['下课时间']),10)
        time11_1=Time_character_concatenation(self.time_convert(self.read_week_afx['11']['下课时间']),10)
        time12_1=Time_character_concatenation(self.time_convert(self.read_week_afx['12']['下课时间']),10)
        time13_1=Time_character_concatenation(self.time_convert(self.read_week_afx['13']['下课时间']),10)
        time14_1=Time_character_concatenation(self.time_convert(self.read_week_afx['14']['下课时间']),10)

        
        #以下if块中判断 正在进行 的科目并修改字体颜色,导出red_lesson信息    
        if   self.is_time_in_range(self.read_week_afx['1']['上课时间'],time1_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg='red',bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['2'])
            if self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['1']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1] and self.a==0:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.a+=1
        elif self.is_time_in_range(self.read_week_afx['2']['上课时间'],time2_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg='red',bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['3'])
            if   self.b==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['2']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.b+=1
        elif self.is_time_in_range(self.read_week_afx['3']['上课时间'],time3_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg='red',bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['4'])
            if self.c==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['3']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.c+=1
        elif self.is_time_in_range(self.read_week_afx['4']['上课时间'],time4_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg='red',bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['5'])
            if self.d==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['4']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.d+=1
        elif self.is_time_in_range(self.read_week_afx['5']['上课时间'],time5_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg='red',bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['6'])
            if self.e==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['5']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.e+=1
        elif self.is_time_in_range(self.read_week_afx['6']['上课时间'],time6_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg='red',bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['7'])
            if self.f==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['6']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.f+=1
        elif self.is_time_in_range(self.read_week_afx['7']['上课时间'],time7_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg='red',bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['8'])
            if self.g==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['7']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.g+=1
        elif self.is_time_in_range(self.read_week_afx['8']['上课时间'],time8_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg='red',bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['9'])
            if self.h==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['1']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.h+=1
        elif self.is_time_in_range(self.read_week_afx['9']['上课时间'],time9_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg='red',bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['10'])
            if self.i==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['9']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.i+=1
        elif self.is_time_in_range(self.read_week_afx['10']['上课时间'],time10_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg='red',bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['11'])
            if self.j==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['10']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.j+=1
        elif self.is_time_in_range(self.read_week_afx['11']['上课时间'],time11_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg='red',bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['12'])
            if self.k==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['11']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.k+=1
        elif self.is_time_in_range(self.read_week_afx['12']['上课时间'],time12_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg='red',bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            red_lesson(self.read_week_afx['13'])
            if self.l==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['12']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.l+=1
        elif self.is_time_in_range(self.read_week_afx['13']['上课时间'],time13_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg='red',bg=self.gcc)
            red_lesson(self.read_week_afx['14'])
            self.Time_FUll_Screen()
            if self.m==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['13']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.m+=1
        elif self.is_time_in_range(self.read_week_afx['14']['上课时间'],time14_1,self.localtime_cs):
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
            self.Time_FUll_Screen()
            if self.n==0 and self.time_convert(Time_character_concatenation(self.time_convert(self.read_week_afx['14']['下课时间']),2))[1]==self.time_convert(self.localtime_cs)[1]:
                #每到下课两分钟后最小化所有窗口,恢复课表窗口
                zxh()
                self.n+=1
        else:
            self.sil1.config(fg=self.font_color,bg=self.gcc)
            self.sil2.config(fg=self.font_color,bg=self.gcc)
            self.sil3.config(fg=self.font_color,bg=self.gcc)
            self.sil4.config(fg=self.font_color,bg=self.gcc)
            self.sil5.config(fg=self.font_color,bg=self.gcc)
            self.sil6.config(fg=self.font_color,bg=self.gcc)
            self.sil7.config(fg=self.font_color,bg=self.gcc)
            self.sil8.config(fg=self.font_color,bg=self.gcc)
            self.sil9.config(fg=self.font_color,bg=self.gcc)
            self.sil10.config(fg=self.font_color,bg=self.gcc)
            self.sil11.config(fg=self.font_color,bg=self.gcc)
            self.sil12.config(fg=self.font_color,bg=self.gcc)
            self.sil13.config(fg=self.font_color,bg=self.gcc)
            self.sil14.config(fg=self.font_color,bg=self.gcc)
        self.root.after(1000, lambda: self.update_lesson())    #每秒调用一次red_lesson()函数

    def Time_FUll_Screen(self):
            '''创建一个全屏显示的实时时间窗口'''
            fn=os.getcwd()
            with open(fn+'\\Schedule_Info\\profile.json','r') as readweek:
                read_week = json.load(readweek)
                countdown=read_week['countdown']
                    
            def exit_time():
                '''关闭实时时间窗口'''
                root_time.destroy()
            def update_time():
                '''更新实时时间窗口'''
                with open(fn+'\\Schedule_Info\\profile.json','r') as readweek:
                    read_week = json.load(readweek)
                    countdown=read_week['countdown']
                current_time = datetime.now().strftime('%H:%M:%S')#[:-4]
                time_label.config(text=current_time)     #time_label控件更新
                root_time.after(1, update_time)  # 每隔1秒更新时间


            root_time = tk.Toplevel()
            root_time.geometry("%dx%d" % (self.screenWidth,self.screenHeight))
            root_time.resizable(0, 0)
            root_time.overrideredirect(True)
            root_time.wm_attributes('-topmost',1)
            button1 = tk.Button(root_time , text='退出全屏'  ,fg='black', command=exit_time ,bd=0 , width=8 ,font=('黑体',15))
            button1.place(x=self.screenWidth*0.833,y=self.screenHeight*0.926)#(x=1400,y=self.screenHeight*0.5)
            button2 = tk.Button(root_time , text='倒计时'  ,fg='black', command='' , bd=0 , width=8 ,font=('黑体',15))
            button2.place(x=self.screenWidth*0.726,y=self.screenHeight*0.926)
            time_label = tk.Label(root_time, font=("Arial", 200),fg='#FF0000')
            time_label.place(x=self.screenWidth*0.1627,y=self.screenHeight*0.26)#0.045
            update_time()

    def Font_Color_Change(self):
        '''改变软件主题'''
        fn=os.getcwd()

        
        with open(fn+'\\Schedule_Info\\profile.json','r') as readweek:
            read_week = json.load(readweek)
            theme=read_week['theme']
        with open(fn+'\\Schedule_Info\\profile.json','w') as writeweek:
            if theme=='lightcolour':
                aegaweg='deepcolour'
            elif    theme=='deepcolour':
                aegaweg='multicolour'
            elif theme=='multicolour':
                aegaweg='lightcolour'
            read_week['theme']=aegaweg
            json.dump(read_week,writeweek)


        
        
        if aegaweg=='multicolour':
            self.screenWidth = self.winfo_screenwidth()  # 获取显示区域的宽度
            self.screenHeight = self.winfo_screenheight()  # 获取是否�示�域的高宽数据
            left,top = self.screenWidth - 150,int(self.screenHeight/172.8)+30
            gca=get_color(left, top)
            gcc=RGB_to_Hex((int((gca[0])),int((gca[1])),int((gca[2]))))
            self.gcc=gcc
        else:
            self.gcc=self.theme_d[aegaweg][1]
        print(self.gcc)
        self.font_color=self.theme_d[aegaweg][0]
        self.root.config(bg=self.gcc)
        self.configure(bg=self.gcc)
        if self.gcc=='white':
            self.root_set.configure(background=self.gcc)
            self.button1.configure(bg=self.gcc)
            self.button2.configure(bg=self.gcc)
            self.button3.configure(bg=self.gcc)
            self.button4.configure(bg=self.gcc)
            self.button5.configure(bg=self.gcc)
        else:
            self.root_set.configure(background='grey')
            self.button1.configure(bg='grey')
            self.button2.configure(bg='grey')
            self.button3.configure(bg='grey')
            self.button4.configure(bg='grey')
            self.button5.configure(bg='grey')
        self.update_lesson()
        self.zaodu.configure(bg=self.gcc,fg=self.font_color)
        self.zaoshang.configure(bg=self.gcc,fg=self.font_color)
        self.xiawu.configure(bg=self.gcc,fg=self.font_color)
        self.zhongwu.configure(bg=self.gcc,fg=self.font_color)
        self.time_label2.config(bg=self.gcc)


        


    def set_buttons_Window(self):
        '''TimetableWindow函数,安装程序设置按钮'''
        fn=os.getcwd()

        def EXit():
            '''关闭主程序'''
            os._exit(0)


        image_close = Image.open(fn+"\\ico\\软件关闭.png")         #关闭按钮
        photo = image_close.resize((20,20))  #规定图片大小
        self.photoimage_close = ImageTk.PhotoImage(photo)
        self.button1 = tk.Button(self.root_set , image = self.photoimage_close , bg=self.gcc1 , command=EXit , bd=0 , width=100 , height=35)
        self.button1.pack(side=tk.BOTTOM)

        image_setting = Image.open(fn+"\\ico\\课表编辑.png")         #课表编辑按钮
        photo = image_setting.resize((20,20))  #规定图片大小
        self.photoimage_setting = ImageTk.PhotoImage(photo)
        self.button2 = tk.Button(self.root_set ,image = self.photoimage_setting, command=self.KBBJ , bg=self.gcc1 , bd=0 , width=100 , height=35)
        self.button2.pack(side=tk.BOTTOM)
        
        image_time = Image.open(fn+"\\ico\\时间全屏.png")         #时间全屏按钮
        photo = image_time.resize((20,20))  #规定图片大小
        self.photoimage_time = ImageTk.PhotoImage(photo)
        self.button3 = tk.Button(self.root_set , image=self.photoimage_time , command=self.Time_FUll_Screen , bg=self.gcc1 , bd=0 , width=100 , height=35)
        self.button3.pack(side=tk.BOTTOM)

        image_theme = Image.open(fn+"\\ico\\主题切换.png")         #主题切换按钮
        photo = image_theme.resize((20,20))  #规定图片大小
        self.photoimage_theme = ImageTk.PhotoImage(photo)
        self.button4 = tk.Button(self.root_set , image=self.photoimage_theme , command=self.Font_Color_Change , bg=self.gcc1 , bd=0 , width=100 , height=35)
        self.button4.pack(side=tk.BOTTOM)

        image_language = Image.open(fn+"\\ico\\语言切换.png")         #语言切换按钮
        photo = image_language.resize((20,20))  #规定图片大小
        self.photoimage_language = ImageTk.PhotoImage(photo)
        self.button5 = tk.Button(self.root_set , image=self.photoimage_language , command='' , bg=self.gcc1 , bd=0 , width=100 , height=35)
        self.button5.pack(side=tk.BOTTOM)

    def update_time(self):
        '''TimetableWindow函数,更新实时时间窗口'''
        current_time1 = TIME.strftime("%H:%M:%S", TIME.localtime())
        self.time_label2.config(text=current_time1,bg=self.gcc)     #time_label2控件更新
        self.after(1000, self.update_time)  # 每隔1秒更新时间


    def red_lesson(self):
        '''TimetableWindow函数,导出标红课时信息'''
        j_d={'语文':'chinese','数学':'math','英语':'english','物理':'physics','化学':'chemistry','生物':'biology','政治':'biology','历史':'history','地理':'geography','其他':'others',}
        for i,j in self.read_week_afx.items():
            if self.is_time_in_range(j['上课时间'],j['下课时间'],self.localtime_cs_next):
                with open(os.getcwd()+'\\Schedule_Info\\red_lesson.json','w') as writeweek:
                    if j['科目'] not in j_d.keys():                 #将录入信息的中文转换为英文
                        jkm='others'
                    else:
                        jkm=j_d[j['科目']]
                    J={'lesson_information':jkm,'start_time':j['上课时间'],'finish_time':j['下课时间'],}
                    json.dump(J,writeweek)
        self.root.after(1000, lambda: self.red_lesson())    #每秒调用一次red_lesson()函数

    def run(self):
        '''TimetableWindow函数,运行主程序'''
        self.set_buttons_Window()
        self.update_time()
        self.kmxs()
        self.update_lesson()      

        self.root_set.mainloop()





window_timetable = TimetableWindow()
window_timetable.run()

'''def yunxin():
    while True:
        window_timetable = TimetableWindow()
        window_timetable.run()

t4 = threading.Thread(target=yunxin) 
t4.setDaemon=True
t4.start()'''


'''t1 = threading.Thread(target=TimeWindow_Date.mainloop) 
t1.setDaemon=True
t1.start()
window_time = TimeWindow_Date()'''





'''t3 = threading.Thread(target=TimetableWindow.run) 
t3.setDaemon(True) 
t3.start()'''
