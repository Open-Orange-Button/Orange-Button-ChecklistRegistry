from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import server.models


def index(request):
    return HttpResponse('hi')


def checklist_detail(request, ChecklistTemplateID_Value):
    checklist_template = get_object_or_404(server.models.ChecklistTemplate, ChecklistTemplateID_Value=ChecklistTemplateID_Value)
    sections_and_questions = defaultdict(list)
    for question in checklist_template.Questions.all().order_by('DisplaySeqNumber_Value'):
        sections_and_questions[question.SectionName_Value].append(question)
    print(sections_and_questions)
    return render(
        request,
        'server/checklist_detail.html',
        dict(
            checklist_template=checklist_template,
            sections_and_questions=dict(sections_and_questions),
        ),
    )
