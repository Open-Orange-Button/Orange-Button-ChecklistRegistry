from django.urls import path

from . import views

app_name = 'server'
urlpatterns = [
    path("", views.index, name="checklisttemplate-index"),
    path("<uuid:ChecklistTemplateID_Value>", views.checklist_detail, name="checklisttemplate-detail"),
    path("<uuid:ChecklistTemplateID_Value>/json", views.checklist_json, name="checklisttemplate-json"),
]
