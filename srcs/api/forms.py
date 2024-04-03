from django import forms

class uploadProfilePicture(forms.Form):
    file = forms.FileField()