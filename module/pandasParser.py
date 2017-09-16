# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import math

from config import BEINGMATE
Main_Business = {
    '营业总收入-百万元':'营业总收入',
    '产品':'',
    '奶粉类':'',
    '其他主营业务':'',
    '其他业务':'',

    '毛利率':'毛利率',
    '产品':'',
    '奶粉类':'',
    '其他主营业务':'',
    '其他业务':'',

    '毛利-百万元':'毛利',
    '产品':'',
    '奶粉类':'',
    '其他主营业务':'',
    '其他业务':'',

    '营业成本-百万元':'营业成本',
    '产品':'',
    '奶粉类':'',
    '其他主营业务':'',
    '其他业务':'',
}

Profit = {
    '营业总收入':,
    '营业收入':'',
    '营业成本':'',
    '营业税金及附加':'',
    '销售费用':'',
    '管理费用':'',
    '财务费用':'',
    '资产减值损失':'',
    '投资净收益':'',
    '营业利润':'',
    '营业外收支':'',
    '利润总额':'',
    '减：所得税':'',
    '减：少数股东损益':'',
    '归属于母公司所有者的净利润':'',
}

def getType(final_types):
    if 'Q' in str(final_types):
        return u'季报'
    elif 'H' in str(final_types):
        return u'中报'
    elif 'E' in str(final_types):
        return u'中报'
    else:
        return u'年报'

#处理最终数据报表
def finalParser():
    final = pd.read_excel(BEINGMATE['Final'])
    financialSummarySeason = pd.read_excel(BEINGMATE['Financial_Summary_Season'])#读取财务摘要单季表
    mainBusiness = pd.read_excel(BEINGMATE['Main_Business'])#读取主营业务表

    for final_types in final.columns:
        year = '20' + str(final_types)[0:2]
        reptype = getType(final_types = final_types)

        #处理主营业务
        data = detailParser(mainBusiness, year, reptype)
        dataParser(final, data, dictFile)
        # for item in mainBusiness.columns:
        #     print item.split('-')[0]
        #     print mainBusiness.ix[u'营业总收入']
        #     # print financialSummarySeason[u'2017-06-30'][u'报告类型']

#输入一个DataFrame 返回对应到Final具体哪一列
def detailParser(dataF, year, reptype):
    for item in dataF.columns:
        if year in str(item):
            if reptype == dataF[item][u'报告期']:
                return dataF[item]

def dataParser(final, data, dictFile):
    pass

if __name__ == '__main__':
    finalParser()
