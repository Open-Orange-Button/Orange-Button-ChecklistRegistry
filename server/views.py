import ast
from collections import defaultdict
import datetime

import django.forms as forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

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
    return HttpResponse('hi')


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
            checklist_template=checklist_template,
            sections_and_questions=dict(sections_and_questions),
        ),
    )

