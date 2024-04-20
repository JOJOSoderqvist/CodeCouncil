from app.models import Tag


def fetch_popular_tags(request):
    popular_tags_objects = Tag.objects.get_popular_tags()
    popular_tags = [tag['name'] for tag in popular_tags_objects]
    return {'tags': popular_tags}

