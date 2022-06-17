from logging import root
from PySide2.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QTabWidget,
    QToolButton
)
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import QUrl, Qt
from webwidgets import WebEngine
from research import TopoBusca, BuscaUrl
from addtabs import tabs
from starttabs import start
import sys
import time
import AutoUpdate
import os
import urllib.error
from getpass import getuser
import tkinter as tk

root = tk.Tk()
root .geometry ("300x300")
tk.Label(root,text="Version 1.0").pack()
tk.mainloop()


try:
    AutoUpdate.set_url("https://raw.githubusercontent.com/weedenek/Weedy-Browser/main/version.txt") # .txt dosyasının raw linki/raw link of the .txt file
    AutoUpdate.set_download_link("https://raw.githubusercontent.com/Arif-Helmsys/Testing/main/exp.py") # .txt dosyasını okuttuktan sonra indirmesini istediğimiz bir program
    AutoUpdate.set_current_version("0.1") # .txt ye yazdığınız mevcut sürüm dışında herhangi bir sürüm numarası yazabiliriz
    print(AutoUpdate.is_up_to_date()) # Üstte yazdığımız sürüm .txt de yazılan sürümle uyuşmuyorsa yani güncel değilse False, Güncel ise True olarak ekrana yazdırır

    if not AutoUpdate.is_up_to_date(): # Eğer güncel değil ise
        print("Stahování začíná...")
        time.sleep(1)
        print("stahování...")
        print(AutoUpdate.get_latest_version()) # .txt de ki sürüm  numarasını okuyup ekrana yazdırıyor
        if not os.path.exists("C:\\Users\\"+getuser()+"\\Desktop\\Updater"): # Masaüstünde Updater klasörü yoksa
            print("Složka vytvořena")
            os.makedirs("C:\\Users\\"+getuser()+"\\Desktop\\Updater") # Masaüstüne Updater klasörünü oluştur
            AutoUpdate.download("C:\\Users\\"+getuser()+"\\Desktop\\Updater\\updater.py") # Oluşturulan klasöre updater adını verdiğimiz .py dosyasını indir

        else: # Şayet Böyle bir klasör varsa
            AutoUpdate.download("C:\\Users\\"+getuser()+"\\Desktop\\Updater\\updater.py") # updater adını verdiğimiz .py dosyasını Önceden var olan klasöre indir

    elif AutoUpdate.is_up_to_date(): # Program Güncel ise
        print("Vaše verze je aktualizována!")
except urllib.error.URLError:
    print("Zkontrolujte připojení k internetu!")


class Browser(QTabWidget):
    ObjectWidgets = dict() # dicionario com todos os widgets
    CounterTabs = 0 # registrador de abas abertas

    def __init__(self):
        super(Browser, self).__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.more = QToolButton()
        self.more.setText('+')
        self.more.clicked.connect(self.start)
        self.more.setStyleSheet(
            '''border: none;
            padding: 5px;
            color: #fff;
            background: teal;'''
        )
        self.setCornerWidget(
            self.more, Qt.Corner.TopLeftCorner
        )
        self.tabCloseRequested.connect(
            self.removeJanela
        )
        self.start()

    # inicia as abas ///////////////////////////////////////////////////////////////////

    def start(self, url=None):
        self.URL = url
        if not self.URL:
            try:
                self.URL = sys.argv[1].replace('"', '')
            except IndexError:
                self.URL = 'https://duckduckgo.com'
        start(self, self.ObjectWidgets)       

    # busca o que foi digitado na barra de pesquisa depende de <pesquisa>

    def busca(self):
        BuscaUrl(self, self.ObjectWidgets)

    # remove a janela ao pressionar o botão de fechar aba

    def removeJanela(self, index):
        if self.count() > 1:
            self.removeTab(index)
            self.ObjectWidgets['webengine' + str(index)].deleteLater()
            self.CounterTabs -= 1

    # aguarda a pagina terminar de carregar e adiciona a aba solicitada
    # depende do modulo <adicionarabas> -> Abas

    def addtabs(self):
        tabs(self, self.ObjectWidgets)
        self.CounterTabs = self.count()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap('img/icon.png')))
    app.setApplicationName('Weedy Browser')
    app.setApplicationDisplayName('Weedy Browser')
    tabVar = Browser()
    tabVar.setWindowTitle('Weedy Browser')
    tabVar.showMaximized()
    tabVar.show()
    sys.exit(app.exec_())
