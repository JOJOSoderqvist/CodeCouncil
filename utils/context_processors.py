from app.models import Tag, Profile


def fetch_popular_tags(request):
    popular_tags_objects = Tag.objects.get_popular_tags()
    popular_tags = [tag['name'] for tag in popular_tags_objects]
    return {'tags': popular_tags}


def fetch_popular_users(request):
    popular_profiles_objects = Profile.objects.get_popular_profiles()
    popular_profiles = [profile['displayed_name'] for profile in popular_profiles_objects]
    return {'profiles': popular_profiles}
