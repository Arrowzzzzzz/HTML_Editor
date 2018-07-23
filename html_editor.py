#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Arrowzzzzzz@protonmail.com
#html编辑器(自用)
import time,Tkinter,tkFileDialog,re,tkMessageBox,pprint     #time获取本地时间,boTkinter图形界面,pprint和php中var_dump一样
re_list = [r'<title>(\n*.*)</title>',r'<h1>环境:系统(\n*.*)</h1>',r'<h1>来源于:(\n*.*)</h1>']      #title,系统,来源的正则
re_img = [r'src="(\n*.*)" title="',r'title="(\n*.*)" alt="',r'alt="(\n*.*)"']       #img的正则
class ArrowHtml():      #类
    def __init__(self):
        self.html_time = time.strftime('%Y年%m月%d日 %H:%M:%S',time.localtime(time.time()))        #strftime接收时间,并以特定的格式输出,localtime输出元组(年月日等)并且可以将秒变成年月日格式元组,time显示1970(unix出生时间)到今天的秒速.
        self.html_nbsp = "&nbsp"

    def Write_html(self,File_name,New_title,New_system,Data,New_sources):         #标题,实验系统环境,内容
        with open(File_name + ".html","w+") as htmlfile :       #创建文件
            htmlfile.write('<!DOCTYPE HTML>\n\t<html>\n\t\t<head>\n\t\t\t<meta charset="utf-8">\n\t\t\t<title>%s</title>\n\t\t</head>\n\t\t<body>\n\t\t编辑日期:%s<br />\n\t\t<h1>环境:系统%s</h1>\n\t\t<h1>来源于:%s</h1>\n' %(New_title.encode("utf-8"),self.html_time,New_system.encode("utf-8"),New_sources.encode("utf-8")))          #写HTML框架并且title,time,system,sources内容
            htmlfile.write(Data.encode("utf-8"))        #指定编码格式,写text内容
            htmlfile.write("\t\t</body>\n\t</html>")        #闭合body和html标签

    def ask_quit(self) :        #退出确认函数
        if tkMessageBox.askyesno("Tip", "Exit?"):       #tkMessageBox是一个消息框模块,askyesno是显示yes和no按钮 问号图标
            Window.destroy()        #destroy关闭窗口

    def Set_setting(self):      #获取字段,并且判断使用的标签
        New_system = Arrow_system.get()         #实验系统环境内容
        New_title = Arrow_title.get()           #网站标题内容
        New_sources = Arrow_sources.get()       #来源内容Datas
        Sources_data = Arrow_text.get("0.0","end")          #获取text内容,从0.0到最后(end是最后)
        File_name = Arrow_file_name.get()       #文件名内容
        Datas = Sources_data.split('\n')        #将text内容按回车分为不同的列
        Data = ""
        for i in range(len(Datas)-1):       #获取Datas中有几列,并去除最后一个空\n
            Data_h = Datas[i].split('\t')        #将Datas中第一列,按\t分为不同的列
            H_number = len(Data_h)             #定义是h几标签
            Html_h = 1      #初始化h几标签
            if Datas[i][0] == "\t":         #不是H1标签
                Html_h = H_number           #定义H几标签
                Data_len = len(Datas[i])        #长度(主要获取列有多长)
                Data_t = Datas[i][int(Html_h-1):Data_len]        #列中除去\t全部数据
                if Data_t[0:4] == "img " :      #判断是否是图片
                    Data_img = Data_t.split(' ')  # 按空格分为不同的列
                    Data = Data + "\t" + "\t"*int(Html_h) + self.html_nbsp*4*int(Html_h-1) + '<img src="' + Data_img[1] + '" title="' + Data_img[2] + '" alt="' + Data_img[3] + '">\n'  # img数据
                else :
                    Data = Data + "\t" + "\t"*int(Html_h) + "<h" + str(Html_h) + ">" + self.html_nbsp*4*int(Html_h-1) + Data_t + "</h" + str(Html_h) + ">\n"          #数据
            elif Datas[i][0:4] == "img ":       #判断是否是图片
                Data_img = Datas[i].split(' ')         #按空格分为不同的列
                Data = Data + '\t\t<img src="' + Data_img[1] + '" title="' + Data_img[2] + '" alt="' + Data_img[3] + '">\n'         #数据
            elif Datas[i][0] == " " :       #判断是否是开头空格
                Datas_nbsp = Datas[i].split(" ")        #以空格切割成列表
                Nbsp_number = len(Datas_nbsp)       #看列表长度
                for z in range(Nbsp_number - 1) :       #循环列表
                    if Datas_nbsp[z] == "img" :     #判断是否是图片
                        if_img = 0      #标记
                        break
                    else :
                        if_img = 1      #标记
                if if_img == 1 :        #不是图片
                    Data = Data + "\t\t<h" + str(Html_h) + ">" + self.html_nbsp * (Nbsp_number - 1) + Datas_nbsp[Nbsp_number - 1] + "</h" + str(Html_h) + ">\n"  # 数据
                else :      #是图片
                    Data = Data + "\t\t" + self.html_nbsp*(Nbsp_number-4) + '<img src="' + Datas_nbsp[-3] + '" title="' + Datas_nbsp[-2] + '" alt="' + Datas_nbsp[-1] + '">\n'  # 数据
            else :      #判断是H1标签
                Data = Data + "\t\t<h" + str(Html_h) + ">" + Datas[i] +"</h" + str(Html_h) + ">\n"          #数据
            self.Write_html(File_name,New_title, New_system, Data, New_sources)       #传输数据到写入html函数中

    def Save(self):     #快捷键ctrl+s调用函数
        self.Set_setting()      #保存文件
    def File_open(self):        #打开文件函数
        filepath = tkFileDialog.askopenfilename(initialdir='C:/')       #tkFileDialog是打开文件的对话框,initialdir指定每次显示C盘文件
        filename_list = filepath.split('/')     #以斜杠切割成列表
        filename = filename_list[-1:]       #获取文件名(带后缀)
        with open(filepath) as file_html:       #打开文件
            file_content = file_html.read()     #读取里面的内容
            file_list = []
            for i in re_list:       #循环读取title,系统,来源的正则
                re_re= re.compile(i)  # 将i中字段写入到规则中
                re_result = re_re.findall(file_content)     #执行规则，并且输出查找到的结果
                for o in re_result:     #循环读取结果
                    file_list.append(o)     #将结果添加到列表中
            re_body = r'<h1>来源于:%s</h1>\n([\s\S]*)\n\t\t</body>' %file_list[2]      #利用变量，构成正文内容正则
            re_re= re.compile(re_body)  # 将正文内容正则写入到规则中
            re_result = re_re.findall(file_content)     #执行规则，并且输出查找到的结果
            re_result = re.sub(r'</*h\d*>', "", "".join(re_result))     #去除<h*>,</h*>的字段
            re_result = re.sub(r'(&nbsp)*', "", "".join(re_result))     #取出&nbsp的字段
            File_text_list = "".join(re_result).split('\n')     #以斜杠切割成列表
            tmp_text = ""
            for i in File_text_list:        #循环列表
                if "<img" in i:     #i中是否有<img
                    img_str = ""
                    for img in re_img:      #循环img正则
                        re_re = re.compile(img)     #将img正则写入到规则
                        re_result = re_re.findall(i)        #执行规则，并且输出查找到的结果
                        img_str= img_str + "".join(re_result) + " "     #构建img内容
                    tmp_text = tmp_text + "img " + img_str[:-1] + "\n"      #形成完整的img内容
                else :
                    tmp_text = tmp_text + i[2:] + "\n"      #添加正文内容
        File_title = file_list[0]       #title内容
        File_system = file_list[1]      #system version内容
        File_source = file_list[2]      #source内容
        File_text = tmp_text        #text内容
        Arrow_file_name.insert(Tkinter.INSERT,"".join(filename)[:-5])       #将文件名插入到图形file_name中
        Arrow_title.insert(Tkinter.INSERT,File_title)       #将title插入到图形title中
        Arrow_system.insert(Tkinter.INSERT,File_system)     #将系统信息插入到图形system_version中
        Arrow_sources.insert(Tkinter.INSERT,File_source)        #将来源插入到图形sources中
        Arrow_text.insert(Tkinter.INSERT,File_text)     #将正文内容插入到图形text中
Window = Tkinter.Tk()       #调用Tkinter中TK接口
Window.title("My HTML Editor")          #图形界面的标题框名
w,h = Window.maxsize()          #获取当前分辨率
html_w = round(w*0.8,0)         #返回浮点数,的四舍五入值(小数点0位)
html_h = round(h*0.8,0)         #返回浮点数,的四舍五入值(小数点0位)
ground_w = (w - html_w) / 2     #偏移宽量
ground_h = (h - html_h) / 2     #偏移高量
Window.geometry("%sx%s+%s+%s"%(str(html_w)[:-2],str(html_h)[:-2],str(ground_w)[:-2],str(ground_h)[:-2]))         #图形界面宽,高,偏移量
Window.minsize(800,600)         #限制最小宽高
#---------------------------------------自适应---------------------------------------------------
Window.columnconfigure(1,weight=1)          #配置列,1代表从第0列开始,weight添加几个像素
Window.rowconfigure(2,weight=1)             #配置行,2代表从第2行开始,weight添加几个像素
#--------------------------------------------------------------------------------------------------
zzzzzz = ArrowHtml()        #使用ArrowHtml类
def Save_ctrl_s(event):         #ctrl+函数
    zzzzzz.Save()       #调用保存html函数
Tkinter.Label(Window,       #label标签
              text="Wecome to Arrowzzzzzz HTML Editor\nThe Elder Scrolls V：Skyrim is good game",  #窗口标签内容
              font=("Arial",16),          #标签字体和字体大小
              ).grid(row=0,columnspan=8,sticky="nsew")          #row是行,column是列,sticky是组件靠近单元格的某一角,n是北,s是南,e是东,w是西,columnspan是指定跨越列显示
Tkinter.Label(Window,       #生成文件名
              text="FILE_NAME:",        #标签内容
              font=("Arial",12),        #标签字体和字体大小
              ).grid(row=1,column=0,sticky="nsew")      #第1行,第0列
Arrow_file_name = Tkinter.Entry(Window)
Arrow_file_name.grid(row=1,column=1,sticky="nsew")           #entry是输入框,title输入框,第1行,第1列
Tkinter.Label(Window,       #标题
              text="TITLE:",          #标签内容
              font=("Arial",12),        #标签字体和字体大小
              ).grid(row=1,column=2,sticky="nsew")       #第1行,第0列
Arrow_title = Tkinter.Entry(Window)
Arrow_title.grid(row=1,column=3,sticky="nsew")           #entry是输入框,title输入框,第1行,第1列
Tkinter.Label(Window,       #实验系统环境
              text="System Version:",          #标签内容
              font=("Arial",12),     #标签字体和字体大小
              ).grid(row=1,column=4,sticky="nsew")       #第1行,第2列
Arrow_system = Tkinter.Entry(Window)
Arrow_system.grid(row=1,column=5,sticky="nsew")           #entry是输入框,实验系统环境输入框,第1行,第3列

Tkinter.Label(Window,       #来源
              text="SOURCES:",          #来源内容
              font=("Arial",12),        #来源字体和字体大小
              ).grid(row=1,column=6,sticky="nsew")       #第1行,第4列
Arrow_sources = Tkinter.Entry(Window)
Arrow_sources.grid(row=1,column=7,sticky="nsew")        #entry是输入框,sources输入框,第1行,第5列
Arrow_text = Tkinter.Text(Window,      #内容z
                   )
Arrow_text.grid(row=2,columnspan=8,sticky="nsew")     #第2行，横跨8列
Tkinter.Button(Window,      #生成文件
               text="Generate file",        #生成文件内容
               command=zzzzzz.Set_setting       #执行zzzzzz.Set_setting操作
               ).grid(row=3,columnspan=8,sticky="nswe")         #第3行，横跨8列
#---------------------------------------快捷键---------------------------------------------------
Arrow_text.bind("<Control-s>",Save_ctrl_s)          #ctrl+s
Arrow_text.bind("<Control-S>",Save_ctrl_s)          #ctrl+S
#---------------------------------------菜单---------------------------------------------------
menu_list = Tkinter.Menu(Window);       #menu是创建一个菜单类
menu_file = Tkinter.Menu(menu_list)         #在menu_list中在创建一个菜单类
menu_file.add_command(label="open",command=zzzzzz.File_open);          #add_command是添加菜单项，label是指定菜单名称
#menu_file.add_command(label="open",command=openfile);
menu_list.add_cascade(label="file",menu=menu_file)          #
Window["menu"]=menu_list        #将菜单应用到主窗口中

try:  # --------------------------------确认退出相关--------------------------------------
   Window.protocol("WM_DELETE_WINDOW",zzzzzz.ask_quit)
except:
   pass
Window.mainloop()           #运行图形界面