# forms.py
from django import forms

class ScrapingForm(forms.Form):
    url_to_scrape = forms.URLField(label='URL à scraper')
    class_names = forms.CharField(widget=forms.Textarea, label='Noms de classe CSS')
    max_pages = forms.IntegerField(label='Max Pages', required=False)  
