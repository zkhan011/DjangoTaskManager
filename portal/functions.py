# coding: UTF-8
# Copyright: Dmitriy Antonenko 2017


from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile, ActionType, SystemLog

def get_user_permissions(user):
    """

    :param user:
    :return: permissions (array)
    """
    permissions = []

    try:
        profile = UserProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        return permissions

    for p in profile.direct_access.all():
        permissions.append(p)

    for r in profile.roles.all():
        for p in r.permissions.all():
            permissions.append(p)

    return permissions


def can_do(user, action):
    """
    Function check user Authorization to proceed action

    :param user: object User
    :param action: action to check Authorization to do
            can be string (like "Can do something") or Inteder (field code on model)
    :return: True or False
    """

    # нужно получить список PermissionsType из User.role.permissions и User.direct_access
    # и проверить есть ли там action

    #if user.is_superuser:
    #    return True

    try:
        action = int(action)
        # action is integer
        try:
            action_obj = ActionType.objects.get(code=action)
        except ObjectDoesNotExist:
            return False

    except ValueError:
        # action is string
        try:
            action_obj = ActionType.objects.get(name=action)
        except ObjectDoesNotExist:
            return False

    permissions = get_user_permissions(user)

    if action_obj in permissions:
        return True
    else:
        return False


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def syslog(request,  action, level='info'):
    """
    Adds a record to system ivents log

    user,     dated,     action
    contents,     page,     url,    ip
    :return:
    """

    log = SystemLog()

    try:
        log.user = request.user
    except :
        log.user = None

    log.action = action
    log.url = request.path
    log.ip = get_user_ip(request)
    log.content = request.META.get('QUERY_STRING')
    log.level = level.upper()

    log.save()
