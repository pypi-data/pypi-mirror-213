django-admin-resumable2
=========================

django-admin-resumable2 is a django app to allow you to upload large files from within the django admin site.

Screenshot
----------


Installation
------------

    * pip install django-admin-resumable2
    * Add ``admin_resumable2`` to your ``INSTALLED_APPS``
    * Add ``path('', include('admin_resumable2.urls')),`` to your urls.py
    * Add a model field eg: ``from admin_resumable2.fields import ModelAdminResumableFileField``

::

    class Foo(models.Model):
        title = models.CharField(max_length=200)
        file = ModelAdminResumableFileField(upload_to='foo/')

        # use below code to change path of resumable
        def save(self, force_insert=None, force_update=None, using=None, update_fields=None):
            old_path = self.file.path  # Get the current old path
            file_name = os.path.basename(old_path) # get file name

            upload_to_method = Foo._meta.get_field('file').orig_upload_to # Get the original upload to path
            if type(upload_to_method) == str:
                orig_upload_to = upload_to_method + file_name

            else:
                orig_upload_to = upload_to_method(self, file_name)

            new_path = os.path.join(settings.MEDIA_ROOT, orig_upload_to)  # Create the original path

            directory = os.path.dirname(new_path)
            os.makedirs(directory, exist_ok=True)

            if new_path != old_path:
                
                while True:
                    file_name, file_extension = os.path.splitext(new_path)
                    random_value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
                    new_path = file_name + '_' + random_value + file_extension          

                    if not os.path.exists(new_path):
                        orig_upload_to = new_path.replace(str(settings.MEDIA_ROOT), '')
                        break              

                shutil.move(old_path, new_path)
                self.file.name = orig_upload_to

            return super().save(force_insert, force_update, using, update_fields)


Optionally:

    * Set ``ADMIN_RESUMABLE_SUBDIR``, default is ``'admin_uploaded'``
    * Set ``ADMIN_RESUMABLE_CHUNKSIZE``, default is ``"1*1024*1024*5"``
    * Set ``ADMIN_RESUMABLE_STORAGE``, default is ``'django.core.files.storage.FileSystemStorage'`` 

Compatibility
-------------
{py37, py38, py310}-django{4.* above}
