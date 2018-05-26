#!encode: utf-8

import numpy as np
import pymysql
import pandas
import datetime
from sklearn import linear_model
from InfoManage.models import PredictData, Product


class linear(object):
    def __init__(self):
        self.W = None
        self.b = None
        self.clf = None

    def train(self, X, y):
        try:
            self.clf = linear_model.LinearRegression()    
            self.clf.fit(X, y)
        except:
            pass

    def predict(self, X):
        y_pred = self.clf.predict(X)
        return y_pred

    def get_data(self):
        db = pymysql.connect("localhost", "root", "lmz1995", "erp")
        cursor = db.cursor()
        cursor.execute("select SaleForm.deliver_date, SaleFormProduct.pro_name_id, SaleFormProduct.num from "
                       "SaleFormProduct, SaleForm where SaleFormProduct.sf_name_id=SaleForm.id")

        raws = cursor.fetchall()
        x_data = []
        y_data = []
        for raw in raws:
            x_data.append([raw[1], int(raw[0].strftime("%Y%m%d")[-2:])])
            y_data.append(raw[2])
        x_data = pandas.DataFrame(x_data)
        y_data = pandas.DataFrame(y_data)
        db.close()
        return x_data, y_data

    def pre_data(self):
        today = datetime.date.today()
        time = []
        for i in range(1, 8):
            time.append(int((datetime.timedelta(days=i) +today).strftime("%Y%m%d")[-2:]))
        db = pymysql.connect("localhost", "root", "lmz1995", "erp")
        cursor = db.cursor()
        cursor.execute("select id from Product")
        raws = cursor.fetchall()
        pre = []
        for t in time:
            for raw in raws:
                pre.append([t, raw[0]])
        pre = pandas.DataFrame(pre)
        db.close()
        return pre

    def save_data(self,x,y):
        x = np.array(x).tolist()
        y = np.array(y).tolist()
        db = pymysql.connect("localhost", "root", "lmz1995", "erp")
        cursor = db.cursor()
        cursor.execute("TRUNCATE PredictData")
        db.close()
        for i in range(len(x)):
            date = x[i][0]
            time = datetime.date.today().strftime("%Y-%m-{}".format(date))
            time=datetime.datetime.strptime(time,'%Y-%m-%d')
            s = PredictData()
            s.date = time
            pro = Product.objects.get(id=x[i][1])
            s.pro_name = pro
            s.num = str(int(y[i][0]))
            s.save()

    def get_pre(self):
        datas = PredictData.objects.all()
        re = []
        for data in datas:
            pro = Product.objects.get(id = data.pro_name_id)
            re.append([data.date.strftime("%m/%d/%Y"), data.num, pro.pro_name])
        head = ['Day']
        pro_name = []
        for i in re:
            pro_name.append(i[2])
        pro_name = set(pro_name)
        head.extend(pro_name)
        # print(head)
        res = ''
        for i in head:
            res += i+','
        res = res[:-1]
        res += '\n'
        time = []
        for data in datas:
            time.append(data.date.strftime("%m/%d/%Y"))
        time = set(time)
        pre = []
        # today = datetime.date.today()
        # time = []
        # for i in range(1, 8):
        #     time.append((datetime.timedelta(days=i) + today).strftime("%m/%d/%Y"))
        # print(time.sort())
        # print(time)
        time = list(time)
        time.sort()
        for t in time:
            res += t+','
            for p in pro_name:
                for r in re:
                    if r[0] == t:
                        if r[2] == p:
                            res += str(r[1])+','
            res = res[:-1]
            res += '\n'
        return res






def main():
    l = linear()
    x,y = l.get_data()
    l.train(x, y)
    x_pre = l.pre_data()
    pre = l.predict(x_pre)
    l.save_data(x_pre,pre)
    return l.get_pre()



