# from django.shortcuts import render, HttpResponseRedirect
# from django.contrib import auth
# from django.urls import reverse
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
#
# from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
# from baskets.models import Basket
from django.contrib import auth
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy

from common.views import CommonContextMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from baskets.models import Basket
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
# from django.db import transaction
# from users.forms import ShopUserProfileEditForm
# from authapp.forms import ShopUserEditForm




class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались!'
    title = 'GeekShop - Регистрация'

    def send_verify_link(self, user):                                                               # (1)
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        subject = f'Для активации пользователя {user.username} пройдите по ссылке'
        message = f'Для потверждения учетной записи {user.username} на портале\n' \
                  f'{settings.DOMAIN_NAME} пройдите по ссылке {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def get_context_data(self, **kwargs):
        title = 'регистрация'
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context.update(
            title=title,
            form=self.form_class()
        )
        return context

    def post(self, request, *args, **kwargs):
        register_form = self.form_class(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            self.send_verify_link(user)
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return super().get(request, *args, **kwargs)

def verify(request, email, activate_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activate_key and not user.is_activation_key_expired:
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save(update_fields=['activation_key', 'activation_key_expires', 'is_active'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/verification.html')
    except Exception as e:
        print(e)
    return render(request, 'users/verification.html')

class UserProfileView(CommonContextMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'GeekShop - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class UserLogoutView(LogoutView):
    pass


# @transaction.atomic
# def edit(request):
#     title = 'Редактирование'
#
#     if request.method == 'POST':
#         edit_form = ShopUserEditForm(request.POST, request.FIELS, instance=request.user)
#         profile_form = ShopUserProfileEditForm(request.POST, instance=request.users.shopuserprofile)
#         if edit_form.is_valid() and profile_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('auth:edit'))
#     else:
#         edit_form = ShopUserEditForm(instance=request.user)
#         profile_form = ShopUserProfileEditForm(instance=request.users.shopuserprofile)
#
#     content = {
#         'title': title,
#         'edit_form': edit_form,
#         'profile_form': profile_form
#     }
#
#     return render(request, 'users/edit.html', content)



# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 print(form.errors)
#     else:
#         form = UserLoginForm()
#     context = {'title': 'GeekShop - Авторизация', 'form': form}
#     return render(request, 'users/login.html', context)
#
#
# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация прошла успешно!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'title': 'GeekShop - Регистрация', 'form': form}
#     return render(request, 'users/registration.html', context)
#
#
# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(instance=user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#
#     context = {
#         'title': 'GeekShop - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=user)
#     }
#     return render(request, 'users/profile.html', context)
#
#
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))