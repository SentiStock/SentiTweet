from django import forms
from tweet.models import Set


class SetForm(forms.ModelForm):
    # def save(self):
    #     instance = forms.ModelForm.save(self)
    #     instance.hashtags.clear()
    #     instance.hashtags.add(*self.cleaned_data['hashtags'])
    #     return instance

    class Meta:
        model = Set
        fields = ['name', 'description', 'hashtags', 'mode']
        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description', 'required': True}),
            'hashtags': forms.SelectMultiple(attrs={'class': 'form-control selectpicker', 'required': True, 'data-live-search':'true'}),
            'mode': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }