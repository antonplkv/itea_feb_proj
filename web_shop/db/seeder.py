from .models import (
    Category,
    Product,
    Texts,
    News
)


def create_category(**kwargs):
    required_fields = ('title', 'slug')
    [kwargs[arg] for arg in required_fields]
    return Category.objects.create(**kwargs)


def create_product(**kwargs):
    required_fields = ('title', 'slug', 'price')
    [kwargs[arg] for arg in required_fields]
    return Product.objects.create(**kwargs)


def get_category_data(unique_arg):
    return {
        'title': f'Category {unique_arg}',
        'slug': f'slug-{unique_arg}',
        'description': f'qweqweqw {unique_arg}'
    }


def get_product_data(unique_arg):
    return {
        'title': f'Category {unique_arg}',
        'slug': f'slug-{unique_arg}',
        'description': f'qweqweqw {unique_arg}',
        'price': 1000
    }