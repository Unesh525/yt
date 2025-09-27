import time

from django.http import HttpResponse
from django.shortcuts import render
from pytubefix import YouTube
from pathlib import Path

from pytubefix.cli import on_progress

# Create your views here.
def index(request):
    if request.method == "POST":
        url = request.POST.get('url')
        print(url)
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            audio_stream = yt.streams.filter(only_audio=True).first()

            title = yt.title
            duration = yt.length
            minutes = duration // 60
            seconds = duration % 60
            timing = f"Duration :{minutes}:{seconds}"
            thumbnail = yt.thumbnail_url
            audio_file_size_bytes = audio_stream.filesize

            video_file_size_bytes = stream.filesize

            video_file_size_mb = video_file_size_bytes / (1024 * 1024)
            audio_file_size_mb = audio_file_size_bytes / (1024 * 1024)

            video_size = f"{video_file_size_mb:.2f} MB"
            audio_size = f"{audio_file_size_mb:.2f} MB"


            return render(request, 'index.html',{'url':url,'title':title,'duration':timing,'thumbnail':thumbnail,'video_size':video_size,'audio_size':audio_size})
        except Exception as e:
            print(e)
            msg = "Url Not Found"
            return render(request,'index.html',{'msg':msg})

    else:
        return render(request, 'index.html')



def downloadmp4(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        print(url)
        for i in range(1):
            try:
                yt = YouTube(url)
                stream = yt.streams.get_highest_resolution()
                downloads_path = str(Path.home() / "Downloads")
                stream.download(downloads_path)
                msg = "Download Complete"


                break
            except Exception as e:
                print(f"Attempt {i + 1} failed: {e}")
                time.sleep(5)
                msg = "not downloading"
        return render(request, 'index.html',{'msg':msg})

    else:
        return render(request, 'index.html')


def downloadmp3(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        print(url)
        for i in range(1):
            try:
                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                downloads_path = str(Path.home() / "Downloads")
                print(downloads_path)
                audio_stream.download(downloads_path)
                msg = "Download Complete"
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed: {e}")
                time.sleep(5)
                msg = "not downloading"
        return render(request, 'index.html',{'msg':msg})

    else:
        return render(request, 'index.html')

