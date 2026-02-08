import ast
from collections import defaultdict
from functools import partial
import itertools

import ob_taxonomy.models as models


def default_field_kwargs(ob_taxonomy_element: models.OBTaxonomyElement, **kwargs):
    match ob_taxonomy_element.name:
        case 'TaxonomyElementString':
            return dict(blank=True, **kwargs)
        case 'TaxonomyElementArrayBoolean':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
        case 'TaxonomyElementArrayInteger':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
        case 'TaxonomyElementArrayNumber':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
        case 'TaxonomyElementArrayString':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
        case _:
            return dict(blank=True, null=True, **kwargs)


# dict of functions Callable[models.OBTAxonomyElement]
# we do not necessarily know the type of the field given only the item type.
# If the itemtype is not decimal or integer item type, any item type that defines
# units has unknown type without knowing the taxonomy element
OB_ITEM_TYPE_FIELD_CONF = defaultdict(lambda: default_field_kwargs)
OB_ITEM_TYPE_FIELD_CONF['LegalEntityIdentifierItemType'] = partial(default_field_kwargs, max_length=20)


def taxonomy_element_to_django_field(ob_taxonomy_element: models.OBTaxonomyElement, field_kwargs):
    match ob_taxonomy_element.name:
        case 'TaxonomyElementBoolean':
            field_class = 'BooleanField'
        case 'TaxonomyElementInteger':
            field_class = 'IntegerField'
        case 'TaxonomyElementNumber':
            field_class = 'DecimalField'
        case 'TaxonomyElementString':
            field_class = 'CharField'
        case 'TaxonomyElementArrayBoolean':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
        case 'TaxonomyElementArrayInteger':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
        case 'TaxonomyElementArrayNumber':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
        case 'TaxonomyElementArrayString':
            raise NotImplementedError(f'taxonomy_element_to_django_field: {ob_taxonomy_element.name}')
    return ast.Call(
        func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr=field_class, ctx=ast.Load()),
        args=[],
        keywords=[ast.keyword(arg=k, value=v) for k, v in field_kwargs.items()],
    )



# defining the fields
# 1. What is the item type?
#  a. Does the item type define enums? Then Value is a string with choices
#  b. Does the item type define units? Then Value follows the TaxonomyElement used, and Units is a string with choices
#  c. Are neither enums nor units defined? Then Value follows the TaxonomyElement used.


def generate_django_enum_field(django_enum_name: str):
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
                            ast.Name(id=django_enum_name, ctx=ast.Load()),
                        ]
                    )
                ]
            )),
            ast.keyword(arg='choices', value=ast.Name(id=django_enum_name, ctx=ast.Load()))
        ],
    )


def generate_django_enum_class(django_enum_name: str, enums: type[models.OBItemTypeEnum | models.OBItemTypeUnit]):
    return ast.ClassDef(
        name=django_enum_name,
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


def generate_ob_element(ob_element: models.OBElement, context=None):
    context = context or dict(django_enum_class={})
    fields = []
    if ob_element.item_type.enums.exists():
        django_enum_name = f'{ob_element.item_type.name}Enum'
        django_enum_classes[django_enum_name] = generate_django_enum_class(django_enum_name, ob_element.item_type.enums)
        value_field = generate_django_enum_field(django_enum_name)
        fields.append(value_field)
    else:
        if ob_element.item_type.units.exists():
            django_enum_name = f'{ob_element.item_type.name}Unit'
            django_enum_classes[django_enum_name] = generate_django_enum_class(django_enum_name, ob_element.item_type.units)
            unit_field = generate_django_enum_field(django_enum_name)
            fields.append(unit_field)
            conf = OB_ITEM_TYPE_FIELD_CONF[ob_element.item_type](ob_element.taxonomy_element)
            value_field = taxonomy_element_to_django_field(ob_element.taxonomy_element, conf['field_args'], conf['field_kwargs'])
            fields.append(value_field)


def generate_ob_element_array(element_array: models.OBArrayOfElement):
    return ast.ClassDef(
        name=element_array.items.name,
        bases=[ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='Model', ctx=ast.Load())],
        keywords=[],
        body=generate_ob_element_fields(element_array.items),
        decorator_list=[],
    )


def generate_ob_object_array(object_array: models.OBArrayOfObject):
    return ast.ClassDef(
        name=object_array.items.name,
        bases=[ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='Model', ctx=ast.Load())],
        keywords=[],
        body=generate_foreign_key(object_array.items.name),
        decorator_list=[],
    )


def build_django_enum_class_context(ob_taxonomy_element: models.OBTaxonomyElement, ob_item_type: models.OBItemType, context):
    if ob_item_type.enums.exists():
        class_name = f'{ob_item_type.name}Enum'
        enums = ob_item_type.enums.all()
    elif ob_item_type.units.exists():
        class_name = f'{ob_item_type.name}Unit'
        enums = ob_item_type.units.all()
    else:
        return
    context['django_enum_classes'][class_name] = (class_name, enums)


def build_ob_object_context(ob_object: models.OBObject, context):
    if ob_object.name in context['super_objects'] or ob_object.name in context['objects']:
        return
    if ob_object.comprises.exists():
        if ob_object.comprises.through.objects.exclude(method='allOf').exists():
            raise ValueError(f'Cannot generate Django model for {ob_object!r} because only the comprisal method "allOf" is currently supported.')
        if ob_object.comprises.count() > 1:
            raise ValueError(f'Cannot generate Django model for {ob_object!r} because the comprisal of multiple OBObjects is not currently supported.')
        comprisal = ob_object.comprises.first()
        build_ob_object_context(comprisal, context)
        context['super_objects'][comprisal.name] = comprisal
    for ob_element in ob_object.properties.all():
        build_django_enum_class_context(ob_element.taxonomy_element, ob_element.item_type, context)
    for nested_object in ob_object.nested_objects.all():
        if nested_object.name not in context['objects']:
            build_ob_object_context(nested_object, context)
    for element_array in ob_object.element_arrays.all():
        build_django_enum_class_context(element_array.items.taxonomy_element, element_array.items.item_type, context)
    for object_array in ob_object.object_arrays.all():
        build_ob_object_context(object_array.items, context)
    context['objects'][ob_object.name] = ob_object


def generate_foreign_key(name):
    return ast.Assign(
        targets=[ast.Name(id=name, ctx=ast.Store())],
        value=ast.Call(
            func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='ForeignKey', ctx=ast.Load()),
            args=[ast.Constant(value=name)],
            keywords=[
                ast.keyword(arg='on_delete',
                            value=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='CASCADE', ctx=ast.Load())),
            ]
        )
    )


def generate_manytomany(name, name_other):
    return ast.Assign(
        targets=[ast.Name(id=name, ctx=ast.Store())],
        value=ast.Call(
            func=ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='ManyToManyField', ctx=ast.Load()),
            args=[ast.Constant(value=name_other)],
            keywords=[]
        )
    )


def generate_ob_object(ob_object: models.OBObject):
    if ob_object.comprises.exists():
        bases = [ast.Name(id=ob_object.comprises.first().name)]
    else:
        bases = [ast.Attribute(value=ast.Name(id='models', ctx=ast.Load()), attr='Model', ctx=ast.Load())]
    klass = ast.ClassDef(
        name=ob_object.name,
        bases=bases,
        keywords=[],
        body=[],
        decorator_list=[],
    )
    # for ob_element in ob_object.properties.all().order_by('name'):
    #     klass.body.extend(generate_ob_element_fields(ob_element))
    for nested_object in ob_object.nested_objects.all().order_by('name'):
        klass.body.append(generate_foreign_key(nested_object.name))
    for array in itertools.chain(
        # ob_object.element_arrays.all().order_by('name'),
        ob_object.object_arrays.all().order_by('name')
    ):
        klass.body.append(generate_manytomany(array.name, array.items.name))
    return klass


def generate_model_module(ob_objects):
    context = dict(
        django_enum_classes={},
        super_objects={},
        objects={},
        object_arrays={},
        element_arrays={},
    )
    for ob_object in ob_objects:
        build_ob_object_context(ob_object, context)
    generators = dict(
        django_enum_classes=lambda v: generate_django_enum_class(*v),
        super_objects=generate_ob_object,
        objects=generate_ob_object,
        object_arrays=generate_ob_object_array,
        # element_arrays=generate_ob_element_array,
    )
    for (k, v), g in zip(context.items(), generators.values()):
        context[k] = [g(v[kk]) for kk in sorted(v.keys())]
    tree = ast.Module(
        body=list(itertools.chain.from_iterable(context.values())),
        type_ignores=[],
    )
    tree = ast.fix_missing_locations(tree)
    return tree


def test():
    tree = generate_model_module(models.OBObject.objects.filter(name='ChecklistTemplate'))
    print(ast.unparse(tree))
