import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyEMD import EEMD
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler

from .base.EEMD_LSTM_BASE import EEMD_LSTM_BASE

# EEMD_LSTM模型
class EEMD_LSTM_ZY(EEMD_LSTM_BASE):

    def __init__(self,aliasName=""):
        self.aliasName = aliasName

        self.resultDir = ""

        self.scaler_item = MinMaxScaler(feature_range=(0, 1))

    #将原始数据日平均
    def day_average(self,filePath="",index_col="监测时间",saveFileName=""):
        df = pd.read_csv(filePath, header=0, index_col=index_col, parse_dates=True)
        df = df.groupby(df.index.to_period('d')).mean(numeric_only=True)
        if saveFileName !="":
            filePath = self.resultDir + "/" + saveFileName + "_all_day.csv"
            df.to_csv(filePath)
        return df

    # 将原始数据月平均
    def month_average(self,filePath="",index_col="监测时间",saveFileName=""):
        df = pd.read_csv(filePath, header=0, index_col=index_col, parse_dates=True)
        df = df.groupby(df.index.to_period('d')).mean()
        if saveFileName != "":
            filePath = self.resultDir + "/" + saveFileName + "_all_month.csv"
            df.to_csv(filePath)
        return df

    # 通过csv文件来生成模型......
    # nan_dispose drop 删除，fill 以上一行数据填充
    def generatorModelByCsv(self,filePath="",index_col="监测时间",itemName="",average_dim="day",nan_dispose="drop",resultDir="result", saveFileName=""):
        self.resultDir = resultDir
        # 对原始数据按照天进行平均然后参与后续模型模拟生成
        dataset = self.day_average(filePath,index_col=index_col,saveFileName=saveFileName)

        if average_dim == "month":
            dataset = self.month_average(filePath,index_col=index_col,saveFileName=saveFileName)

        dataset = dataset.loc[:,[itemName]]

        if nan_dispose == "drop":
            dataset = dataset.dropna()
        elif nan_dispose == "fill":
            dataset = dataset.fillna(axis=0,method='ffill')

        if saveFileName !="":
            dataset.to_csv(self.resultDir + "/" + saveFileName + "_"+itemName+"_month.csv")

        items = dataset[itemName]  # 返回溶解氧那一列，用字典的方式
        train_data = []
        for i in range(0, len(items)):
            train_data.append([items[i]])

        self.generatorModel(train_data)


    # 生成模型
    def generatorModel(self,train_data):
        # 数据归一化处理
        train_data = self.scaler_item.fit_transform(train_data)
        train_data = self.isolutionforest(train_data)

        # 通过eemd 对train_data 进行模态分解
        imfs = self.eemdData(train_data)

        #STML 建模
        imfs_prediction,test = self.LSTM(train_data,imfs)

        # 模型评估
        self.model_evaluate(imfs_prediction,test)

    #原始数据模态分解
    def eemdData(self,train_data,showEemdImg=True):
        eemd = EEMD()
        eemd.noise_seed(12345)
        imfs = eemd.eemd(train_data.reshape(-1), None, 8)
        print("len(imfs):" + str(len(imfs)))
        if showEemdImg:
            i = 1
            for imf in imfs:
                plt.subplot(len(imfs), 1, i)
                plt.plot(imf)
                i += 1

            plt.savefig(self.resultDir + '/result_imf_'+self.aliasName+'.png')
            plt.show()
        return imfs

    #LSTM建模
    def LSTM(self,train_data,imfs):
        c = int(len(train_data) * .85)
        lookback_window = 6
        imfs_prediction = []
        test = np.zeros([len(train_data) - c - lookback_window, 1])

        i = 1
        for imf in imfs:
            print('-' * 45)
            print('This is  ' + str(i) + '  time(s)')
            print('*' * 45)
            X1_train, Y1_train, X1_test, Y1_test = self.data_split(self.imf_data(imf, 1), c, lookback_window)
            X2_train, Y2_train, X2_test, Y2_test = self.data_split_LSTM(X1_train, Y1_train, X1_test, Y1_test)
            test += Y2_test
            model = self.LSTM_Model(X2_train, Y2_train, i)
            model.save(self.resultDir + '/h5/EEMD-LSTM-imf-'+ self.aliasName +"-"+ str(i) + '-100.h5')
            prediction_Y = model.predict(X2_test)
            imfs_prediction.append(prediction_Y)
            i += 1;

        return imfs_prediction,test

    # 模型评估
    def model_evaluate(self,imfs_prediction,test):
        imfs_prediction = np.array(imfs_prediction)
        prediction = [0.0 for i in range(len(test))]
        prediction = np.array(prediction)
        for i in range(len(test)):
            t = 0.0
            for imf_prediction in imfs_prediction:
                t += imf_prediction[i][0]
            prediction[i] = t

        prediction = prediction.reshape(prediction.shape[0], 1)

        test = self.scaler_item.inverse_transform(test)
        prediction = self.scaler_item.inverse_transform(prediction)

        self.plot_curve(test, prediction)

        rmse = format(self.RMSE(test, prediction), '.4f')
        mape = format(self.MAPE(test, prediction), '.4f')
        r2 = format(r2_score(test, prediction), '.4f')
        mae = format(mean_absolute_error(test, prediction), '.4f')
        print('RMSE:' + str(rmse) + '\n' + 'MAE:' + str(mae) + '\n' + 'MAPE:' + str(mape) + '\n' + 'R2:' + str(r2))

    def visualize(self,history):
        plt.rcParams['figure.figsize'] = (10.0, 6.0)
        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()

    def LSTM_Model(self,X_train, Y_train, i):

        model = Sequential()
        model.add(LSTM(50, activation='tanh', input_shape=(X_train.shape[1], X_train.shape[2])))  # 已经确定10步长
        '''
        ,return_sequences = True
        如果设置return_sequences = True，该LSTM层会返回每一个time step的h，
        那么该层返回的就是1个由多个h组成的2维数组了，如果下一层不是可以接收2维数组
        的层，就会报错。所以一般LSTM层后面接LSTM层的话，设置return_sequences = True，
        如果接全连接层的话，设置return_sequences = False。
        '''
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam')
        model.fit(X_train, Y_train, epochs=100, batch_size=16, validation_split=0.1, verbose=2, shuffle=True)
        return (model)

    def plot_curve(self,true_data, predicted):
        # rmse=format(RMSE(test,prediction),'.4f')
        # mape=format(MAPE(test,prediction),'.4f')
        plt.plot(true_data, label='True data')
        plt.plot(predicted, label='Predicted data')
        print(type(true_data))
        print(type(predicted))
        print(true_data)
        print(predicted)

        true_data_r = true_data.reshape(-1)
        predicted_r = predicted.reshape(-1)

        # 将模型验证数据进行保存
        output_data = [true_data_r, predicted_r]
        result_df = pd.DataFrame(output_data).T
        result_df.columns = ['原始数据', "验证数据"]
        result_df.to_csv("veriry_result.csv")

        plt.legend()
        plt.text(1, 1, 'RMSE:' + str(format(self.RMSE(true_data, predicted), '.4f')) + ' \n ' + 'MAPE:' + str(
            format(self.MAPE(true_data, predicted), '.4f')), color="r", style='italic', wrap=True)
        plt.savefig(self.resultDir + '/result_EEMD_LSTM_'+self.aliasName+'.png')
        plt.show()




