'''
wxPython 实现简单计算器
BoxSizer和GridSizer控制布局
一个textCtrl
按钮分别绑定事件
eval()计算结果
'''
# -*- coding: utf-8 -*-
#Python2.7
import wx
from math import *
class CalcFrame(wx.Frame):

    def __init__(self, title):
        super(CalcFrame, self).__init__(None, title=title,
            size=(300, 250))

        self.InitUI()
       # self.Centre()
        self.Show()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)#线性布局
        #文本输入控件 控件中文本右对齐
        self.textprint = wx.TextCtrl(self, style=wx.TE_RIGHT)
        self.equation = ""#存储textprint中函数
        vbox.Add(self.textprint, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        #表格布局 5行4列 行间距 列间距（像素）
        gridBox = wx.GridSizer(5, 4, 5, 5)

        labels = ['AC', 'DEL', 'pi', 'CLOSE', '7', '8', '9', '/', '4', '5', '6',
                  '*', '1', '2', '3', '-', '0', '.', '=', '+']
        for label in labels:
            buttonIterm = wx.Button(self, label=label)
            self.createHandler(buttonIterm, label)
            gridBox.Add(buttonIterm, 1, wx.EXPAND)
        #wx.EXPAND标志，我们的部件将使用所有已分配给它的空间
        #参数proportion管理窗口总尺寸，它是相对于别的窗口的改变而言的，它只对wx.BoxSizer有意义
        #参数border是窗口或sizer周围以像素为单位的空间总量
        vbox.Add(gridBox, proportion=7, flag=wx.EXPAND)
        self.SetSizer(vbox)

        # 创建按钮处理方法，根据label绑定事件回调函数

    def createHandler(self, button, labels):
        item = "DEL AC = CLOSE"
        if labels not in item:
            self.Bind(wx.EVT_BUTTON, self.OnAppend, button)
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.OnDel, button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON, self.OnAc, button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON, self.OnTarget, button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON, self.OnExit, button)

            # 添加运算符与数字,math.pi就是π

    def OnAppend(self, event):
        eventbutton = event.GetEventObject()
        label = eventbutton.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)#显示在输入框中

    def OnDel(self, event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def OnAc(self, event):
        self.textprint.Clear()
        self.equation = ""

    def OnTarget(self, event):
        string = self.equation
        try:
            #eval 将字符串str当成有效的表达式来求值并返回计算结果。
            target = eval(string)
            self.equation = str(target)
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            #在python2里面，u表示unicode string，类型是unicode, 没有u表示byte string，类型是 str。
#在python3里面，所有字符串都是unicode string, u前缀没有特殊含义了。
            dlg = wx.MessageDialog(self, u'格式错误，请输入正确的等式!',
                                   u'请注意', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnExit(self, event):
        self.Close()

if __name__ == '__main__':

    app = wx.App()
    CalcFrame(title='Calculator')
    app.MainLoop()
#MainLoop:程序的大部分时间花在了一个空闭的循环之中。进入这个循环就标志着程序与用户交互的部分的开始，退出这个循环就标志结束
