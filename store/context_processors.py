from .models import Category  # or wherever your Category model is

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}