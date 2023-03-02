#!/usr/bin/ python
from __future__ import print_function
import os
import sys
from datetime import datetime
import json
import tomlkit
import sane
import threading
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap , QIcon
from PyQt6.QtWidgets import QWidget, QListWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, \
    QFileDialog, QTabWidget, QRadioButton, QButtonGroup, QGroupBox, QLineEdit , QComboBox


app = QApplication(sys.argv)
app.setStyle('breeze')
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.params = {
            'mode' : 'color',
            'sh' : 300,
            'sw' : 400,
            'dpi' : 300,
            'ah': 3507,
            'aw':2480,
            'size':'A4',
            'save_mode':'png',
            'save_extension': 'png',
            'version':2,
            'lang': 'English'
        }
        self.lang = {
            'English' : {
                'refresh_btn' : 'Refresh',
                'scan_btn' : 'Scan',
                'save_btn': 'Save',
                'scan_tb' : 'Scan',
                'setting_tb' : 'Setting',
                'page_pr' : 'Page parameters',
                'color_tx' : 'Color',
                'color_color' : 'Color',
                'color_grey' : 'Grey',
                'page_tx' : 'Page scale',
                'save_pr' : 'Save parameters',
                'app_pr' : 'App parameters',
                'app_set_pr' : 'Setting parameters',
                'app_appr_pr' : 'Appearance parameters',
                'app_set_load_btn' : 'Load settings',
                'app_set_save_btn': 'Save settings',
                'app_appr_lang_load_btn' : 'Add language (Json)'
            },
            'Українська': {
                'refresh_btn': 'Оновити',
                'scan_btn': 'Сканувати',
                'save_btn': 'Зберегти',
                'scan_tb': 'Сканування',
                'setting_tb': 'Налаштування',
                'page_pr': 'Параметри сторінки',
                'color_tx': 'Колір',
                'color_color': 'Кольоровий',
                'color_grey': 'Ч/Б',
                'page_tx': 'Маштабування сторінки',
                'save_pr': 'Параметри збереження',
                'app_pr': 'Параметри програми',
                'app_set_pr': 'Параметри налаштувань',
                'app_appr_pr': 'Параметри вигляду',
                'app_set_load_btn': 'Завантажити налаштування',
                'app_set_save_btn': 'Зберегти налаштування',
                'app_appr_lang_load_btn': 'Додати мову (Json)'
            }
        }

        self.current_scan_state=False



        self.loads_setting(mode='startup')
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
        self.refresh_btn = QPushButton(self.lang[self.params['lang']]['refresh_btn'])
        self.left_pannel.addWidget(self.device_list)
        self.left_pannel.addWidget(self.refresh_btn)
        #add right pannel
        self.tabs = QTabWidget()

        self.scan_widget = QWidget()
        self.image = QLabel()
        self.right_pannel.addWidget(self.image)
        self.right_panel_horizontal = QHBoxLayout()
        self.right_pannel.addLayout(self.right_panel_horizontal)
        self.scan_btn = QPushButton(self.lang[self.params['lang']]['scan_btn'])
        self.save_btn = QPushButton(self.lang[self.params['lang']]['save_btn'])
        self.right_panel_horizontal.addWidget(self.scan_btn)
        self.right_panel_horizontal.addWidget(self.save_btn)
        self.scan_widget.setLayout(self.right_pannel)
        self.tabs.addTab(self.scan_widget , self.lang[self.params['lang']]['scan_tb'])
        #Page Parameters
        self.setting_widget = QWidget()
        self.setting_layout = QVBoxLayout()
        self.page_group = QGroupBox(self.lang[self.params['lang']]['page_pr'])
        self.page_group_layout = QVBoxLayout()
        self.colorl = QLabel(self.lang[self.params['lang']]['color_tx'])
        self.color_drop = QComboBox()
        self.color_drop.addItem(self.lang[self.params['lang']]['color_grey'])
        self.color_drop.addItem(self.lang[self.params['lang']]['color_color'])
        self.page_group.setLayout(self.page_group_layout)
        self.page_group_layout.addWidget(self.colorl)
        self.page_group_layout.addWidget(self.color_drop)
        self.setting_layout.addWidget(self.page_group)
        self.setting_widget.setLayout(self.setting_layout)
        #self.border_height_label = QLabel('Scan Area Height')
        #self.border_width_label = QLabel('Scan Area Width')
        #self.border_height = QLineEdit()
        #self.border_width = QLineEdit()
        self.dropdown = QComboBox()
        self.dropdown.addItem('A4')
        self.dropdown.addItem('A5')
        self.dropdown.addItem('A6')
        self.page_seting_autol = QLabel(self.lang[self.params['lang']]['page_tx'])
        #self.page_seting_manuall = QLabel('Manual')
        self.page_group_layout.addWidget(self.page_seting_autol)
        self.page_group_layout.addWidget(self.dropdown)
        self.dpi_drop = QComboBox()
        #self.dpi_input.setPlaceholderText('DPI')
        for i in range(100 , 1300 , 100):
            self.dpi_drop.addItem(str(i))
        self.page_group_layout.addWidget(self.dpi_drop)
        #self.page_group_layout.addWidget(self.page_seting_manuall)
        #self.page_group_layout.addWidget(self.border_height_label)
        #self.page_group_layout.addWidget(self.border_height)
        #self.page_group_layout.addWidget(self.border_width_label)
        #self.page_group_layout.addWidget(self.border_width)

        #Save Parameters
        self.save_group = QGroupBox(self.lang[self.params['lang']]['save_pr'])
        self.save_setting_layout = QVBoxLayout()
        self.save_drop = QComboBox()
        self.save_drop.addItem('png')
        self.save_drop.addItem('jpeg')
        self.save_drop.addItem('bmp')
        #self.save_name = QLineEdit()
        #self.save_name.setPlaceholderText('File Name')
        self.save_group.setLayout(self.save_setting_layout)
        self.save_setting_layout.addWidget(self.save_drop)
        #self.save_setting_layout.addWidget(self.save_name)
        self.setting_layout.addWidget(self.save_group)
        #App Parameters
        self.app_group = QGroupBox(self.lang[self.params['lang']]['app_pr'])
        self.app_layout = QVBoxLayout()
        self.setting_app_group = QGroupBox(self.lang[self.params['lang']]['app_set_pr'])
        self.setting_app_layout = QVBoxLayout()
        self.setting_app_group.setLayout(self.setting_app_layout)
        self.load_settings = QPushButton(self.lang[self.params['lang']]['app_set_load_btn'])
        self.save_settings = QPushButton(self.lang[self.params['lang']]['app_set_save_btn'])
        self.setting_app_layout.addWidget(self.load_settings)
        self.setting_app_layout.addWidget(self.save_settings)
        self.app_layout.addWidget(self.setting_app_group)
        self.app_group.setLayout(self.app_layout)
        self.appearance_settings = QGroupBox(self.lang[self.params['lang']]['app_appr_pr'])
        self.appearance_layout = QVBoxLayout()
        self.language_drop = QComboBox()
        #self.language_drop.addItem('Українська')
        #self.language_drop.addItem('English')
        for i in self.lang.keys():
            self.language_drop.addItem(i)
        self.add_language = QPushButton(self.lang[self.params['lang']]['app_appr_lang_load_btn'])
        self.appearance_layout.addWidget(self.language_drop)
        self.appearance_layout.addWidget(self.add_language)
        self.appearance_settings.setLayout(self.appearance_layout)
        self.app_layout.addWidget(self.appearance_settings)
        self.setting_layout.addWidget(self.app_group)





        #tabs
        self.tabs.addTab(self.setting_widget , self.lang[self.params['lang']]['setting_tb'])
        self.tab_layout.addWidget(self.tabs)


        #connects
        self.language_drop.currentTextChanged.connect(self.change_lang)
        self.dpi_drop.currentTextChanged.connect(self.dpi_change)
        self.dropdown.currentTextChanged.connect(self.size_setting)
        self.color_drop.currentTextChanged.connect(self.color_change)
        self.refresh_btn.clicked.connect(self.update_list)
        self.scan_btn.clicked.connect(self.scan)
        self.save_btn.clicked.connect(self.save)
        self.save_settings.clicked.connect(self.saves_setting)
        self.load_settings.clicked.connect(self.loads_setting)
        self.save_drop.currentTextChanged.connect(self.settings_save)
        self.apply_settings()
    def change_lang(self , lang):
        self.params['lang'] = lang

    def color_change(self , mode):
        try:
            for key , item in self.lang[self.params['lang']].items():
                if item == mode:
                    print(key)
                    if key == 'color_color':
                        self.params['mode'] = 'color'
                    else:
                        self.params['mode'] = 'gray'
        except:
            print('Color set err')

    def dpi_change(self ,text):
        try:
            self.params['dpi'] = int(text)
            self.size_setting(self.dropdown.currentText())
        except:
            print('Dpi chage err')

    def page_setting(self , height , width):
        try:
            self.params['ah'] = height
            self.params['aw'] = width
        except:
            print('page err')
            print(height, ' ' , width)

    def size_setting(self , current):
        try:
            if current == 'A4':
                height = round((29.7 / 2.54) * self.params['dpi'])
                width = round((21 / 2.54) * self.params['dpi'])
                print(height, ' ', width)
                self.page_setting(height , width)
            elif current == 'A5':
                height = round((21 / 2.54) * self.params['dpi'])
                width = round((14.8 / 2.54) * self.params['dpi'])
                print(height, ' ', width)
                self.page_setting(height, width)
            else:
                height = round((14.8 / 2.54) * self.params['dpi'])
                width = round((10.5 / 2.54) * self.params['dpi'])
                print(height, ' ', width)
                self.page_setting(height, width)
            self.params['size'] = current
        except:
            print('Size change err')





    def update_list(self):
        try:
            self.device_list.clear()
            threat = threading.Thread(target=self.update_devices_threat)
            threat.start()
        except:
            print('Device update err')

    def update_devices_threat(self):
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
            self.device_im.save(workdir +'/' + dt_string[0] +'-'+dt_string[1] + '.' + self.params['save_extension'], self.params['save_mode'] )
        except:
            self.image.setText('Save err')

    def scan(self):
        #print(self.device_list.currentIndex().row())
        #print(self.devices[self.device_list.currentIndex().row()])
        #try:
        try:
            dev = sane.open(self.devices[self.device_list.currentIndex().row()][0])
        except:
            print('Device open err')
            return
        #print(dev.get_parameters())
        #print(dev.get_options())
        try:
            dev.mode = self.params['mode']

        except:
            print('params mode err')
            print(self.params)
        try:
            dev.br_x = self.params['aw']
            dev.br_y = self.params['ah']
        except:
            print('params area err Using default')
            print(self.params)
        try:
            dev.resolution = self.params['dpi']
        except:
            print('Dpi err')
        try:
            if not self.current_scan_state:
                threat = threading.Thread(target=self.scan_thread , args=(dev,))
                threat.start()
            else:
                pass
        except:
            print('threat err')
        #except:
        #    self.image.setText('Err')
    def scan_thread(self , dev):
        try:
            self.current_scan_state = True
            dev.start()
            self.device_im = dev.snap()
            im = ImageQt(self.device_im)
            pix = QPixmap.fromImage(im)
            pix = pix.scaled(self.params['sw'], self.params['sh'])
            self.image.setPixmap(pix)
            dev.close()
            self.current_scan_state = False
        except:
            print('scan err')
            self.current_scan_state = False


    def settings_save(self , current):
        self.params['save_mode'] = current.upper()
        self.params['save_extension'] = current.lower()

    def saves_setting(self):
        try:
            location = os.getenv("HOME")
            with open(location +'/' + '.pyscan_settings.json' , 'w') as file:
                _ = {}
                _['params'] = self.params
                _['langs'] = self.lang
                location = os.getenv("HOME")
                with open(location + '/' + '.pyscan_setting.toml', 'w') as file:
                    tomlkit.dump(_, file)
        except:
            print('Setting save err')
    def loads_setting(self , mode='0'):
        try:
            location = os.getenv("HOME")
            if mode == 'startup':
                try:
                    with open(location +'/' + '.pyscan_setting.toml' , 'r') as file:
                        _ = tomlkit.parse(file.read())
                        self.params = _['params']
                        self.lang = _['langs']
                        #self.apply_settings()
                except:
                    print('err load setting using default')
            else:
                try:
                    with open(location +'/' + '.pyscan_setting.toml' , 'r') as file:
                        _ = tomlkit.parse(file.read())
                        self.params = _['params']
                        self.lang = _['langs']
                    self.apply_settings()
                except:
                    print('err load setting using default')
        except:
            print('Setting load err')

    def load_langs_from_file(self):
        fdialog = QFileDialog()
        fdialog.setMimeTypeFilters('application/json')
        url = fdialog.getOpenFileUrl()
        try:
            with open(url , 'r') as file:
                loaded = json.load(file)
            self.lang.update(loaded)
        except:
            print('Load language from file err')
    #def load_langs(self):
        #location = os.getenv("HOME")
        #try:
            #with open(location +'/' + '.pyscan_langs.json' , 'r') as file:
                #self.lang = json.load(file)
        #except:
            #with open(location + '/' + '.pyscan_langs.json', 'w') as file:
                #json.dump(self.lang , file)


    def apply_settings(self):
        try:
            if self.params['mode'] == 'color':
                self.color_drop.setCurrentText(self.lang[self.params['lang']]['color_color'])
            else:
                self.color_drop.setCurrentText(self.lang[self.params['lang']]['color_grey'])
            self.dropdown.setCurrentText(self.params['size'])
            self.dpi_drop.setCurrentText(str(self.params['dpi']))
            self.save_drop.setCurrentText(self.params['save_extension'])
            self.language_drop.setCurrentText(self.params['lang'])
        except:
            print('Apply settings err')


def run():
    sane.init()
    window=MainWindow()
    #window.loads_setting()
    window.update_list()
    window.show()
    window.resize(600 , 500)
    window.setWindowTitle('PyScan')

    app.exec()
    sane.exit()

if __name__ == '__main__':
    run()
