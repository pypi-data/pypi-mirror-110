import json

from django.views.generic import View
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse

from .utils.directory_tree import DirectoryTree
from .utils.get_list_folder import GetListInFolder
from .utils.decorators import super_user_active_only


@method_decorator(login_required, name='dispatch')
@method_decorator(super_user_active_only, name='dispatch')
class DirectoryTreeView(TemplateView):

    template_name = 'directory_tree/directory_tree_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        media_root = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        if not media_root or not media_url:
            context['error'] = "error : undefind MEDIA_ROOT or MEDIA_URL in setting"
            return context
        return context

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(super_user_active_only, name='dispatch')
class ListFileOrFolder(View):

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
        except Exception as err:
            print("directory => {}".format(err))
            print(request.body)
            body = json.loads(request.body.decode('utf-8'))

        if not 'path_folder' in body:
            return JsonResponse({'error':'no key path_folder'})
        
        list_dir = GetListInFolder(body['path_folder']).get()
        return JsonResponse({'list_folder': list_dir})