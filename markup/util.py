'''
python3 将txt文本解析生成HTML文件
逐行读入 根据源文本中的空行划分不同的块block 对每一块加标签
只涉及了一级标题、二级标题、文本段落、列表、超链接、*强调字体*
输入.txt文件 输出.html文件
'''
import sys,re
#将纯文本生成一个一个block
def lines(file):
    for line in file:yield line
    yield '/n'
def blocks(file):
    block = []
    for line in lines(file):
        if line.strip(): #strip()去掉字符串前后空格
            block.append(line)
        elif block:
            yield ''.join(block).strip()#join将列表项变成字符串
            block=[]
#处理程序 给文本块加html标签
class Handler():
    def callback(self,prefix,name,*args):
        method = getattr(self,prefix+name,None)#prefix+name: start_document()等函数
        if callable(method):return method(*args)#callable（）检查函数是否能被调用
    def start(self,name):
        self.callback('start_',name)
    def end(self,name):
        self.callback('end_',name)
    def sub(self,name):
        def substitution(match):#正则表达式替换
            result = self.callback('sub_',name,match)
            if result is None:result = match.group(0)
            return result
        return substitution
class HTMLRenderer(Handler):
    def __init__(self,f): #输出到文件f
        self.f = f
    def start_document(self): #网页标题
        print('<html><head><title>TestPythonMarkUp</title></head><body>',file=self.f)
    def end_document(self):
        print('</body></html>',file=self.f)
    def start_paragrap(self):
        print('<p style="color: #444;">',file=self.f)
    def end_document(self):
        print('</p>',file=self.f)
    def start_heading(self):
        print('<h2 style="color: #68BE5D;">',file=self.f)
    def end_heading(self):
        print('</h2>',file=self.f)
    def start_list(self):
        print('<ul style="color: #363736;">',file=self.f)
    def end_list(self):
        print('</ul>',file=self.f)
    def start_listitem(self):
        print('<li>',file=self.f)
    def end_listitem(self):
        print('</li>',file=self.f)
    def start_title(self):
        print('<h1 style="color: #1ABC9C;">',file=self.f)
    def end_title(self):
        print('</h1>',file=self.f)
    def sub_emphasis(self,match): #带*的强调字体
        return '<em>%s</em>' % match.group(1)
    def sub_url(self,match):
        return '<a target="_blank" style="text-decoration: none;color: #BC1A4B;" href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self,match):
        return '<a style="text-decoration: none;color: #BC1A4B;" href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self,data):
        print(data,file=self.f)
#每个文本块交给处理程序要用什么规则
class Rule():
    #加标记
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True
class HeadingRule(Rule):
    type = 'heading'
    #要符合规则
    def condition(self,block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    type ='title'
    first = True
    def condition(self,block):
        if not self.first : return False
        self.first = False
        return HeadingRule.condition(self,block)
class ListItemRule(Rule):#列表项
    type = 'listitem'
    def condition(self,block):
        return block[0]=='-'
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True
class ListRule(ListItemRule):#列表
    type = 'list'
    inside = False
    def condition(self,block):
        return True
    def action(self,block,handler):
        if not self.inside and ListItemRule.condition(self,block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self,block):
            handler.end(self.type)
            self.inside=False
        return False
class ParagraphRule(Rule):
        type = 'paragraph'
        def condition(self,block):
            return True
#解析
class Parser():
    def __init__(self,handler):
        self.handler = handler
        self.rules = []
        self.filters = []
        #添加规则
    def addRule(self,rule):
        self.rules.append(rule)
        #添加过滤器-- re 正则表达式
    def addFilter(self,pattern,name):
        def filter(block,handler):
            return re.sub(pattern,handler.sub(name),block)
        self.filters.append(filter)
        #逐块解析
    def parse(self,file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block,self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block,self.handler)
                    if last:break
        self.handler.end('document')
        #加入test.txt需要的规则
class BasicTextParser(Parser):
    def __init__(self,handler):
        Parser.__init__(self,handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z0-9]+@[\.a-zA-Z]+[a-zA-Z0-9]+)', 'mail')

inf = open('test.txt','r')
outf = open('test.html','w')
handler = HTMLRenderer(outf)
parser = BasicTextParser(handler)
parser.parse(inf)
inf.close()
outf.close()