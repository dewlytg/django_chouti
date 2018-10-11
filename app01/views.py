from django.shortcuts import render,HttpResponse,redirect
from app01 import forms
from utils import handler,check_code
from app01 import models
import datetime
import json
import pytz
from io import BytesIO
from django.db.models import F,Q

# Create your views here.

def create_code_img(request):
    #在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img,code = check_code.create_code()
    request.session['check_code'] = code
    img.save(f,'PNG')
    return HttpResponse(f.getvalue())


def auth(func):
    def inner(request,*args,**kwargs):
        user = request.session.get("user")
        if user:
            return func(request,user,*args,**kwargs)
        else:
            return redirect("/index.html")
    return inner


def index(request):
    if request.method == "GET":
        obj = forms.LoginForm()
        obj2 = forms.RegisterForm()
        obj3 = forms.RegisterEmail()
        return render(request, "index.html", {"obj":obj,"obj2":obj2,"obj3":obj3})


def login(request):
    if request.method == "POST":
        msg = handler.BaseResponse()
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            _login_values = form.cleaned_data

            q1 = Q()
            # q1.connector = "OR"
            q1.children.append(("user",_login_values["user"]))

            q2 = Q()
            # q2.connector = "OR"
            q2.children.append(("email",_login_values["user"]))

            con = Q()
            con.add(q1,"OR")
            con.add(q2,"OR")

            c = models.UserInfo.objects.filter(con)
            if c:
                if request.POST.get("code") == request.session.get("check_code"):

                    obj = models.UserInfo.objects.get(con)
                    request.session["is_login"] = True
                    request.session["user"] = _login_values
                    rep = HttpResponse(json.dumps(msg.__dict__))
                    if request.POST.get("keepup-login"):
                        request.session.set_expiry(3)
                        rep.set_cookie("user", obj.user,max_age=86400*30)
                    else:
                        rep.set_cookie("user", obj.user)
                    return rep
                else:
                    msg.status = False
                    msg.errors = {"code":[{"message":"验证码错误"}]}
            else:
                msg.status = False
                msg.summary = "用户名或者密码错误"
        else:
            msg.status = False
            msg.errors = json.loads(form.errors.as_json())
        return HttpResponse(json.dumps(msg.__dict__))


def email(request):
    if request.method == "POST":
        msg = handler.BaseResponse()
        current_time = datetime.datetime.now()
        form = forms.RegisterEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            u_c = models.UserInfo.objects.filter(email=email).count()
            if u_c:
                msg.status = False
                msg.summary = "该邮箱已经注册"
            else:
                m_c = models.SendMsg.objects.filter(email=email).count()
                if m_c:
                    m_obj = models.SendMsg.objects.get(email=email)
                    previous_one_hour = current_time - datetime.timedelta(hours=1)
                    previous_one_hour = previous_one_hour.replace(tzinfo=pytz.timezone('UTC'))
                    code = handler.generator_verification_code()
                    if m_obj.last_time > previous_one_hour:
                        if m_obj.times == 10:
                            msg.status = False
                            msg.summary = "一小时之内只能注册10次，超过限制"
                        else:
                            models.SendMsg.objects.filter(email=email).update(code=code, last_time=current_time,times=F("times") + 1)
                            # handler.send_mail(email, code)
                    else:
                        models.SendMsg.objects.filter(email=email).update(code=code, last_time=current_time, times=1)
                        handler.send_mail(email, code)
                else:
                    code = handler.generator_verification_code()
                    models.SendMsg.objects.create(code=code,email=email,last_time=current_time,times=1)
                    # handler.send_mail(email,code)
        else:
            msg.status = False
            msg.summary = form.errors["email"][0]
        return HttpResponse(json.dumps(msg.__dict__))


def register(request):
    if request.method == "POST":
        msg = handler.BaseResponse()
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            _reg_values = form.cleaned_data
            current_time = datetime.datetime.now()
            c = models.SendMsg.objects.filter(last_time__gt=(current_time - datetime.timedelta(minutes=1))).count()
            if not c:
                msg.status = False
                msg.errors = {"verification_code":[{"message":"你的验证码已经失效"}]}
                return HttpResponse(json.dumps(msg.__dict__))
            else:
                u_c = models.UserInfo.objects.filter(Q(user=_reg_values["user"])|Q(email=_reg_values["email"]))
                if u_c:
                    msg.status = False
                    msg.summary = "用户名或者邮箱已经注册过"
                    return HttpResponse(json.dumps(msg.__dict__))
                else:
                    _reg_values.pop("verification_code")
                    models.UserInfo.objects.create(**_reg_values)
                    models.SendMsg.objects.filter(email=_reg_values["email"]).delete()
                    request.session["is_login"] = True
                    request.session["user"] = _reg_values
                    rep = HttpResponse(json.dumps(msg.__dict__))
                    rep.set_cookie("user",_reg_values["user"])
                    return rep
        else:
            msg.status = False
            msg.errors = json.loads(form.errors.as_json())
            return HttpResponse(json.dumps(msg.__dict__))


def logout(request):
    request.session.clear()
    rep = redirect("/index.html")
    rep.delete_cookie("user")
    return rep


def test(request):
    return render(request,"test.html")