from django.http import JsonResponse, HttpResponseBadRequest, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
from pydub import AudioSegment
from io import BytesIO
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

            destination_path = os.path.join(settings.MEDIA_ROOT, 'audios')
            mp4_file_path = audio_stream.download(output_path=destination_path)
            mp3_file_path = mp4_file_path.replace('.mp4', '.mp3')

            audio = AudioSegment.from_file(mp4_file_path, format='mp4')
            audio.export(mp3_file_path, format='mp3')

            os.remove(mp4_file_path)

            with open(mp3_file_path, 'rb') as audio_file:
                audio_file_content = audio_file.read()

            os.remove(mp3_file_path)

            audio_bytes = BytesIO()
            audio_bytes.write(audio_file_content)
            audio_bytes.seek(0)
            
            res = FileResponse(audio_bytes, as_attachment=True)
            res['Content-Disposition'] = f'attachment; filename="{video_title}.mp3"'
            res['Content-Type'] = 'audio/mpeg'
            return res
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('Only POST requests are allowed')

