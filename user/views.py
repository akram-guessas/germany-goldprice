from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from blog.models import Post
from .models import Item,Customer,Vendor
from .forms import UserCreationForm,LoginForm,UserUpdateForm,ProfileUpdateForm,ItemCreateForm,CustomerSignUpForm,VendorSignUpForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from deep_translator import GoogleTranslator
from datetime import datetime
from .filters import ItemFilter
from django.urls import reverse
from django.urls import reverse_lazy

from django.conf import settings
User = settings.AUTH_USER_MODEL

def SingUp(request):
    context = {
        'title': 'تسجيل حساب'
    }
    return render(request,'user/singup.html',context)

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'user/customer_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('user:login')

class VendorSignUpView(CreateView):
    model = User
    form_class = VendorSignUpForm
    template_name = 'user/vendor_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('user:login')

def index(request):
    items = Item.objects.all()
    f = ItemFilter(request.GET, queryset=items)
    items = f.qs
    
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_page)
    
    now = datetime.now().strftime("%d %B %Y")
    time = datetime.now().strftime("%H:%M") + ' AM'
    month = now.split()[1]
    translated = GoogleTranslator(source='auto', target='ar').translate(month)
    date_now = now.replace(month,translated) 
    
    context = {
        'title': 'متجر الذهب في ألمانيا',
        'items': items,
        'filter': f,
        'page': page,
        'date': date_now,
    }
    return render(request,'user/store.html',context)

def Item_detail(request,item_name, item_id):
    item = get_object_or_404(Item,pk=item_id)
    items = Item.objects.all()
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_page)
    context = {
            'title': item,
            'item':item,
            'items': items,
    }
    
    return render(request, 'user/detail.html',context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            #username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            # messages.success(
            #    request, 'تهانينا {} لقد تمت عملية التسجيل بنجاح.'.format(username))
            messages.success(
                request, f'تهانينا {new_user} لقد تمت عملية التسجيل بنجاح.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {
        'title': 'التسجيل',
        'form': form,
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:profile')
        else:
            messages.warning(
                request, 'هناك خطأ في اسم المستخدم أو كلمة المرور.')

    return render(request, 'user/login.html', {
        'title': 'تسجيل الدخول',
    })


def logout_user(request):
    logout(request)
    return render(request, 'user/logout.html', {
        'title': 'تسجيل الخروج'
    })


@login_required(login_url='login')
def profile(request):
    items = Item.objects.filter(author=request.user)
    item_list = Item.objects.filter(author=request.user)
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    try:
        item_list = paginator.page(page)
    except PageNotAnInteger:
        item_list = paginator.page(1)
    except EmptyPage:
        item_list = paginator.page(paginator.num_page)
    return render(request, 'user/profile.html', {
        'title': 'الملف الشخصي',
        'items': items,
        'page': page,
        'item_list': item_list,
    })


@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'تم تحديث الملف الشخصي.')
            return redirect('user:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'تعديل الملف الشخصي',
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'user/profile_update.html', context)


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    # fields = ['title', 'content']
    template_name = 'user/new_item.html'
    form_class = ItemCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class ItemUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    template_name = 'user/item_update.html'
    form_class = ItemCreateForm
    success_url = reverse_lazy('user:profile')
    success_message = f'تم تحديث معلومات المنتج بنجاح .!!!'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.author:
            return True
        else:
            return False
        
    '''def get_success_url(self):
        # view_name = 'item_update'
        # No need for reverse_lazy here, because it's called inside the method
        # return reverse_lazy(view_name, kwargs={self.kwargs.get('model_name_slug','')})
        return reverse('user:profile')'''


class ItemDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Item
    # success_url = reverse_lazy('user:profile')
    # success_message = 'تم حذف المنتج بنجاح .!!!'
    
    def test_func(self):
        item = self.get_object()
        if self.request.user == item.author:
            return True
        return False

    def get_success_url(self):
        item = self.get_object()
        
        messages.success(self.request, f"تم حذف المنتج بنجاح . {item.item_name}")
        return reverse("user:profile")
