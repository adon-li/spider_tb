from datetime import datetime
from numpy import int64

from settings import *
import numpy as np
from data_source.engines import get_engine
from db_setting import DATA_SOURCE
import pandas as pd
from data_source.sessions import sessions, sessions_scopes
import warnings

logger = logging.getLogger('SycmFlow')
Scope = sessions_scopes(sessions)
warnings.filterwarnings("ignore")


# pd.set_option('display.max_columns', 500)
# # 显示所有行
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.width', 1000)
# def log(text):
#     print(text)
class SycmData(object):
    def __init__(self, data_source, log):
        self._conn = get_engine(data_source)
        self.log = log

    def live_order_detail_file_db(self, filepath, spider_time, shop_id, shop_name):
        columns = {'columns_type': ['daibo_id', 'shop_id'],
                   'columns_name': {'accountId': "anchor_id",
                                    'accountName': "anchor_name",
                                    'buyerNickMark': "member_name",
                                    'cateLevel1Id': "category1_id",
                                    'cateLevel1Name': "category1_name",
                                    'confirmPaidAmt': "confirm_paid_amount",
                                    'confirmPaidTime': "confirm_paid_time",
                                    'contentId': "content_id",
                                    'contentTitle': "content_title",
                                    'createTime': "order_time",
                                    'daiboId': "daibo_id",
                                    'daiboName': "daibo_name",
                                    'divPayAmt': "pay_amount",
                                    'fansType': "fans_grade",
                                    'itemId': "goods_id",
                                    'itemTitle': "goods_title",
                                    'liveStartTime': "live_start_time",
                                    'mordId': "parent_order",
                                    'orderId': "suborder",
                                    'payTime': "pay_time"
                                    }}
        try:
            df = pd.read_excel(filepath)
            df['shop_id'] = shop_id
            df['shop_name'] = shop_name
            df['spider_date'] = spider_time
            df.rename(columns=columns['columns_name'], inplace=True)
            # print(df.columns.values)
            df['confirm_paid_amount'].replace(np.nan, 0, inplace=True)
            df['daibo_id'].replace(np.nan, 0, inplace=True)
            df[columns['columns_type']] = df[columns['columns_type']].astype(int)
            if len(df) == 1:
                sql = f"""delete FROM hmcdata.spider_sycm_live_order_detail 
                                    where  cast(suborder as varchar) = '{df['suborder'][0]}'
                                        """
            else:
                sql = f"""delete FROM hmcdata.spider_sycm_live_order_detail 
                                    where suborder IN {tuple(df['suborder'].values)}
                                                    """
            self._conn.execute(sql)
            Scope['vertica'].remove()
            df.to_sql(name=f'spider_sycm_live_order_detail', con=self._conn,
                      if_exists="append",
                      chunksize=2000,
                      index=False, schema=DATA_SOURCE['vertica']['db'])
            logger.info('[{0}]: {1}数据入库成功'.format(datetime.now(), filepath.split('\\')[-1]))
            self.log('[{0}]: {1}数据入库成功'.format(datetime.now(), filepath.split('\\')[-1]))
        except Exception as e:
            logger.error(' {0},该文件执行出错：\n{1}'.format(filepath.split('\\')[-1], e))
            self.log('{0},该文件执行出错：\n{1}'.format(filepath.split('\\')[-1], e))

    def live_play_back_file_db(self, filepath, spider_time, shop_id, shop_name):
        columns = {'columns_type': ['plante_grass_deal_person_num', 'add_purchase_num', 'plante_grass_deal_piece_num',
                                    'plante_grass_deal_order_num', 'goods_click_person_num', 'goods_click_num',
                                    'add_purchase_person_num',
                                    'add_fans', 'shop_id'],
                   'columns_name': {'atnUv': "add_fans",
                                    'atnUvRate': "fans_convert_rate",
                                    'cartItemQty': "add_purchase_num",
                                    'cartUv': "add_purchase_person_num",
                                    'contentId': "content_id",
                                    'contentTitle': "content_title",
                                    'ipv': "goods_click_num",
                                    'ipvUv': "goods_click_person_num",
                                    'ipvUvRate': "goods_click_rate",
                                    'itrtRate': "interaction_rate",
                                    'liveStartTime': "live_start_time",
                                    'payAmt': "plante_grass_deal_amount",
                                    'payBuyerCnt': "plante_grass_deal_person_num",
                                    'payBuyerCntRate': "plante_grass_deal_convert_rate",
                                    'payItemQty': "plante_grass_deal_piece_num",
                                    'payOrderCnt': "plante_grass_deal_order_num",
                                    'pv': "live_browse_num",
                                    'uv': "live_visitor"
                                    }}
        try:
            df = pd.read_excel(filepath)
            df['shop_id'] = shop_id
            df['shop_name'] = shop_name
            df['spider_date'] = spider_time
            df.rename(columns=columns['columns_name'], inplace=True)
            df.replace(np.nan, 0, inplace=True)
            df[columns['columns_type']] = df[columns['columns_type']].astype(int64)
            if len(df) == 1:
                sql = f"""delete FROM hmcdata.spider_sycm_live_play_back 
                                        where cast(content_id as varchar) = '{df['content_id'][0]}'
                                        and live_start_time = '{df['live_start_time'][0]}'
                                        """
            else:
                sql = f"""delete FROM hmcdata.spider_sycm_live_play_back 
                                        where content_id IN {tuple(df['content_id'].values)}
                                        and live_start_time IN {tuple(df['live_start_time'].values)}"""
            self._conn.execute(sql)
            Scope['vertica'].remove()

            df.to_sql(name=f'spider_sycm_live_play_back', con=self._conn,
                      if_exists="append",
                      chunksize=2000,
                      index=False, schema=DATA_SOURCE['vertica']['db'])
            logger.info('[{0}]: {1}数据入库成功'.format(datetime.now(), filepath.split('\\')[-1]))
            self.log('[{0}]: {1}数据入库成功'.format(datetime.now(), filepath.split('\\')[-1]))
        except Exception as e:
            logger.error(' {0},该文件执行出错：\n{1}'.format(filepath.split('\\')[-1], e))
            self.log('{0},该文件执行出错：\n{1}'.format(filepath.split('\\')[-1], e))

    def live_goods_transaction_file_db(self, filepath, spider_time, shop_id, shop_name):
        columns = {'columns_type': ['plante_grass_deal_person_num', 'add_purchase_num',
                                    'plante_grass_deal_piece_num', 'plante_grass_deal_order_num',
                                    'goods_click_person_num', 'goods_click_num',
                                    'add_purchase_person_num', 'shop_id'],
                   'columns_name': {
                       'accountId': "anchor_id",
                       'accountName': "anchor_name",
                       'cartItemQty': "add_purchase_num",
                       'cartUv': "add_purchase_person_num",
                       'contentId': "content_id",
                       'contentTitle': "content_title",
                       'ds': "ds",
                       'ipv': "goods_click_num",
                       'ipvUv': "goods_click_person_num",
                       'itemId': "goods_id",
                       'itemPictUrl': "goods_picture",
                       'itemTitle': "goods_title",
                       'liveStartTime': "live_start_time",
                       'payAmt': "plante_grass_deal_amount",
                       'payBuyerCnt': "plante_grass_deal_person_num",
                       'payItemQty': "plante_grass_deal_piece_num",
                       'payOrderCnt': "plante_grass_deal_order_num",
                       'sellerId': "seller_id"
                   }}
        try:
            df = pd.read_excel(filepath)
            df['shop_id'] = shop_id
            df['shop_name'] = shop_name
            df['spider_date'] = spider_time
            df.rename(columns=columns['columns_name'], inplace=True)
            df.replace(np.nan, 0, inplace=True)
            df[columns['columns_type']] = df[columns['columns_type']].astype(int64)
            if len(df) == 1:
                sql = f"""delete FROM hmcdata.spider_sycm_live_goods_transaction 
                                        where cast(content_id as varchar) = '{df['content_id'][0]}'
                                        and cast(goods_id as varchar) = '{df['goods_id'][0]}'
                                        and ds = {df['ds'][0]}
                                        """
            else:
                sql = f"""delete FROM hmcdata.spider_sycm_live_goods_transaction 
                                        where content_id IN {tuple(df['content_id'].values)}
                                        and goods_id IN {tuple(df['goods_id'].values)}
                                        and ds IN {tuple(df['ds'].values)}
                                        """
            self._conn.execute(sql)
            Scope['vertica'].remove()

            df.to_sql(name=f'spider_sycm_live_goods_transaction', con=self._conn,
                      if_exists="append",
                      chunksize=2000,
                      index=False, schema=DATA_SOURCE['vertica']['db'])
            logger.info('[{0}]: {1}数据入库成功'.format(datetime.now(), filepath.split('\\')[-1]))
            self.log('[{0}]: {1}数据入库成功'.format(datetime.now(), filepath.split('\\')[-1]))
        except Exception as e:
            logger.error(' {0},该文件执行出错：\n{1}'.format(filepath.split('\\')[-1], e))
            self.log('{0},该文件执行出错：\n{1}'.format(filepath.split('\\')[-1], e))

# if __name__ == '__main__':
#     a = SycmData(DATA_SOURCE['vertica'],log)
#     a.live_order_detail_file_db(
#         'E:\spider_tb_sale_datas\excel_utils\直播订单明细_2021-05-14_2021-06-15_20210617_1623930091205.xlsx', '021-06-14',
#         '021-06-15', '021-06-17')
#     a.live_play_back_file_db(
#         'E:\spider_tb_sale_datas\excel_utils\直播含回放累计数据_2021-06-20_2021-06-20_20210621_1624246001626.xlsx', '2021-06-20',
#         '2021-06-20', datetime.datetime.now().strftime("%Y-%m-%d"))
#     a.live_goods_transaction_file_db(
#         'E:\spider_tb_sale_datas\excel_utils\直播间商品成交_2021-06-15_2021-06-15_20210618_1623981568272.xlsx', '021-06-14',
#         '021-06-15', '021-06-17')
