from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
from hello.views import open_query
from hello.views import new_question, new_answer

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^query/', open_query, name='query'),
    url(r'^new/question/', new_question, name='question'),
    url(r'^new/answer', new_answer, name='answer'), # il faut pouvoir lire le param dans l url et non
]
