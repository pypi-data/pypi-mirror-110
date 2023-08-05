from django.conf.urls.static import static
from django.urls import path
from pathlib import Path as Pathlib

from . import views

urlpatterns = [
    path('', views.DirectoryTreeView.as_view(), name='directory_tree'),
    path('get/', views.ListFileOrFolder.as_view(), name='list_file_folder'),
]

BASE_DIR = Pathlib(__file__).resolve().parent
STATIC_DIRECTORY_TREE_URL = 'static/'
STATIC_DIRECTORY_TREE_ROOT = str(BASE_DIR / 'templates/directory_tree/static')
urlpatterns += static(STATIC_DIRECTORY_TREE_URL, document_root=STATIC_DIRECTORY_TREE_ROOT)
