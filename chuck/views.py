from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse('Hello <br> <a href="http://localhost:8000/chuck/form_post">form post</a><br><a href="http://localhost:8000/chuck/form_get">form get</a><br><a href="http://localhost:8000/chuck/form_class">form class</a>')


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
