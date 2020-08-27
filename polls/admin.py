from django.contrib import admin
from .models import Question,Choice
from django.contrib.auth.models import User


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets= [(None, {"fields":["question_text"]}),
                ("DateInformation", {"fields": ["pub_date"], "classes":["collapse"]}), ("Users", {"fields": ["author"], "classes":["collapse"]}), ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
