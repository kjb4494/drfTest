from django import forms
from django.utils.translation import ugettext_lazy as _
from testapp.models import CmbUser, Modifier, UserHasModifier

default_errors = {
    'required': _('필수입력 항목입니다.'),
    'invalid': _('올바른 값을 입력해주세요.'),
    'username_exists': _('이미 존재하는 유저명입니다.'),
}


class CmbUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label=_('유저명'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': _('유저명을 입력해주세요.'),
                'required': 'True'
            }
        ),
        error_messages=default_errors
    )
    country = forms.CharField(
        label=_('국가'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': _('국가를 입력해주세요.'),
                'required': 'True'
            }
        ),
        error_messages=default_errors
    )
    point = forms.IntegerField(
        label=_('할당 가능 포인트'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': _('할당 가능 포인트를 입력해주세요.'),
                'required': 'True'
            }
        ),
        error_messages=default_errors
    )
    password = forms.CharField(
        label=_('비밀번호'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': _('비밀번호를 입력해주세요.'),
                'required': 'True'
            }
        ),
        error_messages=default_errors
    )
    password_confirm = forms.CharField(
        label=_('비밀번호 확인'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': _('비밀번호 확인을 입력해주세요.'),
                'required': 'True'
            }
        ),
        error_messages=default_errors
    )

    class Meta:
        model = CmbUser
        fields = ('username', 'country', 'point', 'password', 'password_confirm')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            CmbUser.objects.get(username=username)
            raise forms.ValidationError(
                default_errors['username_exists'],
                code='username_exists',
            )
        except CmbUser.DoesNotExist:
            return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("비밀번호를 다시 확인해주세요.")
        return password_confirm

    def save(self, commit=True):
        user = super(CmbUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])
        user.country = self.cleaned_data['country']
        user.point = self.cleaned_data['point']
        if commit:
            user.save()
            bulk_bucket = []
            modifier_list = Modifier.objects.all()
            for modifier in modifier_list:
                bulk_bucket.append(UserHasModifier(
                    user=user,
                    modifier=modifier
                ))
            UserHasModifier.objects.bulk_create(bulk_bucket)
        return user


class CmbUserChangeForm(forms.ModelForm):
    country = forms.CharField(
        label=_('국가'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': _('국가를 입력해주세요.'),
                'required': 'True'
            }
        ),
        error_messages=default_errors
    )
    point = forms.IntegerField(
        label=_('할당 가능 포인트'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': _('할당 가능 포인트를 입력해주세요.'),
                'required': 'True'
            }
        ),
        error_messages=default_errors
    )

    class Meta:
        model = CmbUser
        fields = ('country', 'point')
