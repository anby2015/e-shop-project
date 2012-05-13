# -*- coding: utf-8 -*-

from django import template                                                                                           
from django.utils.safestring import SafeUnicode  
from django.utils.translation import ugettext as _   
                                                                                                                             
register = template.Library()                                                                                                
                                                                                                                             
@register.filter(name='loginFilter')                                                                                                        
def loginFilter(user):                 
    """
        Shows different information according to the fact that user is logged in
        or not.
    """                                                                                   
    if user.is_authenticated():   
        s = _(u"Вы вошли как ") + user.username + "<br/><a href='/accounts/profile/'>"+u"Профиль"+"</a><br/><a href='/accounts/logout/'>"+u"Выйти"+"</a><br/>"                                                                                                      
    else:  
        s = "<a href='/accounts/registration/'>" + u"Зарегистрироваться"+"</a><br/><a href='/accounts/login/'>"+u"Войти"+"</a><br/>"
    return SafeUnicode(s) 