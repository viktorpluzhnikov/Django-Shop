# import random, hashlib
# from django.contrib.auth.forms import UserCreationForm
#
#
# class ShopUserRegisterForm(UserCreationForm):
#
#     def save(self):
#         user = super(ShopUserRegisterForm, self).save()
#         user.is_active = False
#         salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
#         user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
#         user.save()
#         return user
