from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from allauth.account.views import PasswordChangeView, SignupView, LogoutView
from main.models import User
from . import forms
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# 활성화함수위해
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import member_activation_token
from django.core.exceptions import ValidationError


def index(request):
    if request.user.is_authenticated is False:
        context = {'form': forms.LoginForm}
        return render(request, '../templates/main/login.html', context)
    else:
        return render(request, '../templates/main/main.html')


class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        return reverse("index")


def mypage(request):
    if request.user.is_authenticated is True:
        user_db = User.objects.get(id=request.session['id'])

        return render(request, '../templates/main/mypage.html', context={
            'user': user_db})

    else:
        messages.add_message(request, messages.INFO, '접근 권한이 없습니다')
        return render(request, '../templates/main/mypage.html')


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
            return redirect('main')

        # 실패
        else:
            messages.warning(request, "로그인을 실패했습니다.")
            return render(request, '../templates/main/login.html', {'message': '로그인에 실패했습니다.', 'form': forms.LoginForm})

    else:
        context = {'form': forms.LoginForm}
        return render(request, '../templates/main/login.html', context)


def main(request):
    if request.user.is_authenticated is True:
        return render(request, '../templates/main/main.html', {'login': "t"})

    else:
        return render(request, '../templates/main/main.html', {'login': "f"})


# 회원 탈퇴
def delete_account(request):
    return render(request, '../templates/main/delete_account.html')


# 마이페이지에서의 회원탈퇴
def delete(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.session['id'])

        if check_password(request.POST['password'], user.password):
            user.delete()
            result = True

        else:
            result = False

    return render(request, '../templates/main/delete_result.html', {'result': result})


# 탈퇴 완료 후 화면 전환
def delete_result(request):
    return render(request, '../templates/main/delete_result.html')


# 회원가입
class CustomSignupView(SignupView):
    template_name = "main/signup.html"

    # 이메일 인증을 위한 form 검사
    def form_valid(self, form):
        self.user = form.save(self.request)
        current_site = get_current_site(self.request)
        message = render_to_string('main/activation_email.html', {
            'user': self.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': member_activation_token.make_token(self.user),
        })
        mail_title = "계정 본인확인 이메일"
        mail_to = self.request.POST["email"]
        email = EmailMessage(mail_title, message, to=[mail_to])
        email.send()
        return render(self.request, "main/signup2.html")


# 회원가입기능
# 이메일에 @ & . 없으면 안내해준다.
def validate_email(email):
    if '@' not in email or '.' not in email:
        raise ValidationError(("Invalid Email"), code='invalid')


# 이메일 활성화(비활성화) #
def activate(request, uid64, token, backend='django.contrib.auth.backends.ModelBackend', *args, **kwargs, ):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and member_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user, backend)
        return redirect("signup3")
    else:
        return render(request, '../templates/main/login.html', {'error': '계정 활성화 오류'})


class CustomSLogoutView(LogoutView):
    template_name = "main/logout.html"


class CustomSPasswordChangeView(PasswordChangeView):
    template_name = "main/password_change.html"
    success_url = reverse_lazy("mypage")


def get_redirect_url(self):
    return redirect("login")


def profile_upload(request):
    if request.method == 'POST':
        user_id = request.session['id']
        user = User.objects.get(id=user_id)
        img = request.FILES['file']
        user.profile_photo = img
        user.profile_s3_url = "https://photomarble.s3.ap-northeast-2.amazonaws.com/profile/" + str(img)
        user.save()
    return redirect('mypage')


def signup3(request):
    return render(request, "../templates/main/signup3.html")


# About PhotoMarble 사용가이드 페이지
def about_pm(request):
    return render(request, "../templates/main/about_pm.html")
