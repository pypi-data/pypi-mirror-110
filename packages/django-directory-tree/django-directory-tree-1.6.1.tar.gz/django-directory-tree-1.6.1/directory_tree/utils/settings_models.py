from django.conf import settings
from django.apps import apps

TREE_DRIECTORY_TABLE = {}

try:
    DIRECTORY_TREE_MODEL = settings.DIRECTORY_TREE_MODEL
except:
    DIRECTORY_TREE_MODEL = {}

try:
    DIRECTORY_TREE_MODEL_USE = settings.DIRECTORY_TREE_MODEL_USE
except:
    DIRECTORY_TREE_MODEL_USE = False

def filter_field(model, list_field):
    count = 0
    for field in model._meta.fields:
        if field.name in list_field:
            count += 1
    if count == len(list_field):
        return True

    raise Exception('{} some field in this is not in model {}'.format(list_field, model.__name__))
    
def all_table():
    models = {
        model.__name__: model for model in apps.get_models()
    }

    for key, model_obj in models.items():
        if key in DIRECTORY_TREE_MODEL:
            fields = DIRECTORY_TREE_MODEL[key]
            filter_field(model_obj, fields)
            TREE_DRIECTORY_TABLE[key] = {
                "model": model_obj,
                "fields": fields
            }

all_table()