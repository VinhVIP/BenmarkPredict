from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import tkinter.ttk as ttk
import csv

import pandas as pd
from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


window = Tk()
window.title("Benmark Predict App")
window.geometry('1080x720')


Label(window, text="Nhập file training:", font=(18), ).place(x = 20, y = 50)
pathTrain = Entry(window, width=50,)
pathTrain.place(x = 250, y = 55)

Label(window, text="Nhập file test:", font=(18), ).place(x = 20, y = 100)
pathTest = Entry(window, width=50,)
pathTest.place(x = 250, y = 105)

lblKq = Label(window, text="", font=(18), anchor='w')
lblKq.pack(fill='both')
lblKq.place(x = 20, y = 300)


# TableMargin = Frame(window, width=800, height=100)
# TableMargin.place(x = 100, y = 400)


fileTrain = None 
fileTest = None

def selectFileTraining():
	global fileTrain

	fileTrain = filedialog.askopenfilename(filetypes = (("Text files","*.csv"),("All files","*.*")))
	print(fileTest)
	pathTrain.delete(0, END)
	pathTrain.insert(0, fileTrain)


def selectFileTesting():
	global fileTest 

	fileTest = filedialog.askopenfilename(filetypes = (("Text files","*.csv"),("All files","*.*")))
	print(fileTest)
	pathTest.delete(0, END)
	pathTest.insert(0, fileTest)

def runPredict():
	global fileTrain
	global fileTest 

	if fileTrain != None and fileTest != None:
		run(fileTrain, fileTest, ['ti le trung tuyen', 'dtb ca nuoc', 'tong dang ky'])
	else:
		showinfo(title="Thông báo", message="Vui lòng nhập đầy đủ data train và data test")


btnTrain = Button(window, text="Select file", command=selectFileTraining).place(x = 600, y = 50)
btnTest = Button(window, text="Select file", command=selectFileTesting).place(x = 600, y = 100)

btnRun = Button(window, text="RUN", command=runPredict).place(x = 300, y = 150)


def run(fileTrain, fileTest, tohop):
	dataTrain = pd.read_csv(fileTrain)
	dataTest = pd.read_csv(fileTest)


	# Chuyển dữ liệu từ file csv vào data frame
	dfTrain = pd.DataFrame(dataTrain)
	dfTest = pd.DataFrame(dataTest)


	x_test = dfTest[tohop]
	y_test = dfTest[['diem chuan']]

	x_train = dfTrain[tohop]
	y_train = dfTrain[['diem chuan']]



	# Chọn giá trị alpha cho rigde regression là 2.5
	alpha = 2.5

	# Khởi tạo đối tượng Ridge regression
	reg_ridge = Ridge(alpha = alpha)

	# Đưa dữ liệu train vào để tiến hành huấn luyện
	reg_ridge.fit(x_train, y_train)

	# Dự đoán điểm chuẩn cho năm 2022
	dc_predict = reg_ridge.predict(x_test)


	dc2022 = dc_predict[0][0]

	print('Điểm chuẩn: ', y_test)
	print('Điểm dự đoán: ', dc2022)

	print('Hệ số: ', reg_ridge.coef_)

	res = "Điểm dự đoán: " + "{:.2f}".format(dc2022) + "\n"
	res += "Hệ số: " + str(reg_ridge.coef_) + "\n"



	diem_chuan = np.append(y_train.to_numpy(), [y_test])
	# diem_chuan = y_train.to_numpy()

	diem_du_doan = np.array([])

	for i in range(len(dfTrain.index)):
		df = dfTrain.iloc[i]
		xx = df[tohop]
		yy = df[['diem chuan']]
		bmp = reg_ridge.predict([xx])
		print(bmp)
		diem_du_doan = np.append(diem_du_doan, [bmp])

		res += "Train " + str(int(df[['nam']])) + ": " + str("{:.2f}".format(bmp[0][0])) + "\n"



	lblKq.configure(text = res)

	diem_du_doan = np.append(diem_du_doan, [dc2022])


	nam = np.array([2017, 2018, 2019, 2020, 2021, 2022])

	plt.plot(nam, diem_chuan, 'bo-', label='Điểm chuẩn')
	plt.plot(nam, diem_du_doan, 'ro-', label='Dự đoán', linestyle='dashed')

	plt.legend(loc='best')
	plt.show()


window.mainloop()