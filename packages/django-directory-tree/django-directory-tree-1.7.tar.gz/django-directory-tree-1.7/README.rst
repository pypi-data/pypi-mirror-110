# Directory-Tree

Directory Tree is a Django app to see all directory in media folder.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "directory_tree" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'directory_tree',
    ]

2. Add MEDIA_URL and MEDIA_ROOT to your setting.py setting like this (Optional)::

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    MEDIA_URL = '/media/'
    MEDIA_ROOT = str(BASE / 'media')

3. Add media path in your project urls.py like this (Optional)::

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

4. Option if you want to see file have in a database ? setting like this in setting.py::
    
    DIRECTORY_TREE_MODEL_USE = True # default False
    DIRECTORY_TREE_MODEL = {
        TABLE_NAME: [list_field],
    }

5. Include the directorty tree URLconf in your project urls.py like this::

    path('directory_tree/', include('directory_tree.urls')),


6. Start the development server and visit http://127.0.0.1:8000/admin/
   to login by admin user

7. Visit http://127.0.0.1:8000/directory_tree/ to participate in the directory tree.