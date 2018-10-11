from django import forms
from app01 import models


class LoginForm(forms.Form):
    user = forms.RegexField(
        max_length=64,
        min_length=3,
        # regex='^1[0-9]{10}$', # 手机号
        regex=r'^[a-zA-Z0-9_]+(@[a-zA-Z0-9.]+)?$', # 邮箱格式
        error_messages={"min_length":"最小不能少于3位", "max_length":"最长不能是12位", "invalid":"你的用户名格式不对", "required":"请输入用户名"},

    )

    pwd = forms.CharField(
        max_length=32,
        label="密码",
        widget=forms.PasswordInput(attrs={"class":"tb","placeholder":"密码","name":"pwd","id":"login_pwd"}),
        error_messages={"required": "请输入密码"},
    )

    code = forms.CharField(
        max_length=4,
        error_messages={"required":"请输入验证码"},
        widget=forms.TextInput(attrs={"class":"tb","placeholder":"验证码","name":"code","id":"login_code"})
    )

    user.widget.attrs.update({'class': 'tb',"placeholder":"用户名或者邮箱","name":"username","id":"login_user"})

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
    #     self.fields['login_region'] = forms.TypedChoiceField(
    #         coerce=lambda x:int(x),
    #         choices=models.Region.objects.all().values_list("region_id","region_name"),
    #         widget=forms.Select(attrs={"class":"region"}))


class RegisterEmail(forms.Form):
    email = forms.RegexField(
        # regex='^1[0-9]{10}$', # 手机号
        regex=r'^[a-zA-Z0-9_]+@[a-zA-Z0-9.]+$',  # 邮箱格式
        error_messages={"invalid":"你的邮箱格式不对","required":"请输入邮箱"},
    )

    email.widget.attrs.update({'class': 'register-mobile',"placeholder":"邮箱"})


class RegisterForm(forms.Form):
    user = forms.RegexField(
        max_length=64,
        min_length=3,
        # regex='^1[0-9]{10}$', # 手机号
        regex=r'^[a-zA-Z0-9_]+$',  # 邮箱格式
        error_messages={"min_length":"最小不能少于3位","max_length":"最长不能是12位","invalid":"你的用户名格式不对","required":"请输入用户名"},
    )

    user.widget.attrs.update({'class': 'tb',"placeholder":"用户名"})

    email = forms.RegexField(
        # regex='^1[0-9]{10}$', # 手机号
        regex=r'^[a-zA-Z0-9_]+@[a-zA-Z0-9.]+$',  # 邮箱格式
        error_messages={"invalid":"你的邮箱格式不对","required":"请输入邮箱"},
    )

    pwd = forms.CharField(
        max_length=32,
        label="密码",
        widget=forms.PasswordInput(attrs={"class":"tb","placeholder":"密码","name":"pwd"}),
        error_messages={"min_length": "最小不能少于3位", "max_length": "最长不能是12位", "required": "请输入密码"},
    )

    verification_code = forms.CharField(
        error_messages={"required": "请输入验证码"},
        widget=forms.TextInput(attrs={"class":"tb","name":"verification-code","placeholder":"验证码"})
    )

    # def __init__(self, *args, **kwargs):
    #     super(RegisterForm, self).__init__(*args, **kwargs)
    #     self.fields['reg_region'] = forms.TypedChoiceField(
    #         coerce=lambda x:int(x),
    #         choices=models.Region.objects.all().values_list("region_id","region_name"),
    #         widget=forms.Select(attrs={"class":"region"}))



