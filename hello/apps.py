from django.apps import AppConfig
from django.contrib import algoliasearch


# Register your models here.
class HelloConfig(AppConfig):
    name = 'hello'

    def ready(self):
        Question = self.get_model('Question')
        algoliasearch.register(Question)