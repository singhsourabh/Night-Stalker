from django import forms
from .models import User

class NewUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'codechef', 'spoj', 'codeforce']
        widgets = {
            'name': forms.TextInput(attrs={'id':'handle', 'class':'name', 'required':'true', 'placeholder':'Enter name'}),
            'codechef': forms.TextInput(attrs={'id':'ccname', 'class':'cc', 'placeholder':'Enter codechef username'}),
            'spoj' : forms.TextInput(attrs={'id':'spojname', 'class':'spoj', 'placeholder':'Enter spoj username'}),
            'codeforce' : forms.TextInput(attrs={'id':'cfname', 'name':'cfname', 'class':'cf', 'placeholder':'Enter codeforces username'})
        }
