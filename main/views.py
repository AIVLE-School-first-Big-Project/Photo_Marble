from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from main.models import User
from . import forms
from django.contrib import auth
from django.contrib import messages


# Create your views here.

def index(request):
    if request.user.is_authenticated == False:
        context = {'form':forms.LoginForm}
        return render(request, '../templates/main/login.html', context)
    else:
        return render(request, '../templates/main/main.html')

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("index")

def mypage(request):

    user_db = User.objects.get(id= request.session['id'])
    print(user_db)
    return render(request, '../templates/main/mypage.html', context={
        'user' : user_db
    })


def login(request):
    # 포스트 
    if request.method == 'POST':
        # 정보 가져와서 
        email = request.POST['email']
        password = request.POST['password']

        # 로그인
        user = auth.authenticate(request, email=email, password=password)


        # 성공
        if user is not None:
            auth.login(request, user)
            request.session['id'] = user.id
            print( request.session['id'])
            return render(request, '../templates/main/main.html')
        # 실패
        else:
            messages.warning(request, "로그인에 실패했습니다.")
            return render(request, '../templates/main/login.html',{'message' : '로그인에 실패했습니다.','form':forms.LoginForm})
          
            # return render(request, '../templates/main/login.html',{'form':forms.LoginForm})
    else:
        context = {'form':forms.LoginForm}
        return render(request, '../templates/main/login.html', context)