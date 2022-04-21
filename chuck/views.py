from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse('Hello <br> <a href="http://localhost:8000/chuck/form_post">form post</a><br><a href="http://localhost:8000/chuck/form_get">form get</a><br><a href="http://localhost:8000/chuck/form_class">form class</a><br><a href="http://localhost:8000/chuck/form_class_session">form_class_session</a><br><a href="http://localhost:8000/chuck/cookies">cookies</a> <br><a href="http://localhost:8000/chuck/sessions">sessions</a>')


def dump_data(label, data, response):
    for key, val in data.items():
        print(key, val)
        response += f'{key} = {val}<br>'
    return response


@csrf_exempt
def form_post(request):

    response = """<h1> Hello, this is survey</h1>
    <form name='hello' action='' method="POST" >
        <label for='guess'> Input guess </label>
        <input type='text' name='guess' size=40 id='guess' placeholder= {1} />
        <br>
        <label for='age'> How old r u? </label>
        <input type='text' name='age' size=40 id='age' placeholder= {2} />
        <button type='submit'>Submit</button>
    </form>
    """

    for key, val in request.POST.items():
        response += f'{key} = {val}<br>'
    # response = dump_data('POST', request.POST, response)
    return HttpResponse(response)


def form_get(request):
    response = """<h1> Hello, this is survey</h1>
    <form name='hello' action=''>
        <label for='guess'> Input guess </label>
        <input type='text' name='guess' size=40 id='guess'/>
        <br>
        <label for='age'> How old r u? </label>
        <input type='text' name='age' size=40 id='age'/>
        <button type='submit'>Submit</button>
    </form>\n
    """

    response = dump_data('GET', request.GET, response)
    return HttpResponse(response)


class Guess(View):

    def get(self, request):
        return render(request, 'chuck/chuck_form.html')

    def post(self, request):
        guess = request.POST.get('guess')
        return render(request, 'chuck/chuck_form.html', {'msg': guess})


class GuessSession(View):

    def get(self, request):
        msg = request.session.get('msg', False)
        if msg:
            del(request.session['msg'])
        return render(request, 'chuck/chuck_form.html', {'msg': msg})

    def post(self, request):
        guess = request.POST.get('guess')
        request.session['msg'] = guess
        return redirect(request.path)


def cookies(request):
    print('----', request.COOKIES, '----')
    print(f'Cookies that I have:\n')
    text = ''
    for key, val in request.COOKIES.items():
        text += key + ': ' + val + '<br>'
    resp = HttpResponse(text)
    resp.set_cookie('Love', 'Anya')
    resp.set_cookie('21', '32')
    resp.set_cookie('Fuck', 'Me', max_age=100000)
    resp.set_cookie('Anya', 'I wanna lick u pussy and fuck u so hard')

    return resp


def sessions(request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    # if num_visits > 4: del(request.session['num_visits'])
    return HttpResponse('view count=' + str(num_visits))
