import os.path

from django.shortcuts import render,reverse,HttpResponse
import json
import uuid
from django.urls import reverse

class web:
    #清洗文章把文章中的空格和换行符替换成html格式
    @classmethod
    def article_qx(cls,string):
        return string.replace('\n','<br>').replace(' ','&nbsp;')

    #判断是否是数字
    @classmethod
    def is_count(cls,string):
        '''
        :param string:
        :return: ，不是数字则返回false
        '''
        import re
        if re.match(r'(^([1-9][0-9]*|0)(\.[0-9]+)?$)', string):
            return True
        else:
            return False
    #用于传输ajax通信的消息
    @classmethod
    def get_message_user(cls,code, message):
        message = {
            'code': code,
            'message': message,
        }
        return HttpResponse(json.dumps(message), content_type='application/json')
    #获得随机8位数id
    @classmethod
    def get_8_id(cls):
        array = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                 "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u",
                 "v", "w", "x", "y", "z",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U",
                 "V", "W", "X", "Y", "Z"
                 ]
        id = str(uuid.uuid4()).replace("-", '')  # 注意这里需要用uuid4
        buffer = []
        for i in range(0, 8):
            start = i * 4
            end = i * 4 + 4
            val = int(id[start:end], 16)
            buffer.append(array[val % 62])
        return "".join(buffer)

    #djangoform类工具
    class django_form_tools:
        #获得django_form的报错提示
        @classmethod
        def geterror(cls,string):
            import re
            pattern = r'<li>(?!.*<li>).*?</li>'
            ret = re.findall(pattern=pattern, string=string)[0]
            return ret

    #页码类
    class paging:
        # 控制总页数的位置css
        # '''
        style = '''
            #feye_pages{
            line-height:34px;
            text-align: center;
            display: inline-block;
            margin-left: 20px;
            color:#337ab7;
        }
        .dx_Pages{
            width: 100%;
            text-align: center;
        }
        @media screen and (max-width: 390px){
            #feye_pages{
                display: block;
                margin-left: 0;
            }
            #page_nav ul{
                width: 100%;
                text-align: center;
                display: inline-block;
            }
            #page_nav ul li{
                text-align: center;
            }
        }
        '''


        def __init__(self ,request,obj,reser_name = ''):
            """
            :param request:  传入requst对象
            :param obj: 传入查询出来的model对象,要进行切割
            :param reser_name:反向解析的路由
            :return: meiyedata :切割出来的数据，pages 返回出来的页码组件，style css
            """
            morenper_page_num =12 #默认每页展示多少个
            self.reser_name = reser_name
            data = request.GET.dict()
            # 判断是否有页码要求
            if data.get('page',None):
                try:
                    num = int(data.pop('page'))
                except:
                    num = 0
            else:
                num = 0
            self.page_num = num

            # 判断是否有每页展示多少个要求
            if data.get('per_page_num',None):
                try:
                    per_page_num = int(data['per_page_num'])
                except:
                    per_page_num = morenper_page_num
            else:
                per_page_num = morenper_page_num

            self.per_page_num = per_page_num

            #保存搜索条件
            if len(data) > 0 :
                self.search = '&'.join(f'{i}={data[i]}' for i in data)
            else:
                self.search = False

                #如果是mod对象则用
            # self.constom_count = obj.count()

            #如果是其它数据类型
            self.constom_count = len(obj)

            #翻转列表
            # self.obj = list(reversed(obj))
            self.obj = list(obj)

            #求出余数和商
            shang, yu = divmod(self.constom_count, self.per_page_num)
            if yu:
                self.page_num_count = shang + 1
            else:
                self.page_num_count = shang
            #判断页码数是否正确
            if self.page_num <=0:
                self.page_num = 1
            elif self.page_num > self.page_num_count:
                self.page_num=self.page_num_count
            try :
                self.page_num-1
            except:
                self.page_num=1

            self.meiyedata = self.ret_data()
            self.pages = self.ret_page()

        #返回页码对应的数据
        def ret_data(self):
            # 控制要传出的数据条数
            self.start_page = (self.page_num - 1) * self.per_page_num
            self.end_page = self.page_num * self.per_page_num
            self.obj_list = self.obj[self.start_page:self.end_page]
            return  self.obj_list

        #返回页码组件
        def ret_page(self):
            '''

            :param search: 这个用来保存搜索的，当搜索后也要有分页时输入这个保持搜索条件，同时分页。
            ;:param reser_name : 传入url 名称，用来确定反向解析出网址
            :return:
            '''
            # 控制页码显示逻辑
            html = reverse(f'{self.reser_name}')
            if self.page_num_count <= 5:  # 如果页数小于5 显示页数大小
                start_ym = 1
                end_ym = self.page_num_count
            elif self.page_num  - 3 <= 0:  # 如果页码 小于三 显示前五页
                end_ym = 5
                start_ym = 1
            elif self.page_num  - self.page_num_count >= -2:  # 如果页码 大于最后前三位 显示最后五页
                start_ym = self.page_num_count - 4
                end_ym = self.page_num_count
            else:  # 其他情况显示五页
                start_ym = self.page_num - 2
                end_ym = self.page_num + 2

            #开始构造组件
            ym_qb = '<div class="dx_Pages">'
            # 构造开头页码
            if self.page_num == 1:
                ym_qb += '''<nav id='page_nav' aria-label="Page navigation"><ul class="pagination">
                <li class="disabled"><a href="javascript:void (0) " aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'''
            else:
                if self.search :
                    ym_qb += f'''<nav id='page_nav' aria-label="Page navigation"><ul class="pagination">
                    <li><a href="{html}?{self.search}&page={1} " aria-label="Next"><span aria-hidden="true">首</span></a></li>
                    <li class=""><a href="{html}?{self.search}&page={self.page_num-1} " aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'''
                else:
                    ym_qb += f'''<nav id='page_nav' aria-label="Page navigation"><ul class="pagination">
                    <li><a href="{html}?page={1}" aria-label="Next"><span aria-hidden="true">首</span></a></li>
                    <li class=""><a href="{html}?page={self.page_num-1} " aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'''
            #构造中间页码
            ym = ""
            for i in  range(start_ym,end_ym + 1) :
                if i ==self.page_num:
                    if self.search :
                        ym1 = f"<li class='active'><a href='{html}?{self.search}&page={i}'>{i}</a></li>"
                    else:
                        ym1 = f"<li class='active'><a href='{html}?page={i}'>{i}</a></li>"
                else:
                    if self.search:
                        ym1 = f"<li><a href='{html}?{self.search}&page={i}'>{i}</a></li>"
                    else:
                        ym1=f"<li><a href='{html}?page={ i }'>{ i }</a></li>"
                ym+=ym1
            ym_qb+=ym

            #构造结尾页码
            if self.page_num == self.page_num_count :
                end_next=f'''<li class="disabled" ><a href="javascript:void (0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li> 
                            '''
            else:
                if self.search :
                    end_next = f'''<li><a href="{html}?{self.search}&page={self.page_num + 1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
                                     <li><a href="{html}?{self.search}&page={self.page_num_count}" aria-label="Next"><span aria-hidden="true">尾</span></a></li>
    
    
                    '''
                else:
                    end_next=f'''<li><a href="{html}?page={self.page_num+1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
                                <li><a href="{html}?page={self.page_num_count}" aria-label="Next"><span aria-hidden="true">尾</span></a></li>                
                    '''
            end_end = f'''<span id ="feye_pages">总{self.page_num_count}页</span> </ul> </nav> </div>'''
            ym_qb+=end_next+end_end
            return ym_qb

#API相关类
class API:
    def __init__(self):pass

    #统一字典格式
    @classmethod
    def format_dict(cls,ret):
        dict1 = {}
        for i in ret:
            if isinstance(ret[i], int) or isinstance(ret[i], str):
                dict1[i] = ret[i]
            elif type(ret[i]) == "<class 'decimal.Decimal'>":
                dict1[i] = float(ret[i])
            else:
                dict1[i] = str(ret[i])
        return dict1
#字符串处理
class string_tools:
    def __init__(self):pass
    #获得中文
    @classmethod
    def re_chinese(cls,string):
        import re
        print(string)
        pattern = r'[\u4e00-\u9fa5]+'
        ret = re.findall(pattern=pattern, string=string)
        return ret[0]
#爬虫相关
class spider_tools:
    #格式化请求头
    @classmethod
    def return_header(cls,str1):
        '''
        输入请求头原字符串，返回格式化的字典用于request请求
        :param str:
        :return:
        '''
        headers = {}
        for i in str1.split('\n'):
            if len(i) == 0:continue
            ret = i.split(':',1)
            if len(ret) == 1:continue
            headers[ret[0].strip()] = ret[1].strip()
        return headers
    #格式化params 字符串为字典
    @classmethod
    def return_params(paramstr):
        paramsdic = {}
        for i in paramstr.split('&'):
            ret = i.split('=')
            print(ret)
            paramsdic[ret[0]] = ret[1]
        return paramsdic
    # 格式化fiddler的请求头
    @classmethod
    def turn_fiddler_payload(cls,raw):
        newdata = [ i.replace('        ','') for i in raw.split('\n') if len(i.replace('        ','')) >0]
        payload ={}
        for f in newdata:
            fgdata = f.split('\t')
            payload[fgdata[0]] = fgdata[1]
        return  payload
    # 下载的标题特俗符号处理
    @classmethod
    def title_replace(cls,title):
        '''
        :param title: 传入要更改的名字
        :return:
        '''
        title = title.replace('/', ' ').replace('?', '').replace('!', '').replace(',', '').replace('*', '').replace(':','').replace('★', '')
        return title

    #返回文件下载的标题
    @classmethod
    def get_downfilename(cls,ret):
        '''

        :param ret: 传入响应体
        :return:
        '''
        name = spider_tools.title_replace(ret.headers.get('Content-Disposition').encode('ISO-8859-1').decode('utf8').split('filename=')[1])
        return name

    #下载图片
    @classmethod
    def down_pic(cls,path,url,header):
        import requests
        '''
        :param path: 传入存放地址
        :param url: 下载链接
        :param header: 请求头，最好包含cookie
        :return: 下载成功返回true ，下载失败返回false
        '''
        try :
            data = requests.get(url,headers= header,verify=False,stream=True).content
            with open(path,mode='wb') as f :
                f.write(data)
            return True
        except:
            return  False
        # try :
        #     r = requests.get(url,headers= header,verify=False, stream=True)
        #     f = open(path, "wb")
        #     for chunk in r.iter_content(chunk_size=512):
        #         if chunk:
        #             f.write(chunk)
        #         return True
        # except:
        #     return  False

    #处理路径的特殊字符
    @classmethod
    def path_clean(self,path):
        return path.strip('\u202a')
#加密解密相关
class sign_tools:
    @classmethod
    def get_sign(cls,paragms,neadlist = [],deletelist = [],sign_and = '&',reverse = False):
        '''
        本方法用于加签时的排序，返回
        :param paragms: 传入字典
        :param neadlist: 需要的参数
        :param deletelist: 要删除的参数
        :param sign_and :链接 默认为 &
        :param reverse = True 降序 ， reverse = False 升序
        :return:
        '''
        new_paragms = {}
        if len(neadlist) == 0 :
            neadlist = paragms.keys()
        for i in neadlist:
            if i not in deletelist:
                new_paragms[i] = paragms[i]
        params_listjson = sorted(new_paragms.items(), key=lambda e: e[0],reverse = reverse)  # 参数字典倒排序为列表
        sign = sign_and.join(f'{k}={v}' for k, v in params_listjson)
        return sign
#os的封装
class dx_os:
    def __init__(self):pass

    #获得无后缀的文件名
    @classmethod
    def get_wuhouzhuifilename(cls,path):
        '''
        :param path: 传入路径
        :return:
        '''
        import os
        title_1ist = os.path.basename(path).split('.')
        if len(title_1ist) > 1:  # 去掉后缀
            title_1ist.pop(-1)
            title = ''.join(title_1ist)
        else:
            title = os.path.basename(path)
        return title
    #获得文件后缀
    @classmethod
    def get_file_houzhui(cls,path):
        '''
        :param path: 传入路径
        :return:
        '''
        import os
        houzhui  = path.split('.')[-1]
        return houzhui
    #获得可保存的无特殊符号的文件名
    @classmethod
    def get_chunjingfilename(cls,file):
        ts = ['?',r'\n']
        for i in ts:
            file = file.replace(i,'')
        return file
    #获得文件夹内所有文件的绝对路径，返回列表
    def get_fold_file_absolute(self,path):
        paths = os.walk(path)
        pathlist = [i for i in paths]
        newpathlist = [f'''{os.path.join(pathlist[0][0], i)}''' for i in pathlist[0][2]]
        return newpathlist
    #给文件随机重命名
    @classmethod
    def get_new_file_name(cls,filename):
        import time
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(time.time()).split('.')[0], ext)
        return filename
    #设置快捷方式
    @classmethod
    def set_shortcut(cls,filename, lnkname, argumensts, startpath, iconname=''):  # 如无需特别设置图标，则可去掉iconname参数
        '''

        :param filename: 文件完整路径
        :param lnkname: 快捷方式存放路径
        :param argumensts: 参数 --user-data-dir=E:softwaregooglechromesgooglechrome4 多开
        :param startpath: 开始位置
        :param iconname: 图标路径
        :return:
        '''
        import pythoncom
        from win32com.shell import shell
        from win32com.shell import shellcon
        try:
            # 将要在此路径创建快捷方式
            shortcut = pythoncom.CoCreateInstance(
                shell.CLSID_ShellLink, None,
                pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
            shortcut.SetPath(filename)
            shortcut.SetArguments(argumensts)
            shortcut.SetWorkingDirectory(startpath)  # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
            shortcut.SetIconLocation(iconname, 0)  # 可有可无，没有就默认使用文件本身的图标
            if os.path.splitext(lnkname)[-1] != '.lnk':
                lnkname += ".lnk"
            shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)
            return True
        except Exception as e:
            print(e.args)
            return False
    #设置快捷方式
    @classmethod
    def GetShortCut_path(cls,path):
        import struct
        target = ''
        try:
            with open(path, 'rb') as stream:
                content = stream.read()

                # skip first 20 bytes (HeaderSize and LinkCLSID)
                # read the LinkFlags structure (4 bytes)
                lflags = struct.unpack('I', content[0x14:0x18])[0]
                position = 0x18

                # if the HasLinkTargetIDList bit is set then skip the stored IDList
                # structure and header
                if (lflags & 0x01) == 1:
                    position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E

                last_pos = position
                position += 0x04

                # get how long the file information is (LinkInfoSize)
                length = struct.unpack('I', content[last_pos:position])[0]

                # skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
                position += 0x0C

                # go to the LocalBasePath position
                lbpos = struct.unpack('I', content[position:position + 0x04])[0]
                position = last_pos + lbpos

                # read the string at the given position of the determined length
                size = (length + last_pos) - position - 0x02
                temp = struct.unpack('c' * size, content[position:position + size])
                target = ''.join([chr(ord(a)) for a in temp])
        except:
            # could not read the file
            pass

        return target
    #path方面
    class path:
        #获得桌面路径
        @classmethod
        def get_desk_path(cls):
                return os.path.join(os.path.expanduser('~'), "Desktop")
        #判断是否是lnk文件
        @classmethod
        def is_link(cls,path):
            if path[-3:] == 'lnk':
                return True
            else:
                return False
#图像封装
class dx_img:

    #png转jpg
    @classmethod
    def png_jpg(cls,picpath,fold = False):
        from PIL import Image
        '''
        
        :param picpath: 要转换的图片
        :param fold: 是否需要放到新的文件夹，默认是当前地址
        :return: 成功返回新的地址  失败返回false
        '''
        img = Image.open(picpath)
        if not fold:
            newpath= os.path.join(os.path.dirname(picpath),f'''{dx_os.get_wuhouzhuifilename(picpath)}.jpg''')
        else:
            newpath = os.path.join(fold,f'''{dx_os.get_wuhouzhuifilename(picpath)}.jpg''')


        try:
            img.save(newpath)
            return  newpath
        except:
            try:
                img = img.convert('RGB')  # 1是以彩色图方式去读
                # 存放虚假展示图片
                img.save(newpath)

                print(picpath, '转换成功！')
        # 返回文件名
                return newpath
            except Exception as e:
                print(e)
                return False
if __name__ == '__main__':
    print(dx_img.png_jpg(r'G:\工作\爱赞助\QQ群基础文件\1_2.png'))