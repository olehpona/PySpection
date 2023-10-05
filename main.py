from __future__ import print_function
import os
import sys
from datetime import datetime
import json
import tomlkit
import sane
import threading
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QListWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, \
    QFileDialog, QTabWidget, QGroupBox, QLineEdit, QComboBox, QCheckBox, QSpinBox
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

app = QApplication(sys.argv)
apply_stylesheet(app, theme='light_amber.xml')
app.setStyle('Breeze')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.params = {
            'mode': 'color',
            'sh': 300,
            'sw': 400,
            'dpi': 300,
            'br_x': 3507,
            'br_x': 2480,
            'size': 'A4',
            'save_mode': 'png',
            'save_extension': 'png',
            'version': 3.60,
            'lang': 'English',
            'auto_settings': True,
            'theme': 'Material light'
        }
        self.lang = {
            'English': {
                'refresh_btn': 'Refresh',
                'scan_btn': 'Scan',
                'save_btn': 'Save',
                'scan_tb': 'Scan',
                'setting_tb': 'Setting',
                'page_pr': 'Page parameters',
                'color_tx': 'Color',
                'color_color': 'Color',
                'color_grey': 'Grey',
                'page_tx': 'Page size',
                'page_tx_custom': 'Custom page size (mm)',
                'page_tx_dpi': 'Scan DPI',
                'save_pr': 'Save parameters',
                'app_pr': 'App parameters',
                'app_set_pr': 'Setting parameters',
                'app_appr_pr': 'Appearance parameters',
                'app_set_load_btn': 'Load settings',
                'app_set_save_btn': 'Save settings',
                'app_appr_lang_load_btn': 'Add language (Json)',
                'app_set_auto': 'Auto load/save settings',
                'load_lang_win_title': 'Chose language file',
                'save_win_title': 'Chose directory to save file'
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
                'page_tx_custom': 'Ручний розмір сторінки (мм)',
                'page_tx_dpi': 'DPI сканування',
                'save_pr': 'Параметри збереження',
                'app_pr': 'Параметри програми',
                'app_set_pr': 'Параметри налаштувань',
                'app_appr_pr': 'Параметри вигляду',
                'app_set_load_btn': 'Завантажити налаштування',
                'app_set_save_btn': 'Зберегти налаштування',
                'app_appr_lang_load_btn': 'Додати мову (Json)',
                'app_set_auto': 'Авто збереження/загрузка налаштувань',
                'load_lang_win_title': 'Виберіть мовний файл',
                'save_win_title': 'Виберіть директорію для запису файла'
            },
            'Français': {
                'refresh_btn': 'Actualiser',
                'scan_btn': 'Scanner',
                'save_btn': 'Enregistrer',
                'scan_tb': 'Numériser',
                'setting_tb': 'Paramètre',
                'page_pr': 'Paramètres de la page',
                'color_tx': 'Couleur',
                'color_color': 'Couleur',
                'color_grey': 'Gris',
                'page_tx': 'Échelle de la page',
                'page_tx_custom': 'Format de page personnalisé (mm)',
                'page_tx_dpi': 'numériser DPI',
                'save_pr': 'Enregistrer les paramètres',
                'app_pr': "Paramètres de l'application",
                'app_set_pr': 'Paramètres de réglage',
                'app_appr_pr': "Paramètres d'apparence",
                'app_set_load_btn': 'Charger les paramètres',
                'app_set_save_btn': 'Enregistrer les paramètres',
                'app_appr_lang_load_btn': 'Ajouter une langue (Json)',
                'app_set_auto': 'Charger/enregistrer automatiquement les paramètres',
                'load_lang_win_title': 'Choisir le fichier de langue',
                'save_win_title': 'Choisir le répertoire pour enregistrer le fichier'
            },
            'Polski': {
                'refresh_btn': 'Odśwież',
                'scan_btn': 'Skanuj',
                'save_btn': 'Zapisz',
                'scan_tb': 'Skanuj',
                'setting_tb': 'Ustawienie',
                'page_pr': 'Parametry strony',
                'color_tx': 'Kolor',
                'color_color': 'Kolor',
                'color_grey': 'Szary',
                'page_tx': 'Skala strony',
                'page_tx_custom': 'Niestandardowy rozmiar strony (mm)',
                'page_tx_dpi': 'Skanuj DPI',
                'save_pr': 'Zapisz parametry',
                'app_pr': 'Parametry aplikacji',
                'app_set_pr': 'Ustawianie parametrów',
                'app_appr_pr': 'Parametry wyglądu',
                'app_set_load_btn': 'Załaduj ustawienia',
                'app_set_save_btn': 'Zapisz ustawienia',
                'app_appr_lang_load_btn': 'Dodaj język (Json)',
                'app_set_auto': 'Automatyczne ładowanie/zapisywanie ustawień',
                'load_lang_win_title': 'Wybierz plik językowy',
                'save_win_title': 'Wybierz katalog do zapisania pliku'
            },
            'Deutsch': {
                'refresh_btn': 'Aktualisieren',
                'scan_btn': 'Scannen',
                'save_btn': 'Speichern',
                'scan_tb': 'Scannen',
                'setting_tb': 'Einstellung',
                'page_pr': 'Seitenparameter',
                'color_tx': 'Farbe',
                'color_color': 'Farbe',
                'color_grey': 'Grau',
                'page_tx': 'Seitenskalierung',
                'page_tx_custom': 'Benutzerdefinierte Seitengröße (mm)',
                'page_tx_dpi': 'DPI scannen',
                'save_pr': 'Parameter speichern',
                'app_pr': 'App-Parameter',
                'app_set_pr': 'Einstellungsparameter',
                'app_appr_pr': 'Darstellungsparameter',
                'app_set_load_btn': 'Einstellungen laden',
                'app_set_save_btn': 'Einstellungen speichern',
                'app_appr_lang_load_btn': 'Sprache hinzufügen (Json)',
                'app_set_auto': 'Einstellungen automatisch laden/speichern',
                'load_lang_win_title': 'Sprachdatei wählen',
                'save_win_title': 'Verzeichnis zum Speichern der Datei wählen'
            }
        }

        self.custome = {}
        self.current_page_change_state = False
        self.current_scan_state = False

        self.add_size = AddSize(self.add_new_size)
        if self.params['auto_settings']:
            self.loads_setting(mode='startup')

        self.mainl = QVBoxLayout()
        self.setLayout(self.mainl)
        # adding pannel
        self.horizontal = QHBoxLayout()
        self.left_pannel = QVBoxLayout()
        self.right_pannel = QVBoxLayout()
        self.tab_layout = QVBoxLayout()
        self.horizontal.addLayout(self.left_pannel)
        # self.horizontal.addLayout(self.right_pannel)
        self.horizontal.addLayout(self.tab_layout)
        self.mainl.addLayout(self.horizontal)
        # add widgets for left pannel
        self.device_list = QListWidget()
        self.refresh_btn = QPushButton(self.lang[self.params['lang']]['refresh_btn'])
        self.left_pannel.addWidget(self.device_list)
        self.left_pannel.addWidget(self.refresh_btn)
        # add right pannel
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
        self.tabs.addTab(self.scan_widget, self.lang[self.params['lang']]['scan_tb'])
        # Page Parameters
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
        # self.border_height_label = QLabel('Scan Area Height')
        # self.border_width_label = QLabel('Scan Area Width')
        # self.border_height = QLineEdit()
        # self.border_width = QLineEdit()
        self.pageSize = QComboBox()
        self.pageSize.addItem('A4')
        self.pageSize.addItem('A5')
        self.pageSize.addItem('A6')
        self.pageSize.addItem('Custom')
        self.pageSize_custom_layout = QHBoxLayout()
        self.pageSize_custom_width = QSpinBox()
        self.pageSize_custom_width.setMinimum(1)
        self.pageSize_custom_width.setMaximum(10000)
        self.pageSize_custom_height = QSpinBox()
        self.pageSize_custom_height.setMinimum(1)
        self.pageSize_custom_height.setMaximum(10000)
        self.pageSize_custom_label = QLabel(self.lang[self.params['lang']]['page_tx_custom'])
        self.pageSize_custom_layout.addWidget(self.pageSize_custom_width)
        self.pageSize_custom_layout.addWidget(self.pageSize_custom_height)

        self.page_seting_autol = QLabel(self.lang[self.params['lang']]['page_tx'])
        # self.page_seting_manuall = QLabel('Manual')
        self.page_group_layout.addWidget(self.page_seting_autol)
        self.page_group_layout.addWidget(self.pageSize)
        self.page_group_layout.addWidget(self.pageSize_custom_label)
        self.page_group_layout.addLayout(self.pageSize_custom_layout)
        self.page_setting_dpi = QLabel(self.lang[self.params['lang']]['page_tx_dpi'])
        self.page_group_layout.addWidget(self.page_setting_dpi)
        self.dpi_drop = QComboBox()
        # self.dpi_input.setPlaceholderText('DPI')
        for i in range(100, 1300, 100):
            self.dpi_drop.addItem(str(i))
        self.page_group_layout.addWidget(self.dpi_drop)
        # self.page_group_layout.addWidget(self.page_seting_manuall)
        # self.page_group_layout.addWidget(self.border_height_label)
        # self.page_group_layout.addWidget(self.border_height)
        # self.page_group_layout.addWidget(self.border_width_label)
        # self.page_group_layout.addWidget(self.border_width)

        # Save Parameters
        self.save_group = QGroupBox(self.lang[self.params['lang']]['save_pr'])
        self.save_setting_layout = QVBoxLayout()
        self.save_drop = QComboBox()
        self.save_drop.addItem('png')
        self.save_drop.addItem('jpeg')
        self.save_drop.addItem('bmp')
        # self.save_name = QLineEdit()
        # self.save_name.setPlaceholderText('File Name')
        self.save_group.setLayout(self.save_setting_layout)
        self.save_setting_layout.addWidget(self.save_drop)
        # self.save_setting_layout.addWidget(self.save_name)
        self.setting_layout.addWidget(self.save_group)
        # App Parameters
        self.app_group = QGroupBox(self.lang[self.params['lang']]['app_pr'])
        self.app_layout = QVBoxLayout()
        self.setting_app_group = QGroupBox(self.lang[self.params['lang']]['app_set_pr'])
        self.setting_app_layout = QVBoxLayout()
        self.setting_app_group.setLayout(self.setting_app_layout)
        self.load_settings = QPushButton(self.lang[self.params['lang']]['app_set_load_btn'])
        self.save_settings = QPushButton(self.lang[self.params['lang']]['app_set_save_btn'])
        self.auto_settings = QCheckBox(self.lang[self.params['lang']]['app_set_auto'])

        self.setting_app_layout.addWidget(self.load_settings)
        self.setting_app_layout.addWidget(self.save_settings)
        self.setting_app_layout.addWidget(self.auto_settings)
        self.app_layout.addWidget(self.setting_app_group)
        self.app_group.setLayout(self.app_layout)
        self.appearance_settings = QGroupBox(self.lang[self.params['lang']]['app_appr_pr'])
        self.appearance_layout = QVBoxLayout()
        self.language_drop = QComboBox()
        # self.language_drop.addItem('Українська')
        # self.language_drop.addItem('English')
        self.theme_drop = QComboBox()
        self.theme_drop.addItem('Material dark')
        self.theme_drop.addItem('Material light')
        for i in self.lang.keys():
            self.language_drop.addItem(i)
        self.add_language = QPushButton(self.lang[self.params['lang']]['app_appr_lang_load_btn'])
        self.appearance_layout.addWidget(self.language_drop)
        self.appearance_layout.addWidget(self.add_language)
        self.appearance_settings.setLayout(self.appearance_layout)
        self.app_layout.addWidget(self.appearance_settings)
        self.setting_layout.addWidget(self.app_group)
        self.appearance_layout.addWidget(self.theme_drop)

        # tabs
        self.tabs.addTab(self.setting_widget, self.lang[self.params['lang']]['setting_tb'])
        self.tab_layout.addWidget(self.tabs)

        # connects
        self.theme_drop.currentTextChanged.connect(self.apply_theme)
        self.language_drop.currentTextChanged.connect(self.change_lang)
        self.dpi_drop.currentTextChanged.connect(self.dpi_change)
        self.pageSize_custom_width.valueChanged.connect(self.manual_page_size_change)
        self.pageSize_custom_height.valueChanged.connect(self.manual_page_size_change)
        self.pageSize.currentTextChanged.connect(self.size_setting)
        self.color_drop.currentTextChanged.connect(self.color_change)
        self.refresh_btn.clicked.connect(self.update_list)
        self.scan_btn.clicked.connect(self.scan)
        self.save_btn.clicked.connect(self.save)
        self.save_settings.clicked.connect(self.saves_setting)
        self.load_settings.clicked.connect(self.loads_setting)
        self.save_drop.currentTextChanged.connect(self.settings_save)
        self.add_language.clicked.connect(self.load_langs_from_file)
        self.auto_settings.setTristate(False)
        self.auto_settings.stateChanged.connect(self.change_auto_settings)
        if self.params['auto_settings']:
            self.apply_settings()
            self.auto_settings.setCheckState(Qt.CheckState(2))

    def change_auto_settings(self, state):
        if state == 0:
            self.params['auto_settings'] = False
        else:
            self.params['auto_settings'] = True

    def change_lang(self, lang):
        self.params['lang'] = lang

    def manual_page_size_change(self):
        try:
            if not self.current_page_change_state:
                self.params['br_y'] = self.pageSize_custom_height.value()
                self.params['br_x'] = self.pageSize_custom_width.value()
                self.pageSize.setCurrentText('Custom')
                self.params['size'] = 'Custom'
            else:
                self.current_page_change_state = False
        except Exception as e:
            print(e)

    def add_new_size(self, height, width):
        self.custome[height, 'x', width] = {'height': int(height), 'width': int(width)}
        self.dropdown.addItem(height, 'x', width)

    def color_change(self, mode):
        try:
            for key, item in self.lang[self.params['lang']].items():
                if item == mode:
                    print(key)
                    if key == 'color_color':
                        self.params['mode'] = 'color'
                    else:
                        self.params['mode'] = 'gray'
        except:
            print('Color set err')

    def dpi_change(self, text):
        try:
            self.params['dpi'] = int(text)
            self.size_setting(self.pageSize.currentText())
        except:
            print('Dpi chage err')

    def page_setting(self, height, width):
        try:
            self.params['br_y'] = height
            self.params['br_x'] = width
        except:
            print('page err')
            print(height, ' ', width)

    def size_setting(self, current):
        try:

            if current == 'A4':
                height = 297
                width = 210
                self.current_page_change_state = True
                self.pageSize_custom_width.setValue(width)
                self.current_page_change_state = True
                self.pageSize_custom_height.setValue(height)
                print(height, ' ', width)
                self.page_setting(height, width)
            elif current == 'A5':
                height = 210
                width = 148
                self.current_page_change_state = True
                self.pageSize_custom_width.setValue(width)
                self.current_page_change_state = True
                self.pageSize_custom_height.setValue(height)
                print(height, ' ', width)
                self.page_setting(height, width)
            elif current == 'A6':
                height = 148
                width = 105
                self.current_page_change_state = True
                self.pageSize_custom_width.setValue(width)
                self.current_page_change_state = True
                self.pageSize_custom_height.setValue(height)
                print(height, ' ', width)
                self.page_setting(height, width)
            else:
                pass
            self.params['size'] = current
            self.current_page_change_state = False
        except:
            print('Size change err')

    def apply_theme(self, text):
        try:
            if text == "Material light":
                apply_stylesheet(app, theme='light_amber.xml')
            elif text == "Material dark":
                apply_stylesheet(app, theme='dark_amber.xml')
            self.params['theme'] = text
        except:
            print('Theme err')

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
        # Fdialog.setOptions(QFileDialog.ShowDirsOnly)
        workdir = Fdialog.getExistingDirectory(caption=self.lang[self.params['lang']]['save_win_title'])
        print(workdir)
        try:
            dt_string = datetime.now().strftime("%d-%m-%Y %H_%M_%S").split(' ')
            self.device_im.save(workdir + '/' + dt_string[0] + '-' + dt_string[1] + '.' + self.params['save_extension'],
                                self.params['save_mode'])
        except:
            self.image.setText('Save err')

    def scan(self):
        # print(self.device_list.currentIndex().row())
        # print(self.devices[self.device_list.currentIndex().row()])
        # try:
        try:
            dev = sane.open(self.devices[self.device_list.currentIndex().row()][0])
        except:
            print('Device open err')
            return
        # print(dev.get_parameters())
        # print(dev.get_options())
        try:
            dev.mode = self.params['mode']

        except:
            print('params mode err')
            print(self.params)
        try:
            dev.tl_x = 0
            dev.tl_y = 0
            dev.br_x = self.params['br_x']
            dev.br_y = self.params['br_y']
        except:
            print('params area err Using default')
            print(self.params)
        try:
            dev.resolution = self.params['dpi']
        except:
            print('Dpi err')
        try:
            if not self.current_scan_state:
                threat = threading.Thread(target=self.scan_thread, args=(dev,))
                threat.start()
            else:
                pass
        except:
            print('threat err')
        # except:
        #    self.image.setText('Err')

    def scan_thread(self, dev):
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

    def settings_save(self, current):
        self.params['save_mode'] = current.upper()
        self.params['save_extension'] = current.lower()

    def saves_setting(self):
        try:
            _ = {}
            _['params'] = self.params
            _['langs'] = self.lang
            location = os.getenv("HOME")
            with open(location + '/' + '.pyscan_setting.toml', 'w') as file:
                tomlkit.dump(_, file)
        except:
            print('Setting save err')

    def loads_setting(self, mode='0'):
        try:
            location = os.getenv("HOME")
            if mode == 'startup':
                try:
                    with open(location + '/' + '.pyscan_setting.toml', 'r') as file:
                        _ = tomlkit.parse(file.read())
                        self.params = _['params']
                        self.lang.update(_['langs'])
                        # self.apply_settings()
                except:
                    print('err load setting using default')
            else:
                try:
                    with open(location + '/' + '.pyscan_setting.toml', 'r') as file:
                        _ = tomlkit.parse(file.read())
                        self.params = _['params']
                        self.lang = _['langs']
                    self.apply_settings()
                except:
                    print('err load setting using default')
        except:
            print('Setting load err')

    def load_langs_from_file(self):
        try:
            fdialog = QFileDialog()
            fdialog.setMimeTypeFilters(['application/json'])
            url = fdialog.getOpenFileUrl(caption=self.lang[self.params['lang']]['load_lang_win_title'], filter='*.json')
            url = url[0].url().split('//')[1]
            with open(url, 'r') as file:
                loaded = json.load(file)
            self.lang.update(loaded)
            print(self.lang)
        except:
            print('lang load err')

    # def load_langs(self):
    # location = os.getenv("HOME")
    # try:
    # with open(location +'/' + '.pyscan_langs.json' , 'r') as file:
    # self.lang = json.load(file)
    # except:
    # with open(location + '/' + '.pyscan_langs.json', 'w') as file:
    # json.dump(self.lang , file)

    def apply_settings(self):
        try:
            self.pageSize.setCurrentText(self.params['size'])
            self.pageSize_custom_height.setValue(self.params['br_y'])
            self.pageSize_custom_width.setValue(self.params['br_x'])

            if self.params['mode'] == 'color':
                self.color_drop.setCurrentText(self.lang[self.params['lang']]['color_color'])
            else:
                self.color_drop.setCurrentText(self.lang[self.params['lang']]['color_grey'])
            self.dpi_drop.setCurrentText(str(self.params['dpi']))
            self.save_drop.setCurrentText(self.params['save_extension'])
            self.language_drop.setCurrentText(self.params['lang'])
            self.theme_drop.setCurrentText(self.params['theme'])
            self.apply_theme(self.params['theme'])
            if self.params['auto_settings']:
                self.auto_settings.setCheckState(Qt.CheckState(2))
            else:
                self.auto_settings.setCheckState(Qt.CheckState(0))
        except Exception as e:
            print(e)
            self.saves_setting()


class AddSize(QWidget):
    def __init__(self, func):
        super().__init__()
        self.func = func
        self.setWindowTitle('Add custom scan size')
        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.height = QLineEdit()
        self.height.setPlaceholderText('Height (cm)')
        self.width = QLineEdit()
        self.width.setPlaceholderText('Width (cm)')
        self.input_layout.addWidget(self.height)
        self.input_layout.addWidget(self.width)
        self.layout.addLayout(self.input_layout)

        self.apply_btn = QPushButton('Confirm')
        self.cancel_btn = QPushButton('Cancel')
        self.button_layout.addWidget(self.apply_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.apply_btn.clicked.connect(self.apply_size)
        self.cancel_btn.clicked.connect(self.cancel)

        self.setLayout(self.layout)

    def apply_size(self):
        self.close()
        self.func(self.height.text, self.width.text)

    def cancel(self):
        self.close()


def run():
    sane.init()
    window = MainWindow()
    window.loads_setting()
    window.update_list()
    window.show()
    window.resize(800, 500)
    window.setWindowTitle('PySpection')

    app.exec()
    if window.params['auto_settings']:
        window.saves_setting()
    sane.exit()


if __name__ == '__main__':
    run()
