from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import tkinter.ttk as ttk
import csv

import pandas as pd
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt

import linear

import warnings
warnings.filterwarnings('ignore')


class BenmarkPredict:
	fileTest = None
	fileTrain = None

	res = ""

	def __init__(self):
		self.ui()

	def ui(self):
		self.window = Tk()
		self.window.title("Benmark Predict App")
		self.window.geometry('1080x720')

		Label(self.window, text="Nhập file training:", font=(18), ).place(x = 20, y = 50)
		self.pathTrain = Entry(self.window, width=50,)
		self.pathTrain.place(x = 250, y = 55)

		Label(self.window, text="Nhập file test:", font=(18), ).place(x = 20, y = 100)
		self.pathTest = Entry(self.window, width=50,)
		self.pathTest.place(x = 250, y = 105)

		self.lblResult = Label(self.window, text="", font=(18), anchor='w', width=1080)
		self.lblResult.pack(fill='both')
		self.lblResult.place(x = 0, y = 300)

		self.btnTrain = Button(self.window, text="Select file", command=self.selectFileTrain).place(x = 600, y = 50)
		self.btnTest = Button(self.window, text="Select file", command=self.selectFileTest).place(x = 600, y = 100)

		self.btnRun = Button(self.window, text="RUN", command=self.runPredict).place(x = 300, y = 150)

		self.window.mainloop()


	def selectFileTrain(self):
		self.fileTrain = filedialog.askopenfilename(filetypes = (("Text files","*.csv"),("All files","*.*")))
		self.pathTrain.delete(0, END)
		self.pathTrain.insert(0, self.fileTrain)

	def selectFileTest(self):
		self.fileTest = filedialog.askopenfilename(filetypes = (("Text files","*.csv"),("All files","*.*")))
		self.pathTest.delete(0, END)
		self.pathTest.insert(0, self.fileTest)

	def runPredict(self):
		if self.fileTrain != None and self.fileTest != None:
			self.res = ""
			self.runMyLib(['dtb ca nuoc', 'tong dang ky', 'ti le trung tuyen'])
			self.run(['dtb ca nuoc', 'tong dang ky', 'ti le trung tuyen'])
			# self.lblMyResult.configure(text = self.res)

		else:
			showinfo(title="Thông báo", message="Vui lòng nhập đầy đủ data train và data test")

	def runMyLib(self, tohop):
		dataTrain = pd.read_csv(self.fileTrain)
		dataTest = pd.read_csv(self.fileTest)

		dfTrain = pd.DataFrame(dataTrain)
		dfTest = pd.DataFrame(dataTest)

		x = []
		y = []

		for i in range(len(tohop)):
			xx = []
			for j in range(len(dfTrain.index)):
				xx.append(dfTrain.iloc[j][tohop[i]])
			x.append(xx)

		x.append([1.0] * len(dfTrain.index))

		for i in range(len(dfTrain.index)):
			df = dfTrain.iloc[i]
			y.append(df["diem chuan"])

		x_test = []
		for i in range(len(tohop)):
			x_test.append(dfTest.iloc[0][tohop[i]])
		x_test.append(1.0)

		print('\n', x)
		print('\n', y)
		print('\n')

		myLinear = linear.MyLinearRegression()
		myLinear.fit(x, y)

		self.res += 'Tự cài đặt thuật toán\n'
		self.res += 'Điểm dự đoán: ' + str(myLinear.predict(x_test)) + "\n"
		self.res += 'Hệ số: ' + str(myLinear.coef_) + '\n\n'
		# print('a: ', myLinear.coef_)
		# print('b: ', myLinear.predict(x_test))

		# self.lblMyResult.configure(text = res)


	def run(self, tohop):
		dataTrain = pd.read_csv(self.fileTrain)
		dataTest = pd.read_csv(self.fileTest)

		# Chuyển dữ liệu từ file csv vào data frame
		dfTrain = pd.DataFrame(dataTrain)
		dfTest = pd.DataFrame(dataTest)

		x_test = dfTest[tohop]

		x_train = dfTrain[tohop]
		y_train = dfTrain[['diem chuan']]


		model = linear_model.LinearRegression()
		model.fit(x_train, y_train)

		# R^2
		r_sq = model.score(x_train, y_train)


		# Dự đoán điểm chuẩn cho năm 2022
		dc_predict = model.predict(x_test)


		dc2022 = dc_predict[0][0]

		print('Điểm dự đoán: ', dc2022)
		print('Hệ số: ', str(model.coef_[0]), ' ', str(model.intercept_))

		self.res += "Sử dụng thư viện SKLearn\n"
		# self.res += "Điểm dự đoán: " + "{:.2f}".format(dc2022) + "\n"
		self.res += "Điểm dự đoán: " + str(dc2022) + "\n"
		self.res += "Hệ số: " + str(model.coef_[0]) +' ' + str(model.intercept_) + "\n"

		self.lblResult.configure(text = self.res)

		diem_chuan = y_train.to_numpy()
		diem_du_doan = np.array([])

		for i in range(len(dfTrain.index)):
			df = dfTrain.iloc[i]
			xx = df[tohop]
			bmp = model.predict([xx])
			print(bmp)
			diem_du_doan = np.append(diem_du_doan, [bmp])

			# res += "Train " + str(int(df[['nam']])) + ": " + str("{:.2f}".format(bmp[0][0])) + "\n"


		nam = np.array([2017, 2018, 2019, 2020, 2021])

		plt.plot(nam, diem_chuan, 'bo-', label='Điểm chuẩn')
		plt.plot(nam, diem_du_doan, 'ro-', label='Dự đoán', linestyle='dashed')

		plt.legend(loc='best')
		plt.show()


bmp = BenmarkPredict()