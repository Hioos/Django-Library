from apps.accounts.models import Account


def nav_cats(request):
    if request.user.is_authenticated:
        return {
            'name': request.user.name,
            'image' : request.user.profile_image
        }
    return {}