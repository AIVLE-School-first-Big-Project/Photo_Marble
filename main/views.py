from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from main.models import User
from . import forms
from django.contrib import auth
from django.shortcuts import render,get_object_or_404
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
def main(request):#경주
    return render(request,'../templates/main/main.html')

def login(request):
    # 포스트 
    if request.method == 'POST':
        # 정보 가져와서 
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        print("###############")
        # 로그인
        user = auth.authenticate(request, email=email, password=password)
        print(user)

        # 성공
        if user is not None:
            auth.login(request, user)
            request.session['id'] = user.id
            print( request.session['id'])
            return render(request, '../templates/main/main.html')
        # 실패
        else:
            messages.warning(request, "로그인을 실패했습니다.")
            return render(request, '../templates/main/login.html',{'message' : '로그인에 실패했습니다.','form':forms.LoginForm})
            #return render(request, 'member/error.html',  {'error': 'username or password is incorrect.'}))
    else:
        context = {'form':forms.LoginForm}
        return render(request, '../templates/main/login.html', context)

def main(request):#경주
    return render(request,'../templates/main/main.html')

def delete(request):
    # user = request.session()
    user =get_object_or_404(User, pk=request.session['id'])
    user.delete()
    messages.success(request, '탈퇴가 완료됐습니다.')
    return redirect("http://127.0.0.1:8000/")
