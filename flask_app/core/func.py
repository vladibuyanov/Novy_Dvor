from flask import session

from flask_app.core.models.item import Items


def add_in_cart_func(product):
    if product not in session['card']:
        session['card'][product] = 1
    else:
        session['card'][product] += 1


def cart_func():
    ordered_items_dict = session.get('card', [])
    ordered_items = Items.query.filter(Items.id.in_(ordered_items_dict.keys())).all()
    ordered_items_with_count = [
        [
            item,  # Модель товара
            ordered_items_dict[str(item.id)],  # Количество
            int(item.price) * ordered_items_dict[str(item.id)]  # Цена
        ]
        for item in ordered_items
    ]
    total_price = sum(pair[2] for pair in ordered_items_with_count)
    return ordered_items_with_count, total_price
