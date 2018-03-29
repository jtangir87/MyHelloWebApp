from django.forms import ModelForm
from collection.models import Profile

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ('name', 'description')
