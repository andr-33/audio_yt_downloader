from django.http import FileResponse
from django.conf import settings
import os

class DeleteUsedAudioFileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, FileResponse) and '/downloader/extract-audio' in request.path:
            audio_directory = os.path.join(settings.MEDIA_ROOT, 'audios')
            if os.path.exists(audio_directory) and os.path.isdir(audio_directory):
                for file_name in os.listdir(audio_directory):
                    file_path = os.path.join(audio_directory, file_name)
                    if os.path.exists(file_path):
                        os.remove(file_path)

        return response
