from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, UserProfileEditForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse

from authapp.models import UserProfile, ShopUser

from django.db import transaction
from authapp.forms import ShopUserProfileEditForm


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    # print('next', next)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next
    }

    return render(request, 'users/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


class UserRegisterView(TemplateView):
    template_name = 'users/registration.html'
    register_form_class = ShopUserRegisterForm
    model = ShopUser

    def send_verify_link(self, user):
        verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
        subject = f'Для активации пользователя {user.username} пройдите по ссылке'
        message = f'Для потверждения учетной записи {user.username} на портале\n' \
                  f'{settings.DOMAIN_NAME} пройдите по ссылке {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def get_context_data(self, **kwargs):
        title = 'регистрация'
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context.update(
            title=title,
            register_form=self.register_form_class()
        )
        return context

    def post(self, request, *args, **kwargs):
        register_form = self.register_form_class(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            self.send_verify_link(user)
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            return super().get(request, *args, **kwargs)


def verify(request, email, activate_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user and user.activation_key == activate_key and not user.is_activation_key_expired:
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save(update_fields=['activation_key', 'activation_key_expires', 'is_active'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        pass
    else:
        return render(request, 'authapp/verification.html')


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.users.userprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.users.userprofile)
    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}

    return render(request, 'authapp/edit.html', content)


@transaction.atomic
def edit(request):
    title = 'Редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FIELS, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.users.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.users.shopuserprofile)

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', content)







# from django.core.mail import send_mail
# from django.conf import settings
# from authapp.models import ShopUser
# from django.urls import reverse
#
#
# def send_verify_mail(user):
#     verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
#     title = f'Подтверждение учетной записи {user.username}'
#     message = f'Для подтверждения учетной записи {user.username} на портале \
#         {settings.DOMAIN_NAME} перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
#     return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
#
#
#     # if request.method == 'POST':
#     #     register_form = ShopUserRegisterForm(request.POST, request.FILES)
#     #
#     #     if register_form.is_valid():
#     #         user = register_form.save()
#     #         send_verify_link(user)
#     #         return HttpResponseRedirect(reverse('auth:login'))
#
# def register(request):
#     title = 'регистрация'
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if register_form.is_valid():
#             user = register_form.save()
#             if send_verify_mail(user):
#                 print('сообщение подтверждения отправлено')
#                 return HttpResponseRedirect(reverse('auth:login'))
#             else:
#                 print('ошибка отправки сообщения')
#                 return HttpResponseRedirect(reverse('auth:login'))
#         else:
#             register_form = ShopUserRegisterForm()
#             content = {'title': title, 'register_form': register_form}
#             return render(request, 'authapp/register.html', content)
