from django.forms.models import ModelForm
from shop.models import Profile,CompanyProfile
from django.forms.widgets import Textarea

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'info': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
    
class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ('user','account',)
        widgets = {
            'info': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
