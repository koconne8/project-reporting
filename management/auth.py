from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, HttpResponseRedirect
from pr.settings.base import LOGIN_URL
from django.core.urlresolvers import reverse


def login_page(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html', {})
    else:
        # try logging them in
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'auth/login.html', {'error': 'Incorrect username/password.'})

        # otherwise, log them in
        login(request, user)

        if 'next' in request.POST:
            return HttpResponseRedirect(request.POST['next'])
        else:
            return HttpResponseRedirect(reverse('home'))


def logout_request(request):
    logout(request)
    return HttpResponseRedirect(LOGIN_URL)
