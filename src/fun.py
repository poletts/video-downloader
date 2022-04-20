"""
Collection of functions interacting with pytube library
"""

import os

from pytube import YouTube

def import_video(link: str, path: str):
    """
    Donwload video from link to path

    Parameters:
    ----------
    link:str
        url with link for youTube video
    path: str
        file path for download video
        
    Return:
    ------
    None
    """
    # Stablish connection
    yt=YouTube(link);    
    # Get the highest resolution    
    ys=yt.streams.get_highest_resolution()
    #download
    ys.download(path)    
    
def check_youtube_url(url:str) -> bool:
    """
    Check if the url is accessible by pytube.YouTube module

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

def get_video_info(link:str) -> str:
    """
    Retrieve video informations

    Parameters:
    -----------
    link: str
        url with link for youTube video

    Return:
    -------
    txt: str
        string with information about the video 
    """
    yt=YouTube(link)
    txt = '\nTitle: ' + yt.title + '\n' \
          'Author: ' + yt.author + '\n' \
          'Duration: ' + str(yt.length) +' seconds' + '\n' \
          'Pubished on ' + yt.publish_date.strftime("%B %d, %Y") + '\n' \
          'Views: %d' % yt.views

    return ''.join(txt)

if __name__ == "__main__":

    # Get current path
    path=os.path.dirname(os.path.abspath(__file__))
    
    # Select link
    link=input('Insert video link:')
    
    # Import Video
    import_video(link, path)

    print('Video sucessfully downloaded')
