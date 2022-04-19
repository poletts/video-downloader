# -*- coding: utf-8 -*-
"""

demo code from https://pytube.io/en/latest/

"""

import os
from pytube import YouTube

def import_video(link, path):
    
    # Stablish connection
    yt=YouTube(link);    
    print('title: ',yt.title)    
    print('size: ',yt.length,'seconds')

    # Get the highest resolution    
    ys=yt.streams.get_highest_resolution()
    
    #download
    ys.download(path)    
    
    print('Video downloaded')


# Get current path
path=os.path.dirname(os.path.abspath(__file__))
# Select link
link=input('Insert video link:')
# Import Video
import_video(link,path)

