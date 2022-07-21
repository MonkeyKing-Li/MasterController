from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QGridLayout, QFrame, QPushButton, QWidget, QHBoxLayout, \
    QVBoxLayout, QComboBox, QColorDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import multiprocessing
from settings_ui.tools import StoppableProcess


class MontageSetDialog(QDialog, StoppableProcess):
    montageData = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
        '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
        '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
        '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
        '61', '62', '63', '64'
    ]
    electrodes = [
        'Cz', 'CP1', 'C4', 'Pz', 'O1',
        'Fp1', 'CP6', 'O2', 'CP2', 'P8',
        'C3', 'P7', 'Fp2', 'F8', 'CP5',
        'F7', 'HEOL', 'FC5', 'HEOR', 'P4',  # 20
        'T7', 'F3', 'T8', 'FC2', 'PO4',
        'FC6', 'P3', 'PO3', 'Oz', 'F4',
        'FC1', 'Fz', 'FC4', 'Fpz', 'P6',
        'FCz', 'C6', 'POz', 'F6', 'PO6',  # 40
        'PO8', 'C2', 'TP8', 'F2', 'FT8',
        'AF4', 'AF8', 'CP4', 'AF7', 'CP3',
        'FT7', 'AF3', 'TP7', 'F1', 'PO7',
        'C1', 'F5', 'PO5', 'C5', 'ECG',
        'P5', 'VEOL', 'FC3', 'VEOU'
    ]
    data = []
    signal_returnData = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.exit_flag = multiprocessing.Value('i', 0)
        self.colorLineEdit = QLineEdit()
        self.colorbtn = QPushButton('点击设置颜色')
        self.refLineEdit = QLineEdit()
        self.channelComboBox = QComboBox(self)
        self.nameComboBox = QComboBox(self)
        self.fr = QFrame(self)
        self.init_ui()
        self.colorbtn.setStyleSheet("color:rgb(255,255,255);font-size:36px;background-color:%s ;\
        border:2px groove gray;border-radius:10px;padding:2px 4px" % self.colorLineEdit.text())

    def init_ui(self):
        # --------------------加个logal----------------------------
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(852, 786)

        self.fr.setFixedSize(852, 786)
        self.fr.setStyleSheet("QWidget{background-color:rgb(255,255,255);border:1px;border-radius:15px;}")

        mainlay = QVBoxLayout()
        header_widget = QWidget()

        grid_widget = QWidget()
        layout = QGridLayout()

        name_label = QLabel("<font color = red>*</font>" + "Name:")
        name_label.setFont(QFont('微软雅黑', 14, QFont.Normal))
        name_label.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        self.nameComboBox.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.nameComboBox.setFont(QFont('微软雅黑', 14, QFont.Normal))
        self.nameComboBox.addItems(self.electrodes)

        channelLabel = QLabel("<font color = red>*</font>" + "channel:")
        channelLabel.setFont(QFont('微软雅黑', 14, QFont.Normal))
        channelLabel.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        self.channelComboBox.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.channelComboBox.setFont(QFont('微软雅黑', 14, QFont.Normal))
        self.channelComboBox.addItems(self.montageData)

        self.channelComboBox.currentIndexChanged.connect(self.channel_change)
        self.nameComboBox.currentIndexChanged.connect(self.name_change)

        refLabel = QLabel("<font color = red>*</font>" + "ref:")
        refLabel.setFont(QFont('微软雅黑', 14, QFont.Normal))
        refLabel.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        self.refLineEdit.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.refLineEdit.setFont(QFont('微软雅黑', 14, QFont.Normal))
        self.refLineEdit.setText('unknown')

        colorWidget = QWidget()
        colorLineLayout = QHBoxLayout()
        colorLabel = QLabel("<font color = red>*</font>" + "color:")
        colorLabel.setFont(QFont('微软雅黑', 14, QFont.Normal))
        colorLabel.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")

        self.colorbtn.clicked.connect(self.color_edit)
        self.colorLineEdit.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.colorLineEdit.setFont(QFont('微软雅黑', 14, QFont.Normal))

        colorLineLayout.addWidget(colorLabel)
        colorLineLayout.addWidget(self.colorbtn)
        colorWidget.setLayout(colorLineLayout)

        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.nameComboBox, 0, 1)

        layout.addWidget(refLabel, 1, 0)
        layout.addWidget(self.refLineEdit, 1, 1)

        layout.addWidget(channelLabel, 2, 0)
        layout.addWidget(self.channelComboBox, 2, 1)

        layout.addWidget(colorLabel, 3, 0)
        layout.addWidget(self.colorbtn, 3, 1)
        layout.addWidget(self.colorLineEdit, 4, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)

        widget = QWidget()
        widget.setFixedSize(852, 100)
        btnLay = QHBoxLayout()

        okBtn = QPushButton('确定')
        okBtn.setFixedSize(397, 86)
        okBtn.setStyleSheet(
            "color:rgb(255,255,255);font-size:34px;font-weight:bold;background-color:rgb(0,143,255);border:2px groove "
            "gray;border-radius:10px;padding:2px 4px")
        okBtn.clicked.connect(self.information_confrim)
        btnLay.addWidget(okBtn)
        btnLay.setAlignment(Qt.AlignCenter)
        widget.setLayout(btnLay)

        header_widget.setFixedSize(852, 52)
        closeLay = QHBoxLayout()
        closeBtn1 = QPushButton()
        closeBtn = QPushButton()
        closeBtn.setFixedSize(36, 36)
        closeBtn.setStyleSheet(
            "QPushButton{border-image: url(../res/close.png);border-radius: 30px;border: 2px groove gray;border-style: "
            "outset;}")

        closeBtn.clicked.connect(self.close)
        closeLay.addWidget(closeBtn)
        closeLay.setAlignment(Qt.AlignRight)
        closeLay.addWidget(closeBtn1)
        header_widget.setLayout(closeLay)

        grid_widget.setLayout(layout)
        mainlay.addWidget(header_widget)
        mainlay.addWidget(grid_widget)
        mainlay.addWidget(widget)
        mainlay.setContentsMargins(20, 0, 20, 20)
        self.fr.setLayout(mainlay)

    def color_edit(self):
        c = QColorDialog()
        colorName = c.getColor().name()
        print(colorName)
        self.colorLineEdit.setText(colorName)
        self.colorbtn.setStyleSheet(
            "color:rgb(255,255,255) ; font-size:36px;background-color:%s;border:2px groove "
            "gray;border-radius:10px;padding:2px 4px" % colorName)

    def channel_change(self):
        index = self.channelComboBox.currentIndex()
        self.nameComboBox.setCurrentIndex(index)

    def name_change(self):
        index = self.nameComboBox.currentIndex()
        self.channelComboBox.setCurrentIndex(index)
        print('传入通道索引为%d' % index)

    def information_confrim(self):
        self.data.clear()
        self.data.append('tempid')
        self.data.append(self.nameComboBox.currentText())
        self.data.append(self.refLineEdit.text())
        self.data.append(self.channelComboBox.currentText())
        self.data.append(self.colorLineEdit.text())
        print('return {}'.format(self.data))
        self.exit_flag.value = 1
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    v = MontageSetDialog()
    v.show()
    sys.exit(app.exec_())
