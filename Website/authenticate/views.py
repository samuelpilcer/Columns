from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import ConnexionForm, InscriptionForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion.html', locals())

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('connexion')
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))