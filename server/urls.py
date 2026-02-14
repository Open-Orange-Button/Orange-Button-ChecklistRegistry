from django.urls import path

from . import views

app_name = 'checklisttemplate'
urlpatterns = [
    path('', views.index, name='index'),
    path('how-to-contribute', views.how_to_contribute, name='how-to-contribute'),
    path('<uuid:ChecklistTemplateID_Value>', views.checklist_detail, name='detail'),
    path('<uuid:ChecklistTemplateID_Value>/json', views.checklist_json, name='json'),
]
