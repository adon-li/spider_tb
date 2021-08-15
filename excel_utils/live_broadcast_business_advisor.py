
import logging
import os

from datetime import datetime

import dateutil.parser
import pandas as pd


import requests

import time

import random

import datetime
import dateutil
from db_setting import DATA_SOURCE
from excel_utils.to_db import SycmData
from settings import DOWNLOAD_DIR
logger = logging.getLogger("SycmFlow")
# 显示所有列
pd.set_option('display.max_columns', 500)
# 显示所有行
pd.set_option('display.max_rows', 500)

pd.set_option('display.width', 1000)


def log(text):
    print(text)


class LiveBroadcast(object):
    def __init__(self, cookies,log):
        self.check_login(cookies)
        self.cookies = cookies
        self.sycm = SycmData(DATA_SOURCE['vertica'], log)
        self.logs = log

    def check_login(self, cookies):
        header = {'%authority': 'sycm.taobao.com',
                  '%path': '/custom/login.htm?_target=http://sycm.taobao.com/portal/home.htm',
                  '%scheme': 'https',
                  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                  'referer': 'https://sycm.taobao.com/',
                  'cookie': cookies
                  }
        url = 'https://sycm.taobao.com/custom/menu/getPersonalView.json'
        try:
            response = requests.get(url, headers=header)
            result = response.json()
            if result["code"] == 0:
                self.shop_name = result["data"]["runAsShopTitle"]
                self.shop_id = result["data"]["runAsShopId"]
                logger.info('账户登陆成功！')
                # self.logs('账户登陆成功！')
        except Exception as e:
            logger.error(f'{e}：登录失败，输入的cookie与该账号不匹配，请重新输入！')
            # self.logs(f'{e}：登录失败，输入的cookie与该账号不匹配，请重新输入！')
            os._exit(0)
        time.sleep(random.randint(5, 15))

    def live_order_detail_download(self, start, end, astrict=0):
        """
        :param start:
        :param end:
        :param astrict:
        :return:
        """
        """
        accountId: "2719809625"
        accountName: "茵曼KIDS"主播名称
        buyerNickMark: "贯*4"会员名
        cateLevel1Id: "50008165"
        cateLevel1Name: "童装/婴儿装/亲子装"商品一级类目
        confirmPaidAmt: "-"
        confirmPaidTime: "-"
        contentId: "314814374449"场次ID
        contentTitle: "单件福利65折速来抢"直播标题
        createTime: "2021-06-16 23:44:19"下单时间
        daiboId: "-"
        daiboName: "茵曼KIDS"主播名称
        divPayAmt: "89.99"支付金额
        fansType: "铁粉"直播间粉丝层级
        itemId: "640922028613"商品ID
        itemTitle: "茵曼童装海军风条纹t恤中大女童短袖针织polo上衣学生2021夏新款"商品标题
        liveStartTime: "2021-06-16 20:12:45"直播时间
        mordId: "1878589441827958111"父订单
        orderId: "1878589441827958111"子订单
        payTime: "2021-06-16 23:44:26"支付时间
        """
        header = {
            '%authority': 'gm.mmstat.com',
            '%method': 'GET',
            'accept-encoding': 'gzip, deflate, br',
            'referer': 'https://sycm.taobao.com/s_live/my_live.htm',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'cookie': self.cookies
        }
        start_time = dateutil.parser.parse(start)
        time_array = time.strptime(end, "%Y-%m-%d")
        end_time = time.strftime("%Y-%m-%d 23:59:59", time_array)
        # end_time = dateutil.parser.parse(end)
        params = {'dataApi': 'dataQRForm',
                  'paramJsonStr': '{"dataQRFormId":"live_overview_order",'
                                  '"orderDateType":"3",'
                                  f'"beginTime":"{start_time}",'
                                  f'"endTime":"{end_time}",'
                                  '"start":"0",'
                                  '"hit":"5000",'
                                  '"itemId":null,'
                                  '"itemTitle":null,'
                                  '"orderColumn":"pay_time",'
                                  '"orderType":"1"}'}
        # data = urllib.parse.urlencode(params)
        # print(data)
        try:
            r = requests.get('https://sycm.taobao.com/s_live/liveGeneralQuery.json', params=params, headers=header)
            data = r.json()['data']['model']
            df = pd.DataFrame(data)
            df.replace('-', '', inplace=True)
            file_name = f'直播订单明细_{start}_{end}_{datetime.datetime.now().strftime("%Y%m%d")}_{int(time.time() * 1000)}.xlsx'
            file_path = f'{DOWNLOAD_DIR}/{file_name}'
            df.to_excel(
                file_path,
                encoding='utf-8', index=False)
            logger.info(
                f'{file_name}：下载成功')
            self.logs(f'{file_name}：下载成功')
        except Exception as e:
            print(e)
            logger.error(e)
            time.sleep(random.randint(30, 60))
            if astrict < 3:
                return self.download(start, end, astrict=astrict + 1)
            else:
                logger.error('该文件尝试下载已超上限三次，请重试')
        self.sycm.live_order_detail_file_db(f'{file_path}',datetime.datetime.now().strftime("%Y-%m-%d"),self.shop_id,self.shop_name)
        time.sleep(random.randint(5, 15))

    def live_play_back_download(self, start, end, astrict=0):
        """
        :param start:
        :param end:
        :param astrict:
        :return:
        """
        """
        atnUv: "22"新增粉丝数
        atnUvRate: "0.012485811577752554"转粉率
        cartItemQty: "111"商品加购件数
        cartUv: "55"商品加购人数
        contentId: "314814374449"场次ID
        contentTitle: "单件福利65折速来抢"直播标题
        ipv: "2662"商品点击次数
        ipvUv: "702"商品点击人数
        ipvUvRate: "0.28794093519278097"商品点击率
        itrtRate: "0.02912223133716161"互动率
        liveStartTime: "2021-06-16 20:12:45"直播时间
        payAmt: "3127.18"种草成交金额
        payBuyerCnt: "11"种草成交人数
        payBuyerCntRate: "0.01566951566951567"种草成交转化率
        payItemQty: "30"种草成交件数
        payOrderCnt: "27"种草成交笔数
        pv: "5747"直播间浏览次数
        uv: "2438"直播间访问人数
        """
        start_date_arr = time.strptime(start, "%Y-%m-%d")
        start_date = time.strftime("%Y%m%d", start_date_arr)
        end_date_arr = time.strptime(end, "%Y-%m-%d")
        end_date = time.strftime("%Y%m%d", end_date_arr)
        header = {
            '%authority': 'sycm.taobao.com',
            '%method': 'GET',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'cookie': self.cookies
        }
        # start_time = dateutil.parser.parse(start)
        # end_time = dateutil.parser.parse(end)
        params = {
            'dataApi': 'dataQRForm',
            'paramJsonStr': '{"dataQRFormId":"live_overview_nrt_content",'
                            '"selectFilter":"{\\"afterSelect\\":[\\"contentTitle\\",\\"contentId\\",\\"liveStartTime\\",\\"pv\\",\\"uv\\",'
                            '\\"itrtRate\\",\\"atnUv\\",\\"atnUvRate\\",\\"ipvUv\\",\\"ipv\\",\\"ipvUvRate\\",\\"cartUv\\",\\"cartItemQty\\",'
                            '\\"payBuyerCntRate\\",\\"payBuyerCnt\\",\\"payItemQty\\",\\"payOrderCnt\\",\\"payAmt\\"]}",'
                            f'"beginDate":"{start_date}",'
                            f'"endDate":"{end_date}",'
                            '"orderColumn":"live_start_time","orderType":"1","start":"0","hit":"5000"}'
        }
        # data = urllib.parse.urlencode(params)
        # print(data)
        try:
            r = requests.get('https://sycm.taobao.com/s_live/liveGeneralQuery.json', params=params, headers=header)
            data = r.json()['data']['model']
            df = pd.DataFrame(data)
            df.replace('-', '', inplace=True)
            file_name = f'直播含回放累计数据_{start}_{end}_{datetime.datetime.now().strftime("%Y%m%d")}_{int(time.time() * 1000)}.xlsx'
            file_path = f'{DOWNLOAD_DIR}/{file_name}'
            df.to_excel(file_path,
                        encoding='utf-8', index=False)
            logger.info(
                f'{file_name}：下载成功')
            self.logs(f'{file_name}：下载成功')
        except Exception as e:
            print(e)
            logger.error(e)
            time.sleep(random.randint(30, 60))
            if astrict < 3:
                return self.download(start, end, astrict=astrict + 1)
            else:
                logger.error('该文件尝试下载已超上限三次，请重试')
                self.logs('该文件尝试下载已超上限三次，请重试')
        self.sycm.live_play_back_file_db(f'{file_path}',datetime.datetime.now().strftime("%Y-%m-%d"),self.shop_id,self.shop_name)

        time.sleep(random.randint(5, 15))
    def live_goods_transaction_download(self, start, end, astrict=0):
        """

        :param start:
        :param end:
        :param astrict:
        :return:
        """
        """
        accountId: "2719809625"
        accountName: "茵曼KIDS"账号名称
        cartItemQty: "1"商品加购件数
        cartUv: "1"商品加购人数
        contentId: "314814374449"场次ID
        contentTitle: "单件福利65折速来抢"直播标题
        ds: "20210616"
        ipv: "7"商品点击次数
        ipvUv: "6"商品点击人数
        itemId: "641743201687"商品ID
        itemPictUrl: "http://gw.alicdn.com/tfscom/O1CN01x6LCEY2KyIovdN9TL_!!2719809625.jpg"商品主图
        itemTitle: "茵曼童装打底裤女童薄款外穿儿童七分裤子荷叶边裤脚2021夏季新款"商品标题
        liveStartTime: "2021-06-16 20:12:45"开播时间
        payAmt: "-"种草成交金额
        payBuyerCnt: "-"种草成交人数
        payItemQty: "-"种草成交件数
        payOrderCnt: "-"种草成交笔数
        sellerId: "2719809625"
        """
        start_date_arr = time.strptime(start, "%Y-%m-%d")
        start_date = time.strftime("%Y%m%d", start_date_arr)
        end_date_arr = time.strptime(end, "%Y-%m-%d")
        end_date = time.strftime("%Y%m%d", end_date_arr)
        header = {
            '%authority': 'sycm.taobao.com',
            '%method': 'GET',
            'accept': '*/*',
            '%scheme': 'https',
            'accept-encoding': 'gzip, deflate, br',
            'referer': 'https://sycm.taobao.com/s_live/my_live.htm',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'cookie': self.cookies
        }
        try:
            dict = {"my": "live_ia_my_item", "cooperation": "live_ia_co_item"}
            list = []
            for k, v in dict.items():
                params = {'dataApi': 'dataQRForm',
                          'paramJsonStr': '{'
                                          f'"dataQRFormId":"{v}",'
                                          f'"beginDate":"{start_date}",'
                                          f'"endDate":"{end_date}",'
                                          '"itemId":null,"itemTitle":null,"contentId":null,"orderType":"1","orderColumn":"live_start_time","start":"0","hit":"5000"}'}
                r = requests.get('https://sycm.taobao.com/s_live/liveGeneralQuery.json', params=params, headers=header)
                data = r.json()['data']['model']
                for i in data:
                    i.update(classify=k)
                    list.append(i)
            df = pd.DataFrame(list)
            df.replace('-', '', inplace=True)
            file_name = f'直播间商品成交_{start}_{end}_{datetime.datetime.now().strftime("%Y%m%d")}_{int(time.time() * 1000)}.xlsx'
            file_path = f'{DOWNLOAD_DIR}/{file_name}'
            df.to_excel(
                file_path,
                encoding='utf-8', index=False)
            # # print(df)
            logger.info(
                f'{file_name}：下载成功')
            self.logs(f'{file_name}：下载成功')
        except Exception as e:
            print(e)
            logger.error(e)
            time.sleep(random.randint(30, 60))
            if astrict < 3:
                return self.download(start, end, astrict=astrict + 1)
            else:
                logger.error('该文件尝试下载已超上限三次，请重试')
                self.logs('该文件尝试下载已超上限三次，请重试')
        self.sycm.live_goods_transaction_file_db(f'{file_path}',datetime.datetime.now().strftime("%Y-%m-%d"),self.shop_id,self.shop_name)
        time.sleep(random.randint(5, 15))

# if __name__ == '__main__':
    # a = LiveBroadcast(
    #     'arms_uid=a2888499-7dc8-4fc5-bcbb-c3697bc82895; _samesite_flag_=true; cookie2=195b428ab73351003bbf802e6429c3a3; t=84407dace6a9a87d1ae79e0a632b1871; _tb_token_=e58ee438e05eb; XSRF-TOKEN=29cd6a79-f915-4f7d-abf9-25fa804a24d9; enc=RUDQKb4UiYqXhBzGpFMh%2BNf5CPGoiN371nkfpii2diJFxe5rzPxf7WMfVmmhWJojEZtZYm5Oj7nGSUNkt5UxKDLsq8VJClEIVahJCkzfI%2F8%3D; xlly_s=1; uc1=cookie21=V32FPkk%2FhSg%2F&cookie14=Uoe2ySVMY7NGaA%3D%3D; unb=2211398382792; sn=%E8%8C%B5%E6%9B%BC%E7%AB%A5%E8%A3%85%E6%97%97%E8%88%B0%E5%BA%97%3Abi; csg=362ce0d4; skt=33fe4a60b1ddc118; _cc_=UIHiLt3xSw%3D%3D; _euacm_ac_l_uid_=2211398382792; 2211398382792_euacm_ac_c_uid_=2719809625; 2211398382792_euacm_ac_rs_uid_=2719809625; _euacm_ac_rs_sid_=null; tfstk=cVTFBdsNY23FMN_SDw_zNaqFSDjdZUWPHP5Vxhtcidnjw9IhiK2RsghV__WxSMf..; isg=BGNjVAviB4XEzcvHRwQ1NkVQ8qcNWPea2ZK1SJXAjEI51IL2Hygt6s1FzqRa9E-S; l=eBxzCz-Ij3sZzpP_BOfZlurza779vIRfguPzaNbMiOCPOyCH5XeCW6OnbJLMCnGVnsgX-3WWjis_B8TLbyUIQxv9-e_7XPQoAdLh.; JSESSIONID=C28D03CE8FE17EA0FAD45EFA6AC7AE09; v=0',log)
    # # a.live_order_detail_download('2021-05-15', '2021-06-01')
    # a.live_order_detail_download('2021-05-17', '2021-05-31') # 前闭后开
    # a.live_play_back_download('2021-05-17', '2021-05-31')  # 前闭后闭
    # a.live_goods_transaction_download('2021-05-17', '2021-05-31')  # 前闭后闭
