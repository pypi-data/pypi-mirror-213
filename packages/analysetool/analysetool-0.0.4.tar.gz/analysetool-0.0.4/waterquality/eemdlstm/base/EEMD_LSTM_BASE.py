from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_squared_error


class EEMD_LSTM_BASE():

    def data_split(self,data, train_len, lookback_window):
        train = data[:train_len]  # 标志训练集
        test = data[train_len:]  # 标志测试集

        # X1[]代表移动窗口中的10个数
        # Y1[]代表相应的移动窗口需要预测的数
        # X2, Y2 同理

        X1, Y1 = [], []
        for i in range(lookback_window, len(train)):
            X1.append(train[i - lookback_window:i])
            Y1.append(train[i])
            Y_train = np.array(Y1)
            X_train = np.array(X1)

        X2, Y2 = [], []
        for i in range(lookback_window, len(test)):
            X2.append(test[i - lookback_window:i])
            Y2.append(test[i])
            y_test = np.array(Y2)
            X_test = np.array(X2)

        return (X_train, Y_train, X_test, y_test)

    def data_split_LSTM(self,X_train, Y_train, X_test, y_test):  # data split f
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
        Y_train = Y_train.reshape(Y_train.shape[0], 1)
        y_test = y_test.reshape(y_test.shape[0], 1)
        return (X_train, Y_train, X_test, y_test)

    def imf_data(self,data, lookback_window):
        X1 = []
        for i in range(lookback_window, len(data)):
            X1.append(data[i - lookback_window:i])
        X1.append(data[len(data) - 1:len(data)])
        X_train = np.array(X1)
        return X_train

    def isolutionforest(self,itemData,showImg=False):

        rng = np.random.RandomState(42)
        clf = IsolationForest(random_state=rng, contamination=0.025)  # contamination为异常样本比例
        clf.fit(itemData)

        itemData_copy = itemData
        m = 0

        pre = clf.predict(itemData)
        for i in range(len(pre)):
            if pre[i] == -1:
                itemData_copy = np.delete(itemData_copy, i - m, 0)
                plt.scatter(i, itemData[i], c='red')
                print(i)
                m += 1
        if showImg :
            plt.plot(itemData)
            plt.show()
        return itemData_copy

    def RMSE(self,test, predicted):
        rmse = sqrt(mean_squared_error(test, predicted))
        return rmse

    def MAPE(self,Y_true, Y_pred):
        Y_true, Y_pred = np.array(Y_true), np.array(Y_pred)
        return np.mean(np.fabs((Y_true - Y_pred) / Y_true)) * 100