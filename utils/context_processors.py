from django.utils import timezone

def nowtime(request):
    return{
        'now':timezone.now()
    }