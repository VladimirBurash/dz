from django.shortcuts import render, render_to_response, get_object_or_404,redirect
from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import LoginForm, SignupForm,AddShow
from .models import Show
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.core.files.storage import FileSystemStorage


def login(request):
    redirect_url = '/shows/'
    if request.method == 'POST':
        redirect_url = '/shows/'
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_url)
            else:
                form.add_error(None, 'invalid login/password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form,
                                          'continue': redirect_url})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form,
                                           'type': 'Registration'})



def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def render_cons(pos):
    ObjOnPage = 3
    shows = Show.objects.all()[ObjOnPage * pos: ObjOnPage * (pos + 1)]
    return shows

def ajax_list(request,page_id):
    pos = int(page_id)
    return render_to_response('base_con.html', {'shows': render_cons(pos)})

@csrf_exempt
def shows_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    shows = render_cons(0)
    form = AddShow(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            show = form.fill_object()
            f = request.FILES.get("image")
            print(f)

            if f is None:
                file_url = r'images/default.jpg'
            else:
                file_url = r'images/%d%s' % (show.id, '.jpg')
                fs = FileSystemStorage()
                filename = fs.save('my_app/static/' + file_url, File(f))

            show.image_url = file_url
            show.save()
            return redirect('show', show_id=show.id)
    else:
        return render(request, 'shows.html', {'shows': shows,
                                              'form': form})

@csrf_exempt
def show_view(request,show_id):
    show = get_object_or_404(Show, id=show_id)
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        status = show.participation.filter(id=request.user.id).exists()

        return render(request, 'show.html',
                      { 'show': Show.objects.get(id=show_id), 'status': status}
                      )

    if request.method == 'POST':
        state = request.POST.get('state')
        if state == "True" and not show.participation.filter(id=request.user.id).exists():
                show.participation.add(request.user)
        if state == 'False' and show.participation.filter(id=request.user.id).exists():
                show.participation.remove(request.user)

        return render_to_response('users_list.html', {'users': show.participation.all()})





