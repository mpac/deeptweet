from django.db import models
import datetime

class AddedDateTimeField(models.DateTimeField):
    def get_internal_type(self):
        return models.DateTimeField.__name__
    def pre_save(self, model_instance, add):
        if model_instance.id is None:
            return datetime.datetime.now()
        else:
            return getattr(model_instance, self.attname)

class ModifiedDateTimeField(models.DateTimeField):
    def get_internal_type(self):
        return models.DateTimeField.__name__
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()
