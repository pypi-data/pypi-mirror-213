from Engine import Table as T

class ArrayTable(T.ArrayTable):
    def __init__(self,col:int=0,row:int=0):
        T.ArrayTable.__init__(self,col,row)

    def scatter(self, _coly=1, _colx=0, hight=None):
        import matplotlib.pyplot as plt
        plt.figure(1, figsize=(10, 5))

        if type(_coly) == int:
            plt.scatter(self.table[_colx].data, self.table[_coly].data, s=3)
            if hight is not None:
                plt.scatter(self.table[_colx].data[hight], self.table[_coly].data[hight], s=6, marker="*", c="red")
            plt.xlabel(self.table[_colx].ColName + "(" + self.table[_colx].ColUnit + ")")
            plt.ylabel(self.table[_coly].ColName + "(" + self.table[_coly].ColUnit + ")")
        elif type(_coly) == list:
            for i in _coly:
                plt.scatter(self.table[_colx].data, self.table[i].data, label=self.table[i].ColName)
                plt.xlabel(self.table[_colx].ColName + "(" + self.table[_colx].ColUnit + ")")
                plt.legend()
                plt.ylabel(self.table[_coly[0]].ColName + "(" + self.table[_coly[0]].ColUnit + ")")
        # plt.grid()
        # plt.axhline(y=0,color='r',linestyle="-.")
        # plt.axvline(x=0,color='g',linestyle=":")
        plt.tight_layout()
        plt.show()

    # 读取Excel文件
    def readExcelFile(self, filename, sheetname=0, _header=[0, 1]):
        # TitleUnit表示头和单位的排量方式，0意味着分开排列
        from pandas import read_excel
        df = read_excel(filename, sheet_name=sheetname, header=_header,engine="openpyxl")
        header = df.columns.values
        colName = [str(each[0]) for each in header]
        colUnit = [str(each[1]) for each in header]
        for i in range(len(header)):
            coltoapp = T.PhysicalVarList(0)
            coltoapp.data=list(df[header[i]])
            coltoapp.ColName=colName[i]
            coltoapp.ColUnit=colUnit[i]
            self.append(coltoapp)
        self.row = len(df[header[0]])
        # if datatype == "double":
        #     for i in range(self.col):
        #         self.table[i].convertToFloat()

    def plot(self, _coly=1, _colx=0,save=False):
        import matplotlib.pyplot as plt
        plt.figure(1, figsize=(10, 10))

        if type(_coly) == int:
            plt.plot(self.table[_colx].data, self.table[_coly].data)
            plt.xlabel(self.table[_colx].ColName + "(" + self.table[_colx].ColUnit + ")",fontsize=23)
            plt.ylabel(self.table[_coly].ColName + "(" + self.table[_coly].ColUnit + ")",fontsize=23)
        elif type(_coly) == list:
            for i in _coly:
                plt.plot(self.table[_colx].data, self.table[i].data, label=self.table[i].ColName)
                plt.xlabel(self.table[_colx].ColName + "(" + self.table[_colx].ColUnit + ")",fontsize=23)
                plt.legend(fontsize=20)
                plt.ylabel(self.table[_coly[0]].ColName + "(" + self.table[_coly[0]].ColUnit + ")",fontsize=23)
        # plt.grid()
        # plt.axhline(y=0,color='r',linestyle="-.")
        # plt.axvline(x=0,color='g',linestyle=":")
        # plt.tight_layout()
        # plt.rcParams['font.family'] = ['sans-serif']
        #字体样式和大小
        # plt.rcParams['font.sans-serif'] = ['Times New Roman']
        # plt.rcParams['font.size'] = '20'
        # plt.rcParams['axes.labelsize'] = '20'
        # plt.rcParams['ytick.labelsize'] = '20'
        
        #颜色
        # plt.rcParams['lines.color'] = '#000000'

        # # 显式负号
        # plt.rcParams['axes.unicode_minus'] = False

        # plt.rcParams['image.cmap'] = 'gray'

        # #线宽
        # plt.rcParams['lines.linewidth'] = 3
        # plt.xticks(fontsize=20)
        # plt.yticks(fontsize=20)
        if save:
            plt.savefig("fig.svg",dpi=600,format="svg",bbox_inches='tight',transparent=True)

        plt.show()

    def animation(self, _coly=1, _colx=0):
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        fig = plt.figure(0, figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1)
        # fig, ax = plt.subplots()
        ln, = ax.plot([], [], 'b-', animated=False)
        plt.xlabel(self.table[_colx].ColName + "(" + self.table[_colx].ColUnit + ")")
        plt.ylabel(self.table[_coly].ColName + "(" + self.table[_coly].ColUnit + ")")
        plt.tight_layout()

        def init():
            ax.set_xlim(0.8 * min(self.table[_colx].data), 1.05 * max(self.table[_colx].data))
            ax.set_ylim(0.8 * min(self.table[_coly].data), 1.05 * max(self.table[_coly].data))
            return ln,
            # ax.set_xlim(0, 2 * np.pi)
            # ax.set_ylim(-1, 1)
            # return ln,

        def update(i):
            # ln.set_data(range(i),range(i))
            ln.set_data(self.table[_colx].data[:i], self.table[_coly].data[:i])
            # print(i)
            return ln,

        ani = FuncAnimation(fig, update, frames=np.arange(0, self.row), interval=0.00001,
                            init_func=init, blit=True, repeat=False)
        # ani.save("temp12.gif", writer="pillow",fps=30)
        plt.show()

    def fromPandas(self,data):
        self.clear()
        self.setParaName(data.columns)
        self.setParaUnit(["EmptyUnit"]*self.row)
        # for j in range(len(data.columns)):
        #     self.table[j].data=data.iloc[:,j]
        for index, row in data.iterrows():
            self.append(row)
        # for i in range(len(data)):
        #     self.append(data.iloc[i, :])


    # 高斯回归，x为预测向量，xcolumn为训练集x所在的行，ycolumn为训练集的y，kerneltype和函数的类型
    # 当trained=True模型已经训练完成，可以直接预测，当trained==False则先训练函数
    def GPR(self, x, xcolumn=[0], ycolumn=1, kerneltype="Matern", trained=True):
        from sklearn.preprocessing import MinMaxScaler
        from numpy import array, newaxis
        # import numpy as np
        Xtrain = array([self.table[i].data for i in xcolumn]).T
        Ytrain = array(self.table[ycolumn].data)[:, newaxis]



        # 将训练集归一化到[0.01,0.99]
        xscaler = MinMaxScaler(feature_range=(0.01, 0.99))
        yscaler = MinMaxScaler(feature_range=(0.01, 0.99))
        Xfit = xscaler.fit_transform(Xtrain)
        Yfit = yscaler.fit_transform(Ytrain)

        # 如果训练未完成，则训练
        if trained == False:
            from sklearn.gaussian_process import GaussianProcessRegressor
            if kerneltype == "Matern":
                from sklearn.gaussian_process.kernels import Matern
                kernel = Matern(length_scale=1.0, length_scale_bounds=(0.01, 0.99))
            if kerneltype == "RBF":
                from sklearn.gaussian_process.kernels import RBF
                kernel = RBF(length_scale=1.0, length_scale_bounds=(0.01, 0.99))
            if kerneltype == "DotProduct":
                from sklearn.gaussian_process.kernels import DotProduct
                kernel = DotProduct(sigma_0=1.0, sigma_0_bounds=(0.01, 0.99)) ** 2
            self.gp = GaussianProcessRegressor(kernel=kernel)
            self.gp.fit(Xfit, Yfit)

        # 获取每一个属性的最大最小值
        minn = [min(each) for each in Xtrain.T]
        maxx = [max(each) for each in Xtrain.T]

        # 处理预测向量，使之归一化到区间

        xx=0.01 + (array(x) - array(minn)) / (array(maxx) - array(minn)) * (0.99 - 0.01)
        # xx=xx[:,newaxis]

        # print(xx)

        # xx = []
        # for each in x:
        #     xx.append(0.01 + (array(each) - array(minn)) / (array(maxx) - array(minn)) * (0.99 - 0.01))

        # # for i in range(len(x)):
        # #     xx.append(0.01 + (x[i] - minn[i]) / (maxx[i] - minn[i]) * (0.99 - 0.01))
        xx = array([xx])
        # print(xx)

        # 预测
        y_mean, y_std = self.gp.predict(xx, return_std=True)

        # 还原y的真实值
        return yscaler.inverse_transform(y_mean[:,newaxis])[0]


