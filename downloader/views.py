from django.http import JsonResponse, HttpResponseBadRequest, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
from pydub import AudioSegment
import os
import json

@csrf_exempt
def extract_audio(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        video_url = data.get('video_url')
        if not video_url:
            return HttpResponseBadRequest('Missing the video link')
        
        try:
            yt = YouTube(video_url)
            video_title = yt.title
            audio_stream = yt.streams.filter(only_audio = True).first()

            mp4_file_path = audio_stream.download(output_path=settings.MEDIA_ROOT)
            mp3_file_path = mp4_file_path.replace('.mp4', '.mp3')

            audio = AudioSegment.from_file(mp4_file_path, format='mp4')
            audio.export(mp3_file_path, format='mp3')

            os.remove(mp4_file_path)

            res = FileResponse(open(mp3_file_path, 'rb'), as_attachment=True)
            res['Content-Disposition'] = f'attachment; filename="{video_title}.mp3"'
            return res
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('Only POST requests are allowed')

