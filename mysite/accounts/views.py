from django.shortcuts import render,redirect
from .forms import CreateUserForm
# Create your views here.
def create_user(request):
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = CreateUserForm()
        
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
        