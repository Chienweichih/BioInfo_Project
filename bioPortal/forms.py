from django import forms

class QueryForm(forms.Form):
    query_text = forms.CharField(label='Query Text', max_length=100, initial='mitochondrion inheritance')

class NamedEntityForm(forms.Form):
    named_entity_text = forms.CharField(label='Abstract Text', widget=forms.Textarea, max_length=1000, initial='The mechanisms ensuring accurate partitioning of yeast vacuoles and mitochondria are distinct, yet they share common elements. Both organelles move along actin filaments, and both organelles require fusion and fission to maintain normal morphology. Recent studies have revealed that while vacuolar inheritance requires a processive myosin motor, mitochondrial inheritance requires controlled actin polymerization. Distinct sets of proteins required for the fusion and fission of each organelle have also been identified.')
