import csv
 

arr = [0,0,0,0,0,0]
k = 3
n = 8

columns_name = []


def printRes(k):
    global arr
    global columns_name

    a = []
    for i in range(1, k+1):
        a.append(columns_name[arr[i]+1])
    print(a)

def gen(i, n, k):
    global arr

    for j in range(arr[i-1]+1, n-k+i+1):
        arr[i] = j
        if i == k:
            printRes(k)
        else:
            gen(i+1, n, k)



def call():
    with open('C:/Users/vinhv/Documents/Jupyter/data/data_cntt_test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        
        global columns_name

        for row in csv_reader:
            columns_name = row
            print(row)
            break

        gen(1,n,k)

 
call()

# print("List of column names : ",
#       list_of_column_names[0])