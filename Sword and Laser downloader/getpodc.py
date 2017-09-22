#!/usr/bin/env python
import re
import string
import requests
import os.path
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen



def main():

    # relative to this script's location
    last_episode_filename = "last_watched_ep.txt"
    download_folder = "/Disks/D:/Downloads/Podcasts"

    directory = os.path.dirname(os.path.realpath(__file__))
    last_episode_filepath = os.path.join(directory, last_episode_filename)

    if len(sys.argv) == 3 and sys.argv[1] == '-le':
        with open(last_episode_filepath, 'w') as last_watched_file:
            last_watched_file.write(sys.argv[2])
        print('last episode number is now %s' % sys.argv[2])
        return

    

    with open(last_episode_filepath) as data_file:
        try:
            last_episode_n = int(data_file.readline())
        except ValueError:
            print('script data file does not contain integer number!')
            exit()

    r = requests.get('http://swordandlaser.com/')
    soup = BeautifulSoup(r.text, "html.parser")
    
    # first all post tags on the page - tag containing all info in a post also with link to download
    # they are sorted from most to less recent
    post_tags = soup.find_all(class_ = 'post')

    # list of tuples(url , episode filename)
    eps_to_download = list()
    # remember that to update the data
    ep_number_changed = False

    for i in range(len(post_tags)):

        post_title = get_post_title(post_tags[i])
        if (str(last_episode_n) in post_title) or (i == (len(post_tags) - 1)):
            # found last watched episode
            if( i == 0):
                print("No new content(")
            else:

                print("New episodes found:")
                for URL, name in eps_to_download:
                    print(name)

                answer = input('Download them all? y/n\n')
                if(answer == 'y'):
                    download_episodes(eps_to_download, download_folder, 10)
                    ep_number_changed = True
                    
            break
        
        else:
            #add URL and filename of this ep to the list 
            eps_to_download.append((get_episode_URL(post_tags[i]), re.search("#.*", post_title).group(0)))


    if ep_number_changed:
        # update last watched ep number
        last_watched_ep_n = re.search("# *([0-9]*)", get_post_title(post_tags[0]))
        with open(last_episode_filepath, 'w') as last_watched_file:
            last_watched_file.write(last_watched_ep_n.group(1))
        
         
    
def get_post_title(post):
    '''input - post tag - 
    returns : true if it's title equals title of last watched episode'''

    post_title = post.find(class_ = 'entry-title')

    remove_chars_dict = {ord(c):None for c in "\/."}
    title_str = str(post_title.string).translate(remove_chars_dict)
    
    return title_str


def get_episode_URL(post):
    download_URL_tag = post.find('a', string = re.compile('Download'))
    if(download_URL_tag is None):
        raise Exception('''no \'a\' tag with string \"Download directly here!\" 
        was found in a post with name''' + get_post_title(post))
    download_URL = download_URL_tag['href']
    return download_URL
            

def download_episodes(eps_to_download, folder, percent_to_show):
    ''' downloads all files from URLs in eps_to_download to folder.
    filenames are created by adding .mp3 to the names
    eps_to_download - list of tuples(URL, name)'''

    ensure_folder_exists(folder)

    for URL, name in eps_to_download:
        print('Downloading episode :\n' + name)
        path = os.path.join(folder, name + '.mp3') 
        
        download_file_from_URL(URL, path, percent_to_show)
    

def download_file_from_URL(URL, dest, percent_step_to_show):
    
    responce = requests.get(URL, stream = True)
    responce.raise_for_status()
    
    # number of bytes to download
    total_length = float(responce.headers.get('content-length'))
    downloaded_length = 0.0
    next_progress_step_to_show = 0.0
    
    with open(dest, 'wb') as f:
        for block in responce.iter_content(1024):
            
            f.write(block)
            downloaded_length += len(block)
            progress_percent = (downloaded_length / total_length) * 100
        
            # print progress only once in a while
            if progress_percent >= next_progress_step_to_show:
                
                print("%.2f %%" %  next_progress_step_to_show)
                next_progress_step_to_show += percent_step_to_show
                
        
        print("Done!")
        
        
def ensure_folder_exists(folder):
    from os import makedirs
    
    if(os.path.exists(folder)):
        return
    
    makedirs(folder)

if __name__ == '__main__':
    main()
