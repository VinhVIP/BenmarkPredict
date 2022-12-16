#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


# Đọc dữ liệu được lưu ở file có định dạng .csv
data = pd.read_csv('data/data_qtkd.csv')

data


# In[8]:


# Chuyển dữ liệu từ file csv vào data frame
df = pd.DataFrame(data)

# Lấy năm cuối cùng (2022) làm data test
index_test = len(df.index) - 1

df_test = df.iloc[index_test]
x_test = df_test[['ti le trung tuyen', 'dtb ca nuoc', 'tong dang ky']]
y_test = df_test[['diem chuan']]

# Loại bỏ data của năm có `index_test`
# Những data còn lại sẽ sử dụng để làm data train
df_train = df.drop(df.index[index_test])
x_train = df_train[['ti le trung tuyen', 'dtb ca nuoc', 'tong dang ky']]
y_train = df_train[['diem chuan']]

# Chọn giá trị alpha cho rigde regression là 2.5
alpha = 2.5

# Khởi tạo đối tượng Ridge regression
reg_ridge = Ridge(alpha = alpha)

# Đưa dữ liệu train vào để tiến hành huấn luyện
reg_ridge.fit(x_train, y_train)

# Dự đoán điểm chuẩn cho năm 2022
dc_predict = reg_ridge.predict([x_test])

dc2022 = dc_predict[0][0]

print('Điểm chuẩn: ', y_test[0])
print('Điểm dự đoán: ', dc2022)

print('Hệ số: ', reg_ridge.coef_)


# In[9]:


diem_chuan = np.append(y_train.to_numpy(), [y_test])

diem_du_doan = np.array([])

for i in range(len(df.index)-1):
    df_test = df.iloc[i]
    x_test = df_test[['ti le trung tuyen', 'dtb ca nuoc', 'tong dang ky']]
    y_test = df_test[['diem chuan']]
    
    dc_predict = reg_ridge.predict([x_test])
    diem_du_doan = np.append(diem_du_doan, [dc_predict])

diem_du_doan = np.append(diem_du_doan, [dc2022])


nam = np.array([2017, 2018, 2019, 2020, 2021, 2022])

plt.plot(nam, diem_chuan, 'bo-', label='Điểm chuẩn', linestyle='dashed')
plt.plot(nam, diem_du_doan, 'ro-', label='Dự đoán')
plt.title("Quản trị kinh doanh")
plt.legend(loc='best')
plt.show()

