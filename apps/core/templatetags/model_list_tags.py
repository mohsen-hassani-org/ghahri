from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    value = ''
    if isinstance(dictionary, dict):
        if dictionary.get(key):
            value = dictionary.get(key)
    return value

@register.filter
def get_object_item(object_item, key):
    keys = key.split('__')
    for key in keys:
        object_item = getattr(object_item, key)
    return object_item

@register.filter
def get_verbose_name(model, key):
    if '__' not in key:
        return model._meta.get_field(key).verbose_name
    keys = key.split('__')
    for key in keys:
        model = model._meta.get_field(key).related_model or model
    return model._meta.get_field(key).verbose_name
