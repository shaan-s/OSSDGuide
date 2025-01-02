from django import forms
from .models import school_boards
from django.forms import MultiWidget
from django.core.validators import RegexValidator

class ReviewForm(forms.Form):
    numbers = {None:"—","1":1,"2":2,"3":3,"4":4,"5":5}
    review_text = forms.CharField(max_length=1023,required=False,label="Review: (optional)",widget= forms.Textarea, validators=[RegexValidator(regex=r'[ -~]+',message="Only ASCII characters are accepted (letters, numbers, and punctuation).")])
    online = forms.BooleanField(required=False)
    overall_rating = forms.ChoiceField(choices=numbers)
    interesting_rating = forms.ChoiceField(choices=numbers)
    easy_rating = forms.ChoiceField(choices=numbers)
    user_school_board = forms.ChoiceField(choices=school_boards, label="What is your school board?")
