from datetime import datetime
from .models import Category


def global_context(request):
    current_year = datetime.now().year
    categories = Category.objects.all()
    return {
        'current_year': current_year,
        'categories': categories
    }
