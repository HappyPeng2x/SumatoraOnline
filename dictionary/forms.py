from django import forms

class SearchForm(forms.Form):
    expression = forms.CharField(max_length=100)

    def clean_expression(self):
        return self.cleaned_data['expression']
