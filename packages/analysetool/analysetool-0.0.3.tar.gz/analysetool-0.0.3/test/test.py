import matplotlib.pyplot as plt

realData = [ 9.4, 9.7, 10.3, 9.8, 9.8, 9.8, 8.9, 8.7, 9.7, 10.3, 11.2]
predictData = [9.4, 10.0, 9.99, 9.69, 9.89, 10.27, 9.52, 9.72, 9.56, 9.25, 9.62]

plt.plot(realData, label='True data')
plt.plot(predictData, label='Predicted data')

plt.legend()
plt.show()