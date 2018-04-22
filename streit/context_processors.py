# coding: utf-8

from streit.settings import PROJECT_NAME, PROJECT_VERSION

#from streit.functions import can_do


def site_common_values(request):
    # return the value you want as a dictionnary. you may add multiple values in there.

    values ={
        'PROJECT_NAME': PROJECT_NAME,
        'PROJECT_VERSION': PROJECT_VERSION,
    }

    return values


def site_menu(request):
    """
    Spliting menu paths
    :param request:
    :return:
    """
    try:
        sub_menu = request.path.split('/')[2]
    except:
        sub_menu = ''

    return {
            'main_menu': request.path.split('/')[1] ,
            #'sub_menu' : request.path.split('/')[2],
            'sub_menu': sub_menu,
            }


# def user_access_permissions(request):
#     # TODO: переделать брать ассеss permissions ОДИН раз при login и хранить в сессии
#
#     permissions = {}
#     if request.user.is_authenticated():
#         permissions['2200'] = can_do(request.user, '2200')
#
#     return {'u_access': permissions,}

