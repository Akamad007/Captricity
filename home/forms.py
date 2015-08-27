'''
Created on Jul 18, 2015

@author: akash
'''


from django import forms 

from home.models import HomeImages


class HomeImageForm(forms.ModelForm):
    
    class Meta:
        model = HomeImages
        exclude = ('is_active','name','user')
    