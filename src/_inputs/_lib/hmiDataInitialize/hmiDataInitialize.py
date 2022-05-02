from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from gui import HMI_Init
from lib import customModel
from lib import get_data_fromFastAPI
import pandas as pd

url = "http://172.26.98.238:8000/hmiPartInfo/"
df = pd.DataFrame(columns=["id","operatorName","operatorIDNo","machineName","variantName","partName","partNumber","timeIN","timeOUT"])


class PythonMongoDB(HMI_Init.Ui_HMIWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(PythonMongoDB, self).__init__()
        self.setupUi(self)
        # self.user_data = databaseOperations.get_multiple_data()
        self.user_data = get_data_fromFastAPI.get_data(url)
        self.dataframe_get()
        self.model = customModel.CustomTableModel(df)
        # self.delegate = customModel.InLineEditDelegate()
        self.tableView.setModel(self.model)

    def dataframe_get(self):
        r1 = self.user_data["data"][0]
        for i in range(0,len(r1)):
            currentItem = r1[i]
            df.loc[i] = [r1[i]["id"],r1[i]["operatorName"],r1[i]["operatorIDNo"],r1[i]["machineName"],r1[i]["variantName"],r1[i]["partName"],r1[i]["partNumber"],r1[i]["timeIN"],r1[i]["timeOUT"]]
        return df
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    my_app = PythonMongoDB()
    my_app.show()
    app.exec_()
