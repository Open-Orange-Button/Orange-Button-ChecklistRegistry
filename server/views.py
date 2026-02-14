import ast
from collections import defaultdict
import datetime
import itertools

from django.core import paginator
import django.db.models
import django.forms as forms
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse

import ob_taxonomy.models as ob_models
import server.models as models


def question_to_form_field(question: models.Question):
    match question.AnswerType_Value:
        case models.AnswerTypeItemTypeEnum.Text:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='CharField', ctx=ast.Load()),
                args=[
                ],
                keywords=[
                    ast.keyword(arg='label', value=ast.Constant(value=question.QuestionLabel_Value)),
                    ast.keyword(arg='required', value=ast.Constant(value=question.RequirementLevel_Value == models.RequirementLevelItemTypeEnum.Required)),
                    ast.keyword(arg='widget', value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='TextInput', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ))
                ],
            )
        case models.AnswerTypeItemTypeEnum.EnumeratedSingle:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='ChoiceField', ctx=ast.Load()),
                args=[
                ],
                keywords=[
                    ast.keyword(arg='label', value=ast.Constant(value=question.QuestionLabel_Value)),
                    ast.keyword(arg='required', value=ast.Constant(value=question.RequirementLevel_Value == models.RequirementLevelItemTypeEnum.Required)),
                    ast.keyword(arg='choices', value=ast.List(
                        elts=[
                            ast.Tuple(elts=[ast.Constant(value=a.id), ast.Constant(value=a.Value)], ctx=ast.Load())
                            for a in question.AnswerOptions.all()
                        ],
                        ctx=ast.Load(),
                    )),
                    ast.keyword(arg='widget', value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='Select', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ))
                ],
            )
        case models.AnswerTypeItemTypeEnum.EnumeratedMultiple:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='MultipleChoiceField', ctx=ast.Load()),
                args=[
                ],
                keywords=[
                    ast.keyword(arg='label', value=ast.Constant(value=question.QuestionLabel_Value)),
                    ast.keyword(arg='required', value=ast.Constant(value=question.RequirementLevel_Value == models.RequirementLevelItemTypeEnum.Required)),
                    ast.keyword(arg='choices', value=ast.List(
                        elts=[
                            ast.Tuple(elts=[ast.Constant(value=a.id), ast.Constant(value=a.Value)], ctx=ast.Load())
                            for a in question.AnswerOptions.all()
                        ],
                        ctx=ast.Load(),
                    )),
                    ast.keyword(arg='widget', value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='SelectMultiple', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ))
                ],
            )
        case models.AnswerTypeItemTypeEnum.Numeric:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='DecimalField', ctx=ast.Load()),
                args=[
                ],
                keywords=[
                    ast.keyword(arg='label', value=ast.Constant(value=question.QuestionLabel_Value)),
                    ast.keyword(arg='required', value=ast.Constant(value=question.RequirementLevel_Value == models.RequirementLevelItemTypeEnum.Required)),
                    ast.keyword(arg='localize', value=ast.Constant(value=False)),
                    ast.keyword(arg='widget', value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='NumberInput', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ))
                ],
            )
        case models.AnswerTypeItemTypeEnum.Date:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='DateField', ctx=ast.Load()),
                args=[
                ],
                keywords=[
                    ast.keyword(arg='label', value=ast.Constant(value=question.QuestionLabel_Value)),
                    ast.keyword(arg='required', value=ast.Constant(value=question.RequirementLevel_Value == models.RequirementLevelItemTypeEnum.Required)),
                    ast.keyword(arg='widget', value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='SelectDateWidget', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ))
                ],
            )
        case models.AnswerTypeItemTypeEnum.URL:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='URLField', ctx=ast.Load()),
                args=[
                ],
                keywords=[
                    ast.keyword(arg='label', value=ast.Constant(value=question.QuestionLabel_Value)),
                    ast.keyword(arg='required', value=ast.Constant(value=question.RequirementLevel_Value == models.RequirementLevelItemTypeEnum.Required)),
                    ast.keyword(arg='widget', value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='URLInput', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ))
                ],
            )
        case models.AnswerTypeItemTypeEnum.File:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='FileField', ctx=ast.Load()),
                args=[
                ],
                keywords=[
                    ast.keyword(arg='label', value=ast.Constant(value=question.QuestionLabel_Value)),
                    ast.keyword(arg='required', value=ast.Constant(value=question.RequirementLevel_Value == models.RequirementLevelItemTypeEnum.Required)),
                    ast.keyword(arg='widget', value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='ClearableFileInput', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ))
                ],
            )
        case _:
            raise ValueError(f'question_to_form_field: Unsupported answer type "{question.AnswerType_Value}"')


def generate_question_form(questions):
    klass = ast.Module(body=[
        ast.ImportFrom(module='django', names=[ast.alias(name='forms')], level=0),
        ast.ClassDef(
            name='Question',
            bases=[ast.Attribute(value=ast.Name(id='forms', ctx=ast.Load()), attr='Form', ctx=ast.Load())],
            keywords=[],
            body=[
                ast.Assign(
                    targets=[ast.Name(id=f'q_{i}', ctx=ast.Store())],
                    value=question_to_form_field(question)
                )
                 for i, question in enumerate(questions)
            ],
            decorator_list=[],
        ),
    ])
    klass = ast.fix_missing_locations(klass)
    print(ast.unparse(klass))
    temp = {}
    exec(compile(klass, '<ast>', 'exec'), temp)
    return temp['Question']


def index(request):
    checklist_template = models.ChecklistTemplate.objects.get(
        ChecklistTemplateMaintainer__ChecklistTemplateMaintainerName_Value='Blu Banyan',
        ChecklistTemplateName_Value='Residential Installation'
    )
    return HttpResponseRedirect(reverse('checklisttemplate:detail', args=[checklist_template.ChecklistTemplateID_Value]))


def how_to_contribute(request):
    return render(request, 'server/how_to_contribute.html')


def maintainer_detail(request, ChecklistTemplateMaintainerID_Value):
    maintainer = get_object_or_404(models.ChecklistTemplateMaintainer, ChecklistTemplateMaintainerID_Value=ChecklistTemplateMaintainerID_Value)
    return render(
        request,
        'server/maintainer_detail.html',
        dict(
            maintainer=maintainer,
        ),
    )


def maintainer_list(request):
    maintainers = models.ChecklistTemplateMaintainer.objects.all().order_by('ChecklistTemplateMaintainerName_Value')
    return render(
        request,
        'server/maintainer_list.html',
        dict(
            page_maintainers=paginator.Paginator(maintainers, 20).get_page(request.GET.get('page')),
        ),
    )


def checklist_detail(request, ChecklistTemplateID_Value):
    checklist_template = get_object_or_404(models.ChecklistTemplate, ChecklistTemplateID_Value=ChecklistTemplateID_Value)
    sections_and_questions = defaultdict(list)
    questions = checklist_template.Questions.all().order_by('DisplaySeqNumber_Value')
    question_form = generate_question_form(questions)()
    for question, field in zip(questions, question_form):
        sections_and_questions[question.SectionName_Value].append((question, field))
    return render(
        request,
        'server/checklist_detail.html',
        dict(
            other_checklist_templates=(
                models.ChecklistTemplate.objects
                .values_list('ChecklistTemplateName_Value', 'ChecklistTemplateID_Value')
                .order_by('ChecklistTemplateName_Value')
            ),
            checklist_template=checklist_template,
            sections_and_questions=dict(sections_and_questions),
        ),
    )


def model_to_ob_json(model):
    ob_json = defaultdict(dict)
    ob_model = ob_models.OBObject.objects.get(name=model._meta.object_name)
    for element in (
        ob_models.OBElement.objects.filter(obobject__name=model._meta.object_name)
        | ob_models.OBElement.objects.filter(obobject__in=ob_model.comprises.all())
    ):
        if element.item_type.units.exists():
            ob_json[element.name]['Unit'] = getattr(model, f'{element.name}_Unit')
        ob_json[element.name]['Value'] = getattr(model, f'{element.name}_Value')
    for nested_object in ob_model.nested_objects.all():
        ob_json[nested_object.name] = model_to_ob_json(getattr(model, nested_object.name))
    for element_array in ob_model.element_arrays.all():
        ob_json[element_array.name] = []
        for v in getattr(model, element_array.name).all():
            item_json = {}
            if element_array.items.item_type.units.exists():
                item_json['Unit'] = getattr(v, 'Unit')
            item_json['Value'] = getattr(v, 'Value')
            ob_json[element_array.name].append(item_json)
    for object_array in ob_model.object_arrays.all():
        ob_json[object_array.name] = [
            model_to_ob_json(v)
            for v in getattr(model, object_array.name).all()
        ]
    return ob_json


def maintainer_json(request, ChecklistTemplateMaintainerID_Value):
    maintainer = get_object_or_404(models.ChecklistTemplateMaintainer, ChecklistTemplateMaintainerID_Value=ChecklistTemplateMaintainerID_Value)
    ob_json = model_to_ob_json(maintainer)
    response = JsonResponse(ob_json, json_dumps_params=dict(indent=4))
    response['Content-Disposition'] = f'attachment; filename="{maintainer.ChecklistTemplateMaintainerID_Value}.json"'
    return response


def checklist_json(request, ChecklistTemplateID_Value):
    checklist_template = get_object_or_404(models.ChecklistTemplate, ChecklistTemplateID_Value=ChecklistTemplateID_Value)
    ob_json = model_to_ob_json(checklist_template)
    response = JsonResponse(ob_json, json_dumps_params=dict(indent=4))
    response['Content-Disposition'] = f'attachment; filename="{checklist_template.ChecklistTemplateID_Value}.json"'
    return response
