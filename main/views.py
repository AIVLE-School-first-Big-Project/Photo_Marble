from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.views import PasswordChangeView,SignupView
from main.models import User
from . import forms
from django.contrib import auth
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from allauth.account.views import PasswordChangeView,SignupView,LogoutView
from django.contrib.auth.hashers import check_password

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
    profile_photo = user_db.profile_photo
    print(profile_photo)
    return render(request, '../templates/main/mypage.html', context={
        'user' : user_db
    })

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
            return redirect('http://127.0.0.1:8000/')
        # 실패
        else:
            messages.warning(request, "로그인을 실패했습니다.")
            return render(request, '../templates/main/login.html',{'message' : '로그인에 실패했습니다.','form':forms.LoginForm})
            #return render(request, 'member/error.html',  {'error': 'username or password is incorrect.'}))
    else:
        context = {'form':forms.LoginForm}
        return render(request, '../templates/main/login.html', context)

def main(request):#경주
    if request.user.is_authenticated == True:
        print(request.user.is_authenticated )
        return render(request, '../templates/main/main.html', {'login':"t"})
    else:
        print(request.user.is_authenticated )
        return render(request, '../templates/main/main.html', {'login':"f"})


def delete_account(request):
    # user = request.session()
    return render(request, '../templates/main/delete_account.html')

def delete(request):
    if request.method == 'POST':
        user =get_object_or_404(User, pk=request.session['id'])
    # user = request.session()
        if check_password(request.POST['password'],user.password):
            user.delete()
            result = True
        else:
            result = False

    return render(request, '../templates/main/delete_result.html',{'result':result})

def delete_result(request):
    return render(request, '../templates/main/delete_result.html')
class CustomSignupView(SignupView):
    template_name = "main/signup.html" 
    def form_valid(self, form):
        print(self)
        print("###########")
        print(form)
        self.user = form.save(self.request)
        print(self.user)
        return redirect("http://127.0.0.1:8000/login")
        # return redirect('login/')



class CustomSLogoutView(LogoutView):
    template_name = "main/logout.html"

class CustomSPasswordChangeView(PasswordChangeView):
    template_name = "main/password_change.html"

def get_redirect_url(self):
    return redirect("http://127.0.0.1:8000/login")
