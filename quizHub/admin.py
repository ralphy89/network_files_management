from django.contrib import admin
from .models import Quiz, Question, MultipleChoiceAnswer, ShortAnswer
# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(ShortAnswer)

