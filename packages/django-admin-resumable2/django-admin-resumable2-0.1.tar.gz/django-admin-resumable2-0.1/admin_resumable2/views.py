import os

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.http import HttpResponse

from admin_resumable2.files import ResumableFile


def ensure_dir(f):
    d = os.path.dirname(f)
    os.makedirs(d, exist_ok=True)

def get_chunks_subdir():
    return getattr(settings, 'ADMIN_RESUMABLE_SUBDIR', 'admin_uploaded/')

def get_storage(request):
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        raise ImproperlyConfigured(
            'You must set settings.MEDIA_ROOT')
    
    media_url = getattr(settings, 'MEDIA_URL', None)
    if not media_url:
        raise ImproperlyConfigured(
            'You must set settings.MEDIA_URL')
        
    if request.method == 'POST':
        field_name = request.POST['field_name']
    else:
        field_name = request.GET['field_name']

    chunks_subdir = get_chunks_subdir() 
    location = os.path.join(media_root, chunks_subdir)
    location = os.path.join(location, field_name)
    ensure_dir(location)

    url_path = os.path.join(chunks_subdir, field_name) 

    storage_class_name = getattr(
        settings,
        'ADMIN_RESUMABLE_STORAGE',
        'django.core.files.storage.FileSystemStorage'
    )
    return get_storage_class(storage_class_name)(
        location=location, base_url=url_path)

@staff_member_required
def admin_resumable(request):
    storage = get_storage(request)

    if request.method == 'POST':
        chunk = request.FILES.get('file')
        r = ResumableFile(storage, request.POST)

        if not r.chunk_exists:
            r.process_chunk(chunk)

        if r.is_complete:
            actual_filename = storage.save(r.filename, r.file)
            r.delete_chunks()
            return HttpResponse(storage.url(actual_filename))
        
        return HttpResponse('chunk uploaded')
    
    elif request.method == 'GET':
        r = ResumableFile(storage, request.GET)

        if not r.chunk_exists:
            return HttpResponse('chunk not found', status=404)
        
        if r.is_complete:
            actual_filename = storage.save(r.filename, r.file)
            r.delete_chunks()
            return HttpResponse(storage.url(actual_filename))
        
        return HttpResponse('chunk exists')
