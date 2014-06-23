"""
 Custom tags for the Main module
"""

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
import json

register = Library()

"""
    Renders template context data as JSON in one of two ways
    depending on the type
"""
def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True  

"""
    Defaults to the django core serializer to serialize template
    context data as JSON always
"""
def as_json(object):
    return mark_safe(serialize('json', object))

register.filter('as_json', as_json)
as_json.is_safe = True

