class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return self.quantity >= quantity


    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity) is True:
            self.quantity -= quantity
            return self.quantity
        else:
            raise ValueError("Товара не хватает на складе")


    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, quantity=1):
        """
        нужно реализовать метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if quantity > 0 and isinstance(quantity, int):
            if product in self.products:
                self.products[product] += quantity
            else:
                self.products[product] = quantity
            return self.products
        else:
            raise ValueError("Количество товара должно быть целым положительным числом")

    def remove_product(self, product: Product, quantity=None):
        """
        Метод удаления продукта из корзины.
        Если quantity не передан, то удаляется вся позиция
        Если quantity больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if quantity is None:
            self.products.pop(product, None)
        elif quantity >= self.products.get(product, 0):
            self.products.pop(product, None)
        else:
            self.products[product] -= quantity
        return self.products

    def clear(self):
        self.products = {}
        return self.products

    def get_total_price(self) -> float:
        total_price = 0.0
        for product, quantity in self.products.items():
            price = product.price * quantity
            total_price += price
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product, quantity in self.products.items():
            if product.check_quantity(quantity) is True:
                product.buy(quantity)
            else:
                raise ValueError('Товара не хватает на складе')
        self.clear()

