# account/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .models import Account

def check_user_not_authenticated(user):
    # oturum açmamış kullanıcıları kontrol eder.
    return not user.is_authenticated

@user_passes_test(check_user_not_authenticated, login_url='/', redirect_field_name=None)
def register(request):
    # differentiates whether post or get
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account has been created')
            # redirect registrations to interets page
            
        else:
            # add an error message here if the form is not valid
            messages.error(request, 'Error creating account')
    else:
       form = UserRegistrationForm()

    return render(request, 'snippets/register.html', {'form': form})



def view_profile(request, username):
    user_profile = get_object_or_404(Account, username=username)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'snippets/profile.html', context)



# oturum açmış kullanıcıların, register ve login sayfalarına erişim engeli
