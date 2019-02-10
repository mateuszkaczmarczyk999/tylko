from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.http import JsonResponse
from webapp.backend.BoxFactory import BoxFactory
from webapp.backend.GroupBuilder import GroupBuilder
from django.core import serializers


def polls_list(request):
    path = 'webapp/backend/resources/toWeb.csv'
    factory = BoxFactory(path)
    factory.import_boxes_from_csv()
    all_boxes = factory.get_boxes

    group_builder = GroupBuilder()
    group_builder.build_groups(all_boxes)

    all_json_boxes = factory.get_all_json_boxes()
    groups = group_builder.get_all_json_groups()
    result = {"all": all_json_boxes, "thickness": groups[0], "attached": groups[1]}
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