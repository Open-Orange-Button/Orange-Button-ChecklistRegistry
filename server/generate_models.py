import ast

from django.db import models
from django.core import validators

import ob_taxonomy.models as ob_models


def get_django_enum_name(ob_item_type: ob_models.OBItemType):
    suffix = 'Enum' if ob_item_type.enums.exists() else 'Unit'
    return f'{ob_item_type.name}{suffix}'


def generate_django_enum_class(name, enums):
    return ast.ClassDef(
        name=name,
        bases=[ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='TextChoices', ctx=ast.Load())],
        keywords=[],
        body=[
            ast.Assign(
                targets=[ast.Name(id=e.name, ctx=ast.Store())],
                value=ast.Tuple(elts=[
                    ast.Constant(value=e.name),
                    ast.Call(
                        func=ast.Name(id='_'),
                        args=[ast.Constant(value=e.name if e.label == '' else e.label)]
                    ),
                ], ctx=ast.Load()),
            )
            for e in enums
        ],
        decorator_list=[],
    )


def generate_django_enum_field_assignment(name):
    return ast.Call(
        func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='CharField', ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg='max_length', value=ast.Call(
                func=ast.Name(id='max', ctx=ast.Load()),
                args=[
                    ast.Call(
                        func=ast.Name(id='map', ctx=ast.Load()),
                        args=[
                            ast.Name(id='len', ctx=ast.Load()),
                            ast.Name(id=name, ctx=ast.Load()),
                        ]
                    )
                ]
            )),
            ast.keyword(arg='choices', value=ast.Name(id=name, ctx=ast.Load()))
        ],
    )


def item_type_to_django_field(ob_item_type: ob_models.OBItemType, context):
    match ob_item_type.name:
        case 'AnswerTypeItemType' | 'EntityRoleItemType':
            enum_name = get_django_enum_name(ob_item_type)
            if enum_name not in context['django_enum_classes']:
                context['django_enum_classes'][enum_name] = generate_django_enum_class(enum_name, ob_item_type.enums.all())
            return generate_django_enum_field_assignment(enum_name)
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='CharField', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='max_length', value=ast.Call(
                        func=ast.Name(id='max', ctx=ast.Load()),
                        args=[
                            ast.Call(
                                func=ast.Name(id='map', ctx=ast.Load()),
                                args=[
                                    ast.Name(id='len', ctx=ast.Load()),
                                    ast.Name(id=enum_name, ctx=ast.Load()),
                                ]
                            )
                        ]
                    )),
                    ast.keyword(arg='choices', value=ast.Name(id=enum_name, ctx=ast.Load()))
                ],
            )
        case 'DecimalItemType':
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='DecimalField', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='max_digits', value=ast.Constant(value=3)),
                    ast.keyword(arg='decimal_places', value=ast.Constant(value=3)),
                    ast.keyword(arg='blank', value=ast.Constant(value=True)),
                    ast.keyword(arg='null', value=ast.Constant(value=True)),
                ],
            )
        case 'IntegerItemType':
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='IntegerField', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='blank', value=ast.Constant(value=True)),
                    ast.keyword(arg='null', value=ast.Constant(value=True)),
                ],
            )
        case 'StringItemType':
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='CharField', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='max_length', value=ast.Constant(value=500)),
                    ast.keyword(arg='blank', value=ast.Constant(value=True)),
                ],
            )
        case 'LegalEntityIdentifierItemType':
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='CharField', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='max_length', value=ast.Constant(value=20)),
                    ast.keyword(arg='blank', value=ast.Constant(value=True)),
                ],
            )
        case 'UUIDItemType':
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='UUIDField', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='unique', value=ast.Constant(value=True)),
                    ast.keyword(arg='editable', value=ast.Constant(value=False)),
                    ast.keyword(arg='default', value=ast.Attribute(value=ast.Name(id='uuid', ctx=ast.Load()), attr='uuid4', ctx=ast.Load())),
                ],
            )
        case _:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='CharField', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='max_length', value=ast.Constant(value=500)),
                    ast.keyword(arg='blank', value=ast.Constant(value=True)),
                ],
            )
            raise ValueError(f'Django field for item type {ob_item_type!r} is unknown.')


def generate_ob_element(ob_element: ob_models.OBElement, generated_item_type_django_enums: set):
    pass


def generate_ob_array_of_element(element_array: ob_models.OBArrayOfElement, context):
    if element_array.name in context['ob_arrays_of_element']:
        return
    klass = ast.ClassDef(
        name=element_array.items.name,
        bases=[ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='Model', ctx=ast.Load())],
        keywords=[],
        body=[
            ast.Assign(
                targets=[ast.Name(id='Value', ctx=ast.Store())],
                value=item_type_to_django_field(element_array.items.item_type, context),
            )
        ],
        decorator_list=[],
    )
    context['ob_arrays_of_element'][element_array.name] = klass


def generate_ob_object(ob_object: ob_models.OBObject, context, is_super_ob_object=False):
    if ob_object.name in context['ob_objects'] or ob_object.name in context['super_ob_objects']:
        return
    if ob_object.comprises.exists():
        if ob_object.comprises.through.objects.exclude(method='allOf').exists():
            raise ValueError(f'Cannot generate Django model for {ob_object!r} because only the comprisal method "allOf" is currently supported.')
        if ob_object.comprises.count() > 1:
            raise ValueError(f'Cannot generate Django model for {ob_object!r} because the comprisal of multiple OBObjects is not currently supported.')
        super_ob_object = ob_object.comprises.first()
        generate_ob_object(super_ob_object, context, is_super_ob_object=True)
        bases = [ast.Name(id=super_ob_object.name)]
    else:
        bases = [ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='Model', ctx=ast.Load())]
    klass = ast.ClassDef(
        name=ob_object.name,
        bases=bases,
        keywords=[],
        body=[],
        decorator_list=[],
    )
    for ob_element in ob_object.properties.all().order_by('name'):
        field = ast.Assign(
            targets=[ast.Name(id=f'{ob_element.name}_Value', ctx=ast.Store())],
            value=item_type_to_django_field(ob_element.item_type, context),
        )
        klass.body.append(field)
    for nested_ob_object in ob_object.nested_objects.all().order_by('name'):
        generate_ob_object(nested_ob_object, context)
        field = ast.Assign(
            targets=[ast.Name(id=nested_ob_object.name, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='ForeignKey', ctx=ast.Load()),
                args=[ast.Constant(value=nested_ob_object.name)],
                keywords=[
                    ast.keyword(arg='on_delete',
                                value=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='CASCADE', ctx=ast.Load())),
                ]
            )
        )
        klass.body.append(field)
    for element_array in ob_object.element_arrays.all().order_by('name'):
        generate_ob_array_of_element(element_array, context)
        field = ast.Assign(
            targets=[ast.Name(id=element_array.name, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='ManyToManyField', ctx=ast.Load()),
                args=[ast.Constant(value=element_array.items.name)],
                keywords=[]
            )
        )
        klass.body.append(field)
    for object_array in ob_object.object_arrays.all().order_by('name'):
        generate_ob_object(object_array.items, context)
        field = ast.Assign(
            targets=[ast.Name(id=object_array.name, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='ManyToManyField', ctx=ast.Load()),
                args=[ast.Constant(value=object_array.items.name)],
                keywords=[]
            )
        )
        klass.body.append(field)
    if is_super_ob_object:
        context['super_ob_objects'][ob_object.name] = klass
    else:
        context['ob_objects'][ob_object.name] = klass


def assign_constant(name, value):
    return ast.Assign(
        targets=[ast.Name(id=name, ctx=ast.Store())],
        value=ast.Constant(value=value)
    )


def generate_module(ob_objects):
    context = dict(
        django_enum_classes={},
        super_ob_objects={},
        ob_objects={},
        ob_arrays_of_element={},
    )
    for ob_object in ob_objects:
        generate_ob_object(ob_object, context)
    tree = ast.Module(
        body=[
            ast.Import(names=[ast.alias(name='uuid', asname=None)]),
            ast.ImportFrom(module='django.db', names=[ast.alias(name='models')], level=0),
            ast.ImportFrom(module='django.utils.translation', names=[ast.alias(name='gettext_lazy', asname='_')], level=0),
            # *(assign_constant(k, constants[k]) for k in sorted(constants.keys())),
            *(context['django_enum_classes'][k] for k in sorted(context['django_enum_classes'].keys())),
            *(context['super_ob_objects'][k] for k in sorted(context['super_ob_objects'].keys())),
            *(context['ob_objects'][k] for k in sorted(context['ob_objects'].keys())),
            *(context['ob_arrays_of_element'][k] for k in sorted(context['ob_arrays_of_element'].keys())),
        ],
        type_ignores=[],
    )
    return tree


def test():
    ob_object = ob_models.OBObject.objects.filter(name='ChecklistTemplate')
    constants = dict(
        CHARFIELD_LEN=500,
        DECIMALFIELD_DECIMAL_PLACES=20,
        DECIMALFIELD_MAX_DIGITS=40,
    )
    tree = generate_module(ob_object)
    tree = ast.fix_missing_locations(tree)
    print(ast.unparse(tree))

