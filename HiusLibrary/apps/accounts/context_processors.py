from .models import Account


def nav_cats(request):
    if request.user.is_authenticated:
        return {
            'name': request.user.name,
            'image' : request.user.profile_image,
            'is_admin': request.user.is_admin,
        }
    return {}