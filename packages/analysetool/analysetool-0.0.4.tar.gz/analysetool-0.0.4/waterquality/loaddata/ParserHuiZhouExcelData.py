import numpy as np
import pandas as pd
import xlrd

#备注#
#该类主要，将原始excel数据处理成为每个站点一个csv文件

class ParserHuiZhouExcelData():

    # inputFilePath 输入文件路径
    # outputDir  输出文件目录
    def __init__(self,inputFilePath = "",outputDir=""):
        self.inputFilePath = inputFilePath
        self.outputDir = outputDir

    def run(self):

        allData = self.getAllData()
        site_items = allData[0]
        print(site_items)
        # 站点指标
        #['站点名称', 'MN', '监测时间', '水温 (℃)', 'pH值(无量纲)', '溶解氧 (mg/L)', '电导率 (uS/cm)', '浊度(NTU)', '高锰酸盐指数 (mg/L)', '氨氮(mg/L)', '总磷(mg/L)', '总氮(mg/L)', '铜(mg/L)', '六价铬 (mg/L)', '铅(mg/L)', '氰化物 (mg/L)', '温度(℃)', '湿度(%)', '镍(mg/L)', '总酚(ug/L)']

        # site_items=["site_name","mn","date","TEMP","PH","DO","DDL","NTU","CODMN","NH3","TP","TN","COPPER","Ge","PB","qhw","wd","sd","Ni","ZF"]
        site_items=["site_name","mn","date","水温","PH","溶解氧","电导率","浊度","高锰酸盐指数","氨氮","总磷","总氮","铜","六价铬","铅","氰化物","温度","湿度","镍","总酚"]

        siteNames,site_datas = self.getSiteData(allData)
        for i in range(0, len(siteNames)):
            filePath = self.outputDir + "/" + siteNames[i] + ".csv"
            df = pd.DataFrame(site_datas[i], columns=site_items)
            df.to_csv(filePath)

    def getAllData(self):
        wb = xlrd.open_workbook_xls(self.inputFilePath)
        all_sheet_names = wb.sheet_names()

        all_data = []  # 组装所有数据
        for i in range(len(all_sheet_names)):
            data_sheet = wb.sheet_by_index(i)
            nrows = data_sheet.nrows

            if nrows > 3:
                if i == 0:
                    all_data.append(data_sheet.row_values(1))

                for j in range(3, nrows):
                    all_data.append(data_sheet.row_values(j))
        return all_data

    def getSiteData(self,all_data):
        site_datas = []
        tmp_data = []
        siteNames = []

        for i in range(1, len(all_data)):
            name = all_data[i][0]
            if siteNames.count(name) == 0:

                if len(tmp_data) > 0:
                    site_datas.append(tmp_data)
                    tmp_data = []

                siteNames.append(name)

            if i == (len(all_data) - 1) and len(tmp_data) > 0:
                site_datas.append(tmp_data)
                tmp_data = []

            tmp_data.append(all_data[i])

        return siteNames,site_datas




