from django.urls import path

from . import views

app_name = 'server'
urlpatterns = [
    path("<uuid:ChecklistTemplateID_Value>", views.checklist_detail, name="checklisttemplatemaintainer-detail"),
    path("<uuid:ChecklistTemplateID_Value>/json", views.checklist_json, name="checklisttemplatemaintainer-json"),
]
