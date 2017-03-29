from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['txt']
        labels = {
            'txt': "Votre Question",
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['txt']
        labels = {
            'txt': "Votre réponse",
        }

    # def clean_sentiment_label(self):
    #     sent = self.cleaned_data.get('sentiment_label')
    #     if sent == Tweet.SENTIMENTS['UNKNOWN']:
    #         raise forms.ValidationError("Si tu ne sais pas qui donc saura :p")
    #     return sent
