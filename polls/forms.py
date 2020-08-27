from django import forms
from . models import Question, Choice
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *





class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text','votes', "question"]
    # def __init__(self, *args, **kwargs):
    #     super(ChoiceForm, self).__init__(*args, **kwargs)
    #     self.fields[].widget.attrs['readonly'] = True


ChoiceFormSet = inlineformset_factory(
    Question, Choice, form=ChoiceForm,
    fields=['choice_text'], extra=3, can_delete=False,max_num=3,fk_name='question'
)

ChoiceFormSetUpdate = inlineformset_factory(
    Question, Choice, form=ChoiceForm,
    fields=['choice_text'], extra=3, can_delete=False, max_num=3, fk_name='question'
)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]
        
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-7 create-label'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            Div(
                HTML("<br>"),
                Field('question_text'),
                HTML("<br>"),
                Fieldset('Choice',Formset("choices")),
                ButtonHolder(Submit('submit', 'Submit')),
            )
        )
