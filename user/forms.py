from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Item, Profile, Customer, User,Vendor
from ckeditor.fields import RichTextField

class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(label='اسم المستخدم', max_length=30,
                               help_text='اسم المستخدم يجب ألا يحتوي على مسافات.')
    email = forms.EmailField(label='البريد الإلكتروني')
    first_name = forms.CharField(label='الاسم الأول')
    last_name = forms.CharField(label='الاسم الأخير')
    password1 = forms.CharField(
        label='كلمة المرور', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(
        label='تأكيد كلمة المرور', widget=forms.PasswordInput(), min_length=8)
  
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد مستخدم مسجل بهذا الاسم.')
        return cd['username']
    
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        return user

class VendorSignUpForm(UserCreationForm):
    username = forms.CharField(label='اسم المستخدم', max_length=30,
                               help_text='اسم المستخدم يجب ألا يحتوي على مسافات.')
    email = forms.EmailField(label='البريد الإلكتروني')
    first_name = forms.CharField(label='الاسم الأول')
    last_name = forms.CharField(label='الاسم الأخير')
    phone=forms.CharField(required=True,label='رقم الهاتف')
    address=forms.CharField(required=True,label='العنوان')
    password1 = forms.CharField(
        label='كلمة المرور', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(
        label='تأكيد كلمة المرور', widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد مستخدم مسجل بهذا الاسم.')
        return cd['username']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_vendor = True
        user.save()
        vendor = Vendor.objects.create(user=user)
        vendor.phone=self.cleaned_data.get('phone')
        vendor.address=self.cleaned_data.get('address')
        vendor.save()

        return vendor


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم', max_length=30,
                               help_text='اسم المستخدم يجب ألا يحتوي على مسافات.')
    email = forms.EmailField(label='البريد الإلكتروني')
    first_name = forms.CharField(label='الاسم الأول')
    last_name = forms.CharField(label='الاسم الأخير')
    password1 = forms.CharField(
        label='كلمة المرور', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(
        label='تأكيد كلمة المرور', widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد مستخدم مسجل بهذا الاسم.')
        return cd['username']


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(
        label='كلمة المرور', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الأول')
    last_name = forms.CharField(label='الاسم الأخير')
    email = forms.EmailField(label='البريد الإلكتروني')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)


class ItemCreateForm(forms.ModelForm):
    '''item_name = forms.CharField(label='عنوان المنتج')
    # item_image = forms.ImageField(label='صورة المنتج')
    price = forms.FloatField(label='سعر المنتج')
    phone_numb = forms.CharField(label='رقم الهاتف')
    address = forms.CharField(label='العنوان')
    description = forms.CharField(label='وصف المنتج', widget=forms.Textarea)

    item_image = forms.ImageField()'''
    # content = forms.CharField(label='نص التدوينة', widget=forms.Textarea)
    item_name = forms.CharField(label='عنوان المنتج')
    item_name.widget.attrs.update(size='120')
    description = forms.CharField(label='وصف المنتج', widget=forms.Textarea)
    class Meta:
        model = Item
        fields = ['item_name','item_image','price','phone_numb','address','description']
        
