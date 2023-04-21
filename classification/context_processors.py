from . models import Classification

def menu_links(request):
    links = Classification.objects.all()
    return dict(links=links)
