#!/usr/bin/ python
from __future__ import print_function

import sys
from datetime import datetime

import sane
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QListWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, \
    QFileDialog, QTabWidget, QRadioButton, QButtonGroup, QGroupBox, QLineEdit

app = QApplication(sys.argv)
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.params = {
            'mode' : 'color',
            'sh' : 300,
            'sw' : 400
        }


        self.mainl = QVBoxLayout()
        self.setLayout(self.mainl)
        #adding pannel
        self.horizontal = QHBoxLayout()
        self.left_pannel = QVBoxLayout()
        self.right_pannel = QVBoxLayout()
        self.tab_layout = QVBoxLayout()
        self.horizontal.addLayout(self.left_pannel)
        #self.horizontal.addLayout(self.right_pannel)
        self.horizontal.addLayout(self.tab_layout)
        self.mainl.addLayout(self.horizontal)
        #add widgets for left pannel
        self.device_list = QListWidget()
        self.refresh_btn = QPushButton('Refresh')
        self.left_pannel.addWidget(self.device_list)
        self.left_pannel.addWidget(self.refresh_btn)
        #add right pannel
        self.tabs = QTabWidget()

        self.scan_widget = QWidget()
        self.image = QLabel()
        self.right_pannel.addWidget(self.image)
        self.right_panel_horizontal = QHBoxLayout()
        self.right_pannel.addLayout(self.right_panel_horizontal)
        self.scan_btn = QPushButton('Scan')
        self.save_btn = QPushButton('Save')
        self.right_panel_horizontal.addWidget(self.scan_btn)
        self.right_panel_horizontal.addWidget(self.save_btn)
        self.scan_widget.setLayout(self.right_pannel)
        self.tabs.addTab(self.scan_widget , 'scan')

        self.setting_widget = QWidget()
        self.setting_layout = QVBoxLayout()
        self.color_group = QGroupBox('Color managment')
        self.button_group = QButtonGroup()
        self.color_btn = QRadioButton('Color')
        self.grey_btn = QRadioButton('Grey')
        self.button_group.addButton(self.color_btn)
        self.button_group.addButton(self.grey_btn)
        self.color_group_layout = QVBoxLayout()
        self.color_group.setLayout(self.color_group_layout)
        self.color_group_layout.addWidget(self.color_btn)
        self.color_group_layout.addWidget(self.grey_btn)
        self.setting_layout.addWidget(self.color_group)
        self.setting_widget.setLayout(self.setting_layout)

        self.page_params = QGroupBox('Page Parameters')
        self.page_layout = QVBoxLayout()
        self.border_layout = QHBoxLayout()
        self.size_layout = QHBoxLayout()
        self.page_layout.addLayout(self.border_layout)
        self.page_layout.addLayout(self.size_layout)
        self.page_params.setLayout(self.page_layout)
        self.setting_layout.addWidget(self.page_params)

        self.border_height_label = QLabel('Scan Area Height')
        self.border_width_label = QLabel('Scan Area Width')
        self.border_height = QLineEdit()
        self.border_width = QLineEdit()
        self.border_layout.addWidget(self.border_height_label)
        self.border_layout.addWidget(self.border_height)
        self.border_layout.addWidget(self.border_width_label)
        self.border_layout.addWidget(self.border_width)

        self.size_height_label = QLabel('Size Height')
        self.size_width_label = QLabel('Size Width')
        self.size_height = QLineEdit()
        self.size_width = QLineEdit()
        self.size_layout.addWidget(self.size_height_label)
        self.size_layout.addWidget(self.size_height)
        self.size_layout.addWidget(self.size_width_label)
        self.size_layout.addWidget(self.size_width)

        self.tabs.addTab(self.setting_widget , 'setting')
        self.tab_layout.addWidget(self.tabs)


        self.color_group.clicked.connect(self.setting_change)
        self.page_params.clicked.connect(self.setting_change)


        self.refresh_btn.clicked.connect(self.update_list)
        self.scan_btn.clicked.connect(self.scan)
        self.save_btn.clicked.connect(self.save)
    def setting_change(self):
        try:
            if self.button_group.checkedId() == -2:
                self.params['mode'] = 'color'
            else:
                self.params['mode'] = 'grey'
            self.params['ah'] = int(self.border_height.text())
            self.params['aw'] = int(self.border_width.text())
            self.params['sh'] = int(self.size_height.text())
            self.params['sw'] = int(self.size_width.text())
        except:
            self.params['mode'] = 'grey'
            self.params['sh'] = 300
            self.params['sw'] = 400
            print('setting err')




    def update_list(self):
        self.devices = sane.get_devices()
        for i in self.devices:
            self.device_list.addItem(i[1] + ' - ' + i[2])

    def save(self):
        Fdialog = QFileDialog()
        #Fdialog.setOptions(QFileDialog.ShowDirsOnly)
        workdir = Fdialog.getExistingDirectory()
        print(workdir)
        try:
            dt_string = datetime.now().strftime("%d-%m-%Y %H_%M_%S").split(' ')
            self.device_im.save(workdir +'/' + dt_string[0] +'-'+dt_string[1] + '.png')
        except:
            self.image.setText('Err')

    def scan(self):
        #print(self.device_list.currentIndex().row())
        #print(self.devices[self.device_list.currentIndex().row()])
        #try:

        dev = sane.open(self.devices[self.device_list.currentIndex().row()][0])
        try:
            dev.mode = self.params['mode']

        except:
            self.image.setText('params mode err')
            print(self.params)
        try:
            dev.br_x = self.params['aw']
            dev.br_y = self.params['ah']
        except:
            self.image.setText('params area err Using default')
            print(self.params)
        dev.start()
        self.device_im = dev.snap()
        im = ImageQt(self.device_im)
        pix = QPixmap.fromImage(im)
        pix = pix.scaled(self.params['sw'], self.params['sh'])
        self.image.setPixmap(pix)
        dev.close()
        #except:
        #    self.image.setText('Err')
def run():
    sane.init()
    window=MainWindow()
    window.update_list()
    window.show()
    window.resize(600 , 500)
    window.setWindowTitle('PyScan')

    app.exec()
    sane.exit()

if __name__ == '__main__':
    #app.setStyle('breeze')
    sane.init()
    window=MainWindow()
    window.update_list()
    window.show()
    window.resize(600 , 500)
    window.setWindowTitle('PyScan')

    app.exec()
    sane.exit()