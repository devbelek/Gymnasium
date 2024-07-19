from allauth.account.adapter import DefaultAccountAdapter
import logging

logger = logging.getLogger('main')

class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(MyAccountAdapter, self).save_user(request, user, form, commit)
        logger.info(f'Зарегистрирован новый пользователь: {user.username}')
        return user