from django import forms
from .models import UserDetail

class NewUser(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['name', 'codechef', 'spoj', 'codeforce']
        widgets = {
            'name': forms.TextInput(attrs={'id':'handle', 'class':'name', 'required':'true', 'placeholder':'Enter name'}),
            'codechef': forms.TextInput(attrs={'id':'ccname', 'class':'cc', 'placeholder':'Enter codechef username'}),
            'spoj' : forms.TextInput(attrs={'id':'spojname', 'class':'spoj', 'placeholder':'Enter spoj username'}),
            'codeforce' : forms.TextInput(attrs={'id':'cfname', 'name':'cfname', 'class':'cf', 'placeholder':'Enter codeforces username'})
        }

class Modify(forms.Form):
    mcodechef = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'mcc', 'placeholder':'leave blank for no change'}))
    mspoj = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'mspoj', 'placeholder':'leave blank for no change'}))
    mcodeforce = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'mcf', 'placeholder':'leave blank for no change'}))
