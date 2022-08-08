from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QFrame, QPushButton, QWidget, QHBoxLayout, \
    QVBoxLayout, QComboBox, QColorDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import multiprocessing
import ctypes


class MontageSetDialog(QDialog):
    TrainTimes = ['20', '30', '40']
    TestScene = ['拿取水杯', '阻拦小球', '释放小球', '穿戴手套']
    TestTimes = ['10', '20', '30', '40']
    ModelExist = ['是', '否']
    TestMode = ['仅训练', '训练并康复', '仅康复']
    data = []
    signal_returnData = pyqtSignal(list)

    def __init__(self, model_exist):
        super().__init__()
        self.trainTimesComboBox = QComboBox(self)
        self.testSceneComboBox = QComboBox(self)
        self.testTimesComboBox = QComboBox(self)
        # self.modelExistText = QComboBox(self)
        self.modelExistText = QLabel(self)
        self.testModeComboBox = QComboBox(self)

        self.settingsFinishedFlag = multiprocessing.Value('i', 0)
        self.trainTimes = multiprocessing.Value(ctypes.c_char_p, 0)
        self.testScene = multiprocessing.Value(ctypes.c_char_p, 0)
        self.testTimes = multiprocessing.Value(ctypes.c_char_p, 0)
        self.modelExist = multiprocessing.Value(ctypes.c_char_p, 0)
        self.testMode = multiprocessing.Value(ctypes.c_char_p, 0)

        self.fr = QFrame(self)
        self.init_ui()
        if not model_exist:
            self.modelExistText.setText("否")
        else:
            self.modelExistText.setText("是")

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

        name_label = QLabel("<font color = red>*</font>" + "训练次数：")
        name_label.setFont(QFont('微软雅黑', 16, QFont.Normal))
        name_label.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        self.trainTimesComboBox.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.trainTimesComboBox.setFont(QFont('微软雅黑', 16, QFont.Normal))
        self.trainTimesComboBox.addItems(self.TrainTimes)

        channelLabel = QLabel("<font color = red>*</font>" + "康复场景：")
        channelLabel.setFont(QFont('微软雅黑', 16, QFont.Normal))
        channelLabel.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        self.testSceneComboBox.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.testSceneComboBox.setFont(QFont('微软雅黑', 16, QFont.Normal))
        self.testSceneComboBox.addItems(self.TestScene)

        testTimesLabel = QLabel("<font color = red>*</font>" + "康复次数：")
        testTimesLabel.setFont(QFont('微软雅黑', 16, QFont.Normal))
        testTimesLabel.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        self.testTimesComboBox.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.testTimesComboBox.setFont(QFont('微软雅黑', 16, QFont.Normal))
        self.testTimesComboBox.addItems(self.TestTimes)

        modelExistLabel = QLabel("<font color = red>*</font>" + "模型存在：")
        modelExistLabel.setFont(QFont('微软雅黑', 16, QFont.Normal))
        modelExistLabel.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        # self.modelExistText.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        # self.modelExistText.setFont(QFont('微软雅黑', 14, QFont.Normal))
        # self.modelExistText.addItems(self.ModelExist)
        self.modelExistText.setFont(QFont('微软雅黑', 16, QFont.Normal))
        self.modelExistText.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")

        testModeLabel = QLabel("<font color = red>*</font>" + "训练模式：")
        testModeLabel.setFont(QFont('微软雅黑', 16, QFont.Normal))
        testModeLabel.setStyleSheet("QLabel{border-bottom: 1px solid grey;}")
        self.testModeComboBox.setStyleSheet("QLineEdit{border-bottom: 1px solid grey;}")
        self.testModeComboBox.setFont(QFont('微软雅黑', 16, QFont.Normal))
        self.testModeComboBox.addItems(self.TestMode)

        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.trainTimesComboBox, 0, 1)

        layout.addWidget(channelLabel, 1, 0)
        layout.addWidget(self.testSceneComboBox, 1, 1)

        layout.addWidget(testTimesLabel, 2, 0)
        layout.addWidget(self.testTimesComboBox, 2, 1)

        layout.addWidget(modelExistLabel, 3, 0)
        layout.addWidget(self.modelExistText, 3, 1)

        layout.addWidget(testModeLabel, 4, 0)
        layout.addWidget(self.testModeComboBox, 4, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setVerticalSpacing(100)

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

    def channel_change(self):
        index = self.testSceneComboBox.currentIndex()
        print('传入通道索引为%d' % index)

    def name_change(self):
        index = self.trainTimesComboBox.currentIndex()
        print('传入通道索引为%d' % index)

    def information_confrim(self):
        self.trainTimes = self.trainTimesComboBox.currentText()
        self.testScene = self.testSceneComboBox.currentText()
        self.testTimes = self.testTimesComboBox.currentText()
        self.modelExist = self.modelExistText.text()
        self.testMode = self.testModeComboBox.currentText()
        self.settingsFinishedFlag = 1
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    v = MontageSetDialog(model_exist=False)
    v.show()
    sys.exit(app.exec_())
