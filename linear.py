

class Matrix:
    def __init__(self, rows=0, cols=0, arr = None):
        if arr == None:
            self.rowCount = rows
            self.colCount = cols
            self.data = [[0.0] * cols] * rows
        else:
            self.rowCount = len(arr)
            self.colCount = len(arr[0])
            self.data = [[0.0] * self.colCount] * self.rowCount

            self.data = arr


    def getRow(self, row):
        return self.data[row]

    def getValue(self, row, col):
        return self.data[row][col]
    
    def setRow(self, row, rowData):
        self.data[row] = rowData

    def setValue(self, row, col, value):
        rowData = []
        for i in range(len(self.data[row])):
            if i == col:
                rowData.append(value)
            else:
                rowData.append(self.data[row][i])
        self.data[row] = rowData

    def multiple(self, matrix):
        rc1 = self.rowCount
        cc1 = self.colCount
        rc2 = matrix.rowCount
        cc2 = matrix.colCount

        result = Matrix(rows = rc1, cols = cc2)

        for i in range(rc1):
            for j in range(cc2):
                for k in range(rc2):
                    prod = self.getValue(i, k) * matrix.getValue(k, j)
                    result.setValue(i, j, result.getValue(i, j) + prod)

        return result

    def transpose(self):
        rc = self.rowCount
        cc = self.colCount

        trans = Matrix(rows = cc, cols = rc)
        for i in range(cc):
            for j in range(rc):
                trans.setValue(i, j, self.getValue(j, i))
        
        return trans
    
    def toReducedRowEchelonForm(self):
        lead = 0
        rc = self.rowCount
        cc = self.colCount

        for r in range(rc):
            if cc <= lead:
                return
            i = r
            while self.getValue(i, lead) == 0.0:
                i = i+1
                if rc == i:
                    i = r
                    lead = lead + 1
                    if cc == lead:
                        return
            
            temp = self.getRow(i)
            self.setRow(i, self.getRow(r))
            self.setRow(r, temp)

            if self.getValue(r, lead) != 0.0:
                div = self.getValue(r, lead)
                for j in range(cc):
                    self.setValue(r, j, self.getValue(r, j) / div)

            for k in range(rc):
                if k != r:
                    mult = self.getValue(k, lead)
                    for j in range(cc):
                        prod = self.getValue(r, j) * mult
                        self.setValue(k, j, self.getValue(k, j) - prod)
            
            lead = lead + 1

    
    def inverse(self):
        len = self.rowCount
        aug = Matrix(rows = len, cols = len * 2)

        for i in range(len):
            for j in range(len):
                aug.setValue(i, j, self.getValue(i, j))
            
            aug.setValue(i, i+len, 1.0)

        
        aug.toReducedRowEchelonForm()
        inv = Matrix(rows = len, cols = len)

        for i in range(len):
            for j in range(len, 2*len):
                inv.setValue(i, j-len, aug.getValue(i, j))
        
        return inv


# def linearRegression(x, y):
#         tm = Matrix(arr = [y])
#         cy = tm.transpose()
#         cx = x.transpose()
#         return x.multiple(cx).inverse().multiple(x).multiple(cy).transpose().getRow(0)


class MyLinearRegression():

    def fit(self, X, Y):
        x = Matrix(arr = X)
        tm = Matrix(arr = [Y])
        cy = tm.transpose()
        cx = x.transpose()
        self.coef_ = x.multiple(cx).inverse().multiple(x).multiple(cy).transpose().getRow(0)

    def predict(self, x):
        res = 0.0
        for i in range(len(x)):
            res = res + x[i] * self.coef_[i]
        return res


# y = [23.25, 20.25, 22.0, 25.1, 25.9]
# x = Matrix(arr = [[0.555667, 0.517833, 0.585333, 0.692167, 0.697], [0.1912, 0.2192, 0.1417, 0.1749, 0.2513], [1.0, 1.0, 1.0, 1.0, 1.0]])

# x_test = [0.708666, 0.1979, 1]
# # v = linearRegression(x, y)
# # print(v)

# linear = MyLinearRegression()
# linear.fit(x, y)

# print(linear.coef_)
# print(linear.predict(x_test))











