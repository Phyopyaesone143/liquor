from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def time_greeting():
    now = datetime.now().hour
    if 0 <= now < 12:      
        return ("Good Morning", "fas fa-sun")
    elif 12 <= now < 17:   
        return ("Good Afternoon", "fas fa-cloud-sun")
    elif 17 <= now < 20:   
        return ("Good Evening", "fas fa-sunset")
    else:                  
        return ("Good Night", "fas fa-moon")
