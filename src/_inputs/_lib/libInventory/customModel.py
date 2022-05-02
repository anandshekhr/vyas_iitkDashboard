
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import pandas as pd


class CustomTableModel(QtCore.QAbstractTableModel):
    """
    Custom Table Model to handle MongoDB Data
    """
    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        # self.user_data = data
        self._data = data

    def flags(self, index):
        """
        Make table editable.
        make first column non editable
        :param index:
        :return:
        """
        if index.column() > 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        elif index.column() == 1:
            return QtCore.Qt.DecorationRole
        else:
            return QtCore.Qt.ItemIsSelectable

    def rowCount(self, *args, **kwargs):
        return self._data.shape[0]

    def columnCount(self, *args, **kwargs):
        return self._data.shape[1]

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return self._data.iloc[index.row(),index.column()]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[section]

#     def setData(self, index, value, role=QtCore.Qt.EditRole):
#         """
#         Edit data in table cells
#         :param index:
#         :param value:
#         :param role:
#         :return:
#         """
#         if index.isValid():
#             selected_row = self.df[index.row()]
#             selected_column = self.columns[index.column()]
#             selected_row[selected_column] = value
#             self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))
#             ok = databaseOperations.update_existing(selected_row['_id'], selected_row)
#             if ok:
#                 return True
#         return False

#     def insertRows(self):
#         row_count = len(self.user_data)
#         self.beginInsertRows(QtCore.QModelIndex(), row_count, row_count)
#         empty_data = { key: None for key in self.columns if not key=='_id'}
#         document_id = databaseOperations.insert_data(empty_data)
#         new_data = databaseOperations.get_single_data(document_id)
#         self.user_data.append(new_data)
#         row_count += 1
#         self.endInsertRows()
#         return True

#     def removeRows(self, position):
#         row_count = self.rowCount()
#         row_count -= 1
#         self.beginRemoveRows(QtCore.QModelIndex(), row_count, row_count)
#         row_id = position.row()
#         document_id = self.user_data[row_id]['_id']
#         databaseOperations.remove_data(document_id)
#         self.user_data.pop(row_id)
#         self.endRemoveRows()
#         return True


# class ProfilePictureDelegate(QtWidgets.QStyledItemDelegate):
#     """
#     This will open QFileDialog to select image
#     """
#     def __init__(self):
#         QtWidgets.QStyledItemDelegate.__init__(self)

#     def createEditor(self, parent, option, index):
#         editor = QtWidgets.QFileDialog()
#         return editor

#     def setModelData(self, editor, model, index):
#         selected_file =editor.selectedFiles()[0]
#         image = open(selected_file, 'rb').read()
#         model.setData(index, image)


# # class InLineEditDelegate(QtWidgets.QItemDelegate):
# #     """
# #     Delegate is important for inline editing of cells
# #     """

# #     def createEditor(self, parent, option, index):
# #         return super(InLineEditDelegate, self).createEditor(parent, option, index)

# #     def setEditorData(self, editor, index):
# #         text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
# #         editor.setText(str(text))