"""
User interface for quick download of YouTube videos
"""
import sys

from pytube import YouTube
from PySide6.QtWidgets import (QApplication, QWidget, QFileDialog, QStatusBar,
                               QVBoxLayout, QHBoxLayout,                                
                               QLabel, QPushButton, QLineEdit)
from PySide6.QtCore import Signal


class Main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("YouTube Downloader")
        self.central_widget = CentralFrame(self)
        self.status_bar = StatusBar(self)
        self.setup_layout()
        self.resize(600, 400)  
        # connect signal in CentralFrame to slot in StatusBar
        self.central_widget.send_message.connect(self.status_bar.showMessage)
        self.show()
    
    def setup_layout(self):
        lay = QVBoxLayout()
        lay.addWidget(self.central_widget)
        lay.addWidget(self.status_bar)
        lay.setSpacing(0)
        lay.setContentsMargins(0,0,0,0)        
        self.setLayout(lay)
        custom_style_sheet = """
        QWidget{background-color: white;
                padding: 2px}

        QLineEdit={
                   background-color: lightblue;
                   }
        """
        self.setStyleSheet(custom_style_sheet)


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

        if check_youtube_url(link):
            yt = YouTube(link)

            txt = '\nTitle: ' + yt.title + '\n' \
                  'Author: ' + yt.author + '\n' \
                  'Duration: ' + str(yt.length) +' seconds' + '\n' \
                  'Pubished on ' + yt.publish_date.strftime("%B %d, %Y") + '\n' \
                  'Views: %d' % yt.views
            self.video_info.setText(''.join(txt))   
            self.send_message.emit('URL provided is valid', 5000)         
        else:
            self.send_message.emit('Invalid url', 5000)

    def download_fun(self):

        link = self.video_link.text()
        path = self.path.text()

        if check_youtube_url(link):
            self.send_message.emit('Download started...', 5000)            
            yt=YouTube(link)
            # Get the highest resolution    
            ys=yt.streams.get_highest_resolution()    
            #download
            ys.download(path)
            self.video_info.setText('')
            self.send_message.emit('Video sucessfully downloaded', 5000)
        else:
            self.send_message.emit('Invalid url', 5000)  


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        # License
        self.lic = QLabel(self)
        self.lic.setText("(C) 2022 Jean Poletto ")
        self.addPermanentWidget(self.lic)
        # Version
        self.version = QLabel(self)
        self.version.setText(" v0.0.1 ")
        self.addPermanentWidget(self.version)        
        self.showMessage('Welcome', 3000)
    
    def update(self, text:str = None) -> None:
        if text is not None:
            self.showMessage(text, 3000)

    def clean(self):
        self.clearMessage()


def check_youtube_url(url:str) -> bool:
    """
    Check wheter an url is accessible by pytube.YouTube module

    Parameters:
    -----------
    url : str
        url for YouTube video

    Return:
    -------
    bool
        True if url is acessible
        False if url is not accessible
    """
    try:
        YouTube(url)
        status = True
    except:
        status = False
    return status


if __name__ == "__main__":

    app = QApplication(sys.argv)

    main = Main()

    sys.exit(app.exec())
