from django.contrib.algoliasearch import AlgoliaIndex

class QuestionIndex(AlgoliaIndex):
    fields = ('name', 'date')
    geo_field = 'location'
    settings = {'searchableAttributes': ['name']}
    index_name = 'my_index'