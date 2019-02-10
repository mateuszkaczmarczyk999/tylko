from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.http import JsonResponse
from webapp.backend.BoxFactory import BoxFactory
from webapp.backend.GroupBuilder import GroupBuilder

def polls_list(request):
    path = 'webapp/backend/resources/A.csv'
    factory = BoxFactory(path)
    factory.import_boxes_from_csv()
    all_boxes = factory.get_boxes

    group_builder = GroupBuilder()
    group_builder.build_groups(all_boxes)

    result = group_builder.get_json_file()
    return JsonResponse(result)

urlpatterns = [
    url(r'^$', 
        TemplateView.as_view(template_name='index.html'),      
        name='uHome'
    ),
    url(r'^admin/', admin.site.urls),
    path("boxes/", polls_list, name="polls_list"),
]

urlpatterns += staticfiles_urlpatterns()