from django import forms

class get_month(forms.Form):
    month_num = forms.IntegerField(label='Month')