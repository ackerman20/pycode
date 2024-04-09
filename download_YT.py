import os
from pytube import YouTube

list = []
id = str(input("請輸入要下載的影片ID : "))
url = 'https://www.youtube.com/watch?v=' + id
yt = YouTube(url)
a = str(input('是否要儲存在下載 : '))
if a == 'y' or a == 'Y':
    username = os.getlogin()
    path = 'C:/Users/' + username + '/Downloads'
elif a == 'n' or a == 'N':
    path = str(input("請輸入儲存位置 : "))
else:
    os._exit() 
spath = '儲存位置 : ' + path
print(spath)
print(yt.title)
ti = str(input("請輸入檔案名稱 : "))
dic = str(input("請輸入要儲存檔案類型(3=MP3 ; 4=MP4) : "))
if dic == '3':
    name = path+'/'+ ti + '.mp' + dic
    print('download...')
    yt.streams.filter().get_audio_only().download(name)
elif dic == '4':
    name = path+'/'+ ti + '.mp' + dic
    print('正在讀取該影片提供的所有畫質資訊中，請稍後...')
    for stream in yt.streams.all():
        a = stream.resolution
        if a not in list and a != None:
            list.append(a)
    print(list)
    p = str(input('請輸入要的影片畫質(輸入數字即可) : '))
    print('download...')
    p = p + 'p'
    yt.streams.filter().get_by_resolution(p).download(name)
else:
    os._exit()
print('ok!')