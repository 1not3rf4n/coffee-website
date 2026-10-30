from apps.shop.models import Product

CART_SESSION_ID = 'coffee_shop_cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, grind_type="دانه کامل", override_quantity=False):
        product_id = str(product.id)
        item_key = f"{product_id}_{grind_type}"
        
        if item_key not in self.cart:
            self.cart[item_key] = {
                'product_id': product.id,
                'title': product.title,
                'price': product.final_price,
                'quantity': 0,
                'grind_type': grind_type,
                'image_url': product.image.url if product.image else (product.image_url or '/static/images/default-coffee.jpg')
            }
        
        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
