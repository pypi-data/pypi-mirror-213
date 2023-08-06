import datetime

import keras
import numpy as np
import pandas as pd
from PyEMD import EEMD
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


from .base.EEMD_LSTM_BASE import EEMD_LSTM_BASE


class Predict_ZY(EEMD_LSTM_BASE):

    def __init__(self,aliasName="",lookback_window = 6):

        self.aliasName = aliasName
        self.lookback_window = lookback_window ;

    # 根据数据数据和 EEMD-LSTM 模型，对数据进行预测
    def predict_result(self,input_data=None,predictDay=1):
        predit_data=[]
        for i in range(0,predictDay):
            print("预测开始时间：{}，预测次数：{}".format(datetime.datetime.now(),str(i+1)))
            imfs, scaler = self.prepare_data(input_data)
            prediction = self.item_predict(imfs, scaler, input_data)
            predict_val = round(prediction, 2)
            input_data.append(predict_val)
            predit_data.append(predict_val)
            print("预测结束时间：{}，预测次数：{}".format(datetime.datetime.now(), str(i + 1)))
        return predit_data

    # 预测前准备数据
    def prepare_data(self,input_data):
        itemData = []
        for i in range(0, len(input_data)):
            itemData.append([input_data[i]])
        scaler_item = MinMaxScaler(feature_range=(0, 1))
        itemData = scaler_item.fit_transform(itemData)

        eemd = EEMD()
        eemd.noise_seed(12345)
        imfs = eemd.eemd(itemData.reshape(-1), None, 8)
        return imfs,scaler_item

    def item_predict(self,imfs, scaler_item,input_data):
        imfs_prediction = []
        i = 1
        c = int(len(input_data) * .85)
        print("len(imfs):" + str(len(imfs)))
        for imf in imfs:
            print('-' * 45)
            print('This is  ' + str(i) + '  time(s)')
            print('*' * 45)
            x2_test = imf[len(imf) - 6:len(imf) + 1].reshape(1, self.lookback_window, 1)
            if i < 9:
                model = load_model('h5/EEMD-LSTM-imf-'+ self.aliasName +'-' + str(i) + '-100.h5')
                prediction_Y = model.predict(x2_test)
                imfs_prediction.append(prediction_Y)
                keras.backend.clear_session()
                i += 1;

        imfs_prediction = np.array(imfs_prediction).reshape(-1)
        prediction = 0.0
        for i in range(len(imfs_prediction)):
            prediction += imfs_prediction[i]
        prediction = scaler_item.inverse_transform(np.array(prediction).reshape(1, -1)).reshape(-1)[0]
        return prediction

    def drawResultImg(self, all_data,predit_data,time_data):

        print("len(all_data)" + str(len(all_data)))
        print("len(all_predict_data)" + str(len(predit_data)))
        all_data = all_data[-100:]
        predit_data = predit_data[-100:]
        time_data = time_data[-100:]

        plt.plot(time_data,all_data, label='True data')
        plt.plot(time_data,predit_data, label='Predicted data')
        plt.show()


if __name__ == '__main__':
    filePath = "../../test/jlsmc/result/jlsmc_monitor_day_data.csv";
    predict = Predict_ZY(aliasName="DO")

    input_data=[]
    all_data=[]

    predictDay = 5

    dataset = pd.read_csv(filePath, header=0, index_col=0, parse_dates=True)
    dataset = dataset.sort_index(ascending=True)
    df = pd.DataFrame(dataset)

    all_data = df["溶解氧"].tolist()
    input_data = all_data[0:-predictDay]
    time_data = df.index.tolist()

    predit_data = predict.predict_result(input_data=input_data,predictDay=predictDay)

    predit_all_data = df["溶解氧"].tolist()
    predit_input_data = all_data[0:-predictDay]
    predit_input_data.extend(predit_data)

    predict.drawResultImg(all_data,predit_input_data,time_data)


    output_data = [all_data,predit_input_data]
    result_df = pd.DataFrame(output_data).T
    result_df.columns = ['原始数据', "预测数据"]
    result_df.index = time_data

    result_df.to_csv("../result/predict_result.csv")

    print(all_data)
    print(predit_all_data)
    print(predit_data)



