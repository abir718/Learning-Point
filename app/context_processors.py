from .models import Website_logo

def site_logo(request):
    try:
        logo = Website_logo.objects.first()
        print(logo)
    except Website_logo.DoesNotExist:
        logo = None
    return {'site_logo': logo}
