from django import forms

class QueryForm(forms.Form):
    query_text = forms.CharField(label='Query Text', max_length=100)

class NamedEntityForm(forms.Form):
    named_entity_text = forms.CharField(label='Abstract Text', widget=forms.Textarea, max_length=1000)
