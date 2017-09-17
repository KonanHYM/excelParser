# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import math
from config import BEINGMATE

ProfitList = [
    u'营业总收入',
    u'营业收入',
    u'营业成本',
    u'营业税金及附加',
    u'销售费用',
    u'管理费用',
    u'财务费用',
    u'资产减值损失',
    u'投资净收益',
    u'营业利润',
    u'加：营业外收入',
    u'减：营业外支出',
    u'利润总额',
    u'减：所得税',
    u'减：少数股东损益',
    u'归属于母公司所有者的净利润',
]

CashFlowList = [
    u'销售商品、提供劳务收到的现金',
    u'经营活动产生的现金流量净额',
]

BalanceSheetList = [
    u'应收票据',
    u'应收账款',
    u'预收款项',
]

def getType(final_types):
    if 'Q' in str(final_types):
        return u'季报'
    elif 'H' in str(final_types):
        return u'中报'
    elif 'E' in str(final_types):
        return u'中报'
    else:
        return u'年报'

def getSeason(final_types):
    if 'Q' in str(final_types):
        season = final_types.split('Q')[1]
        if season == '1':
            return u'第一季度'
        if season == '2':
            return u'第二季度'
        if season == '3':
            return u'第三季度'
        if season == '4':
            return u'第四季度'
        else:
            return
    else:
        return

#处理最终数据报表
def finalParser():
    final = pd.read_excel(BEINGMATE['Final'])
    mainBusiness = pd.read_excel(BEINGMATE['Main_Business'])#读取主营业务表
    profit = pd.read_excel(BEINGMATE['Profit'])#读取利润表
    profitSeason = pd.read_excel(BEINGMATE['Profit_Season'])#读取利润表(单季)
    balanceSheet = pd.read_excel(BEINGMATE['Balance_Sheet'])#读取资产负债表

    cashFlow = pd.read_excel(BEINGMATE['Cash_Flow'])#读取现金流量表
    cashFlowSeason = pd.read_excel(BEINGMATE['Cash_Flow_Season'])#读取现金流量表（单季）
    for final_types in final.columns:
        year = '20' + str(final_types)[0:2]
        reptype = getType(final_types = final_types)
        season = getSeason(final_types = final_types)
        #处理主营业务
        data = detailParser(mainBusiness, year, reptype)
        if not data is None:
            #营业收入&营业总收入
            final[final_types][1] = data[u'营业总收入' : u'营业成本'][0]
            final[final_types][3] = data[u'营业总收入' : u'营业成本'][0]
            final[final_types][4] = data[u'营业总收入' : u'营业成本'][1]
            final[final_types][5] = data[u'营业总收入' : u'营业成本'][2]
            final[final_types][6] = data[u'营业总收入' : u'营业成本'][3]
            final[final_types][7] = data[u'营业总收入' : u'营业成本'][4]
            #营业成本
            final[final_types][64] = data[u'营业成本' : u'毛利'][0]
            final[final_types][65] = data[u'营业成本' : u'毛利'][2]
            final[final_types][66] = data[u'营业成本' : u'毛利'][3]
            final[final_types][67] = data[u'营业成本' : u'毛利'][4]
            #毛利
            final[final_types][52] = data[u'毛利' : u'毛利率(%)'][0]
            final[final_types][53] = data[u'毛利' : u'毛利率(%)'][2]
            final[final_types][54] = data[u'毛利' : u'毛利率(%)'][3]
            final[final_types][55] = data[u'毛利' : u'毛利率(%)'][4]
            #毛利率
            final[final_types][48] = data[u'毛利率(%)' : u'显示币种'][0]
            final[final_types][49] = data[u'毛利率(%)' : u'显示币种'][2]
            final[final_types][50] = data[u'毛利率(%)' : u'显示币种'][3]
            final[final_types][51] = data[u'毛利率(%)' : u'显示币种'][4]
        #处理利润表
        data = detailParser(profit, year, reptype)
        if not data is None:
            for data_index in data.index:
                if not isinstance(data_index, float):
                    data_strip = data_index.strip()
                    if data_strip in ProfitList:
                        final[final_types][data_strip] = data[data_index]
        #处理利润表（单季）
        data = seasonParser(profitSeason, year, season)
        if not data is None:
            for data_index in data.index:
                if not isinstance(data_index, float):
                    data_strip = data_index.strip()
                    if data_strip in ProfitList:
                        final[final_types][data_strip] = data[data_index]

        #处理资产负债表
        data = detailParser(balanceSheet, year, reptype)
        if not data is None:
            for data_index in data.index:
                if not isinstance(data_index, float):
                    data_strip = data_index.strip()
                    if data_strip in BalanceSheetList:
                        final[final_types][data_strip] = data[data_index]

        #处理现金流量表
        data = detailParser(cashFlow, year, reptype)
        if not data is None:
            for data_index in data.index:
                if not isinstance(data_index, float):
                    data_strip = data_index.strip()
                    if data_strip in CashFlowList:
                        final[final_types][data_strip] = data[data_index]
        #处理现金流量表（单季）
        data = seasonParser(cashFlowSeason, year, season)
        if not data is None:
            for data_index in data.index:
                if not isinstance(data_index, float):
                    data_strip = data_index.strip()
                    if data_strip in CashFlowList:
                        final[final_types][data_strip] = data[data_index]
    # print final
    #生成最终版EXCEL文件
    writer = pd.ExcelWriter('../files/output/2.xlsx')
    final.to_excel(writer,'Sheet1')
    writer.save()

#输入一个DataFrame 返回对应到Final具体哪一列
def detailParser(dataF, year, reptype):
    for item in dataF.columns:
        if year in str(item):
            if reptype == dataF[item][u'报告期']:
                return dataF[item]

#输入一个DataFrame 到单季表 返回对应到Final具体哪一列
def seasonParser(dataF, year, season):
    for item in dataF.columns:
        if year in str(item):
            if season == dataF[item][u'报告期']:
                return dataF[item]

if __name__ == '__main__':
    finalParser()
