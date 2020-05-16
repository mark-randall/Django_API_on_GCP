from .models import FeedItem

def feedItem_forURLPath(request_path: str) -> FeedItem:
    request_path_id = request_path.split('/api/feed/')[1].split('/')[0]
    try:
        return FeedItem.objects.get(id=request_path_id)
    except:
        raise ValidationError('Invalid feed item id')
