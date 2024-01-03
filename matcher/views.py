# matcher/views.py

from django.shortcuts import render, redirect
from .forms import InterestForm
from .models import Interest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def manage_interests(request):
    if request.method == 'POST':
        form = InterestForm(request.POST)  # instance=request.user)
        if form.is_valid():
            selected_interests = form.cleaned_data['interests']
            print(selected_interests)
            request.user.interests.set(selected_interests)
            request.user.save()
            return redirect('home')
    else:
        form = InterestForm(initial={'interests': request.user.interests.all()})

    context = {'form': form}

    return render(request, 'snippets/interests.html', context)


@login_required
def user_interests(request):
    # Fetch interests related to the logged-in user
    user_interests = request.user.interests.all()
    print('Logged in user id:', request.user.id)
    print('Logged in user username:', request.user.username)
    print(user_interests)
    return render(request, 'snippets/user_interests.html', {'interests': user_interests})
    # print(f'You have interests',user_interests)
    # return render(request, 'snippets/user_interests.html', {'interests': user_interests})