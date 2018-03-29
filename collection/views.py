from django.shortcuts import render, redirect

from collection.forms import ProfileForm
from collection.models import Profile
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request): 
    profiles = Profile.objects.all()
    return render(request, 'index.html', {
        'profiles': profiles,
    })

def profile_detail(request, slug):
	profile = Profile.objects.get(slug=slug)
	return render(request, 'profiles/profile_detail.html', {
		'profile' : profile,
		})

@login_required
def edit_profile(request, slug):
	profile = Profile.objects.get(slug=slug)
	if profile.user != request.user:
		raise Http404
	form_class = ProfileForm
	if request.method == 'POST' :
		form = form_class(data=request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('profile_detail', slug=profile.slug)

	else:
		form = form_class(instance=profile)

	return render(request, 'profiles/edit_profile.html', {
		'profile' : profile,
		'form' : form,
		})

def create_profile(request):
	form_class = ProfileForm
	if request.method == 'POST':
		form = form_class(request.POST)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			profile.slug = slugify(profile.name)
			profile.save()
			return redirect('profile_detail', slug=profile.slug)
	else:
		form = form_class()
	return render(request, 'profiles/create_profile.html', {
		'form' : form,
		})