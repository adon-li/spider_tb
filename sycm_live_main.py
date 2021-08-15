# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import datetime

import dateutil
import wx
import wx.adv
from wx import *
from excel_utils.live_broadcast_business_advisor import LiveBroadcast
class MainFrame(wx.Frame):
    def __init__(self, *agrs, **kw):
        self.start = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.end = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        wx.Frame.__init__(self, size=(580, 400), *agrs, **kw)
        l1 = wx.StaticText(self, -1, u"提示：只能下载昨天之前的数据，并且跨度不能大于30天！！！", (30, 130))
        l1.SetForegroundColour("Red")
        # self.t1 = wx.TextCtrl(self, -1, "", (100, 50), size=(200, -1))

        cookie = wx.StaticText(self, -1, u"Cookies:", (30, 40))
        cookie.SetForegroundColour("Black")

        self.cookie = wx.TextCtrl(self, -1, "", (100, 20), size=(200, 50))

        date_start = wx.StaticText(self, -1, u"起始:", (30, 90))
        date_start.SetForegroundColour("Black")

        date_end = wx.StaticText(self, -1, u"结束:", (200, 90))
        date_end.SetForegroundColour("Black")

        self.edtDateb = wx.adv.DatePickerCtrl(self, id=-1, size=(90, 30), pos=(60, 85),
                                              style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY,
                                              dt=datetime.datetime.today() - datetime.timedelta(days=1))
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnCalSelChangedb, self.edtDateb)

        self.edtDatee = wx.adv.DatePickerCtrl(self, id=-1, size=(90, 30), pos=(230, 85),
                                              style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY,
                                              dt=datetime.datetime.today() - datetime.timedelta(days=1))
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnCalSelChangede, self.edtDatee)

        b4 = wx.Button(self, -1, u"开始下载数据", (370, 30))
        self.Bind(wx.EVT_BUTTON, self.b4Click, b4)

        # b5 = wx.Button(self, -1, u"开始下载直播回放累计数据", (370, 40))
        # self.Bind(wx.EVT_BUTTON, self.b5Click, b5)
        #
        # b6 = wx.Button(self, -1, u"开始下载直播商品成交数据", (370, 10))
        # self.Bind(wx.EVT_BUTTON, self.b6Click, b6)

        self.logger = wx.TextCtrl(self, pos=(30, 150), size=(470, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.df = None
        self.dfLength = 0
        self.currentRow = 0
        self.log(f"""正常启动""")
        self.log(f"""默认开始时间{self.start},结束时间{self.end}""")

    def log(self, text):
        self.logger.AppendText(f"""{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {text}\n""")

    def b4Click(self, evt):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0))
        if (dateutil.parser.parse(self.end) - today).days >= 0 or (
                dateutil.parser.parse(self.start) - today).days >= 0:
            self.log("日期不能大于今天")
            return
        days = (dateutil.parser.parse(self.end) - dateutil.parser.parse(self.start)).days
        last_days = (today - dateutil.parser.parse(self.start)).days
        if days < 0:
            self.log("开始日期必须小于结束日期")
            return
        elif days > 30 or last_days > 30:
            self.log("时间跨度大于30天！")
            return
        cookie = self.cookie.GetValue()
        if cookie is None or cookie == "":
            self.log("cookie不能为空")
        else:
            crawer = LiveBroadcast(cookies=cookie, log=self.log)
            crawer.live_order_detail_download(self.start,self.end)
            crawer.live_play_back_download(self.start, self.end)
            crawer.live_goods_transaction_download(self.start, self.end)

    def b3Click(self, evt):
        self.currentRow += 1
        wx.MessageBox(message=u"所有数据已经写完！！", caption=u"提示", parent=self)

    # def b5Click(self, evt):
    #     today = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0))
    #     if (dateutil.parser.parse(self.end) - today).days >= 0 or (
    #             dateutil.parser.parse(self.start) - today).days >= 0:
    #         self.log("日期不能大于今天")
    #         return
    #     days = (dateutil.parser.parse(self.end) - dateutil.parser.parse(self.start)).days
    #     last_days = (today - dateutil.parser.parse(self.start)).days
    #     if days < 0:
    #         self.log("开始日期必须小于结束日期")
    #         return
    #     elif days > 30 or last_days > 30:
    #         self.log("时间跨度大于30天！")
    #         return
    #     cookie = self.cookie.GetValue()
    #     if cookie is None or cookie == "":
    #         self.log("cookie不能为空")
    #     else:
    #         crawer = LiveBroadcast(cookies=cookie, log=self.log)
    #         crawer.live_play_back_download(self.start, self.end)
    # def b6Click(self, evt):
    #     today = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0))
    #     if (dateutil.parser.parse(self.end) - today).days >= 0 or (
    #             dateutil.parser.parse(self.start) - today).days >= 0:
    #         self.log("日期不能大于今天")
    #         return
    #     days = (dateutil.parser.parse(self.end) - dateutil.parser.parse(self.start)).days
    #     last_days = (today - dateutil.parser.parse(self.start)).days
    #     if days < 0:
    #         self.log("开始日期必须小于结束日期")
    #         return
    #     elif days > 30 or last_days > 30:
    #         self.log("时间跨度大于30天！")
    #         return
    #     cookie = self.cookie.GetValue()
    #     if cookie is None or cookie == "":
    #         self.log("cookie不能为空")
    #     else:
    #         crawer = LiveBroadcast(cookies=cookie, log=self.log)
    #         crawer.live_goods_transaction_download(self.start, self.end)
    def OnCalSelChangedb(self, event):
        cal = event.GetEventObject()
        datestr = cal.GetValue()
        self.start = dateutil.parser.parse(str(datestr)).strftime('%Y-%m-%d')
        self.log(f"""起始时间更改为{self.start}""")

    def OnCalSelChangede(self, event):
        cal = event.GetEventObject()
        datestr = cal.GetValue()
        self.end = dateutil.parser.parse(str(datestr)).strftime('%Y-%m-%d')
        self.log(f"""结束时间更改为{self.end}""")

    def cancleEvent(self, event):
        self.Destroy()


class MyApp(wx.App):
    pass
if __name__ == '__main__':
    app = MyApp()
    frame = MainFrame(None,title='生意参谋数据下载')
    frame.Show(True)
    app.MainLoop()




