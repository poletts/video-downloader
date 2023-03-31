"""
User interface download of YouTube videos
"""
import sys, os

if __name__ == "__main__":
    sys.path.append(os.path.abspath('.'))

from PySide6.QtWidgets import (QApplication, QWidget, QFileDialog, QStatusBar,
                               QVBoxLayout, QHBoxLayout,                                
                               QLabel, QPushButton, QLineEdit)
from PySide6.QtCore import Signal

import fun

custom_style_sheet = """
    QWidget {
        background-color: #282828;
        font-size: 14px;
        color: #ffffff;
    }

    QLineEdit{
        background-color: #ff0000;
        color: #ffffff;
        border-radius: 5px;
        padding: 2px;
        alignment: AlignCenter;
    }

    QPushButton{
        background-color: white;
        qproperty-alignment: AlignCenter
        padding: 5px;
        border-radius: 5px;
    }

"""

class Main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video Downloader")
        self.central_widget = CentralFrame(self)
        self.status_bar = StatusBar(self)
        self.setup_layout()
        self.resize(600, 400)  
        # connect signal in CentralFrame to slot in StatusBar
        self.central_widget.send_message.connect(self.status_bar.showMessage)
    
    def setup_layout(self):
        lay = QVBoxLayout()
        lay.addWidget(self.central_widget)
        lay.addWidget(self.status_bar)
        lay.setSpacing(0)
        lay.setContentsMargins(0,0,0,0)        
        self.setLayout(lay)      
        self.setStyleSheet(custom_style_sheet)    
        # with open('src\style.qss',"r") as f:            
        #     custom_style_sheet = f.read()
        #     self.setStyleSheet(custom_style_sheet)        


class CentralFrame(QWidget):
    
    send_message = Signal(str, int)

    def __init__(self, parent= None):
        super().__init__(parent)
        self.resize(600, 300)
        # Instances
        self.default_path = 'C:/Users/install/Downloads'
        # Widgets
        self.path = QLineEdit(self.default_path)
        self.open_explorer = QPushButton('Open')
        self.video_link = QLineEdit()
        self.download_btn = QPushButton('Download')
        self.video_info = QLabel()        
        self.setup_layout()
        # Connections
        self.open_explorer.clicked.connect(self.select_folder_path)
        self.video_link.editingFinished.connect(self.display_info)
        self.download_btn.clicked.connect(self.download_fun)

    def setup_layout(self):
        folder = QHBoxLayout()
        folder.addWidget(QLabel('Destination Folder: '))
        folder.addWidget(self.path)
        folder.addWidget(self.open_explorer)

        video = QHBoxLayout()
        video.addWidget(QLabel('Enter video url: '))
        video.addWidget(self.video_link)
        video.addWidget(self.download_btn)

        lay = QVBoxLayout()
        lay.addLayout(folder)
        lay.addLayout(video)
        lay.addWidget(self.video_info)
        lay.setSpacing(0)
        lay.addStretch(1)
        self.setLayout(lay)

    def select_folder_path(self):
        """Open dialog to select folder path"""

        file_path = QFileDialog.getExistingDirectory(self, 'Please select path', self.default_path)
        if file_path == '':
            self.path.setText(self.default_path)
        else:
            self.path.setText(file_path)  
    
    def display_info(self):
        """Display video info on screen"""

        link = self.video_link.text()
        if fun.check_youtube_url(link):
            txt = fun.get_video_info(link)
            self.video_info.setText(txt)
            self.send_message.emit('URL provided is valid', 5000)         
        else:
            self.send_message.emit('Invalid url', 5000)

    def download_fun(self):

        link = self.video_link.text()
        path = self.path.text()

        if fun.check_youtube_url(link):        
            self.send_message.emit('Download started...', 5000)            
            fun.import_video(link, path)
            self.video_info.setText('')
            self.send_message.emit('Video sucessfully downloaded', 5000)
        else:
            self.send_message.emit('Invalid url', 5000)  


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Display copyright and Version
        self.lic = QLabel(self)
        self.lic.setText("\xa9 2022 poletts | v 0.0.2 ")
        self.addPermanentWidget(self.lic)
        self.showMessage('Welcome', 3000)
    
    def update(self, text:str = None) -> None:
        if text is not None:
            self.showMessage(text, 3000)

    def clean(self):
        self.clearMessage()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec())
