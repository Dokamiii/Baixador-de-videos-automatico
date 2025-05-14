import yt_dlp

# Teste com um vídeo simples do YouTube
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Link de teste

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'video_teste/%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
