from django.contrib import admin
from .models import Question, Answer


# Register your models here.
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["txt_clean",'question_id', "src", "updated"]

    class Meta:
        model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["txt_clean", "src", "updated"]

    class Meta:
        model = Answer


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)