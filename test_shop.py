"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100.0, "This is a book", 1000)


@pytest.fixture
def product2():
    return Product("cup", 200.0, "This is a cup", 500)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_True(self, product):
        assert product.check_quantity(1000), " возвращает False, хотя товара хватает на складе"

    def test_product_check_quantity_False(self, product):
        assert product.check_quantity(1001) is False, " возвращает True, хотя товара не хватает на складе"

    def test_product_check_quantity_0_True(self, product):
        assert product.check_quantity(0), " возвращает False, хотя товара  хватает на складе"

    def test_product_buy(self, product):
        assert product.buy(1000) == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match="Товара не хватает на складе"):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_new_product(self, product):
        cart = Cart()

        cart.add_product(product)
        assert cart.products == {product: 1}

    def test_add_product_increase_product_quantity(self, product):
        cart = Cart()
        first_quantity = 4
        second_quantity = 6

        cart.add_product(product, first_quantity)
        cart.add_product(product, second_quantity)
        assert cart.products == {product: first_quantity + second_quantity}

    def test_add_product_different_products(self, product, product2):
        cart = Cart()
        first_quantity = 1
        second_quantity = 2

        cart.add_product(product, first_quantity)
        cart.add_product(product2, second_quantity)
        assert cart.products == {product: first_quantity, product2: second_quantity}
        # for product, quantity in cart.products.items():
        # assert(f"{product.name}, {product.price:.1f}, {product.description}: {quantity}") == "book, 100.0, This is a book: 10"

    def test_add_product_with_unvalid_quantity(self, product):
        cart = Cart()
        unvalid_quantity = 0

        with pytest.raises(ValueError, match="Количество товара должно быть целым положительным числом"):
            cart.add_product(product, unvalid_quantity)

    def test_remove_product_without_quantity(self, product):
        cart = Cart()

        cart.products = {product: 3}
        cart.remove_product(product)
        assert cart.products == {}

    def test_remove_product_with_quantity(self, product):
        cart = Cart()
        initial_quantity = 300
        quantity_to_be_removed = 200

        cart.products = {product: initial_quantity}
        cart.remove_product(product, quantity_to_be_removed)
        assert cart.products == {product: initial_quantity - quantity_to_be_removed}

    def test_remove_product_with_quantity_more_than_in_cart(self, product):
        cart = Cart()
        initial_quantity = 200
        quantity_to_be_removed = 300

        cart.products = {product: initial_quantity}
        cart.remove_product(product, quantity_to_be_removed)
        assert cart.products == {}

    def test_remove_product_with_quantity_equal_in_cart(self, product):
        cart = Cart()
        initial_quantity = 200
        quantity_to_be_removed = 300

        cart.products = {product: initial_quantity}
        cart.remove_product(product, quantity_to_be_removed)
        assert cart.products == {}

    def test_clear(self, product, product2):
        cart = Cart()

        cart.products = {product: 200, product2: 300}
        cart.clear()
        assert cart.products == {}

    def test_clear_empty_cart(self):
        cart = Cart()

        cart.products = {}
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, product, product2):
        cart = Cart()
        first_quantity = 200
        second_quantity = 300

        cart.products = {product: first_quantity, product2: second_quantity}
        total_price = cart.get_total_price()
        assert total_price == product.price * first_quantity + product2.price * second_quantity

    def test_buy(self, product, product2):
        cart = Cart()
        first_quantity = 900
        second_quantity = 400
        final_quantity_first_product = product.quantity - first_quantity
        final_quantity_second_product = product2.quantity - second_quantity

        cart.products = {product: first_quantity, product2: second_quantity}
        cart.buy()
        assert product.quantity == final_quantity_first_product
        assert product2.quantity == final_quantity_second_product
        assert cart.products == {}

    def test_buy_more_than_available(self, product, product2):
        cart = Cart()
        first_quantity = 1000
        second_quantity = 501

        cart.products = {product: first_quantity, product2: second_quantity}
        assert product.quantity == first_quantity
        with pytest.raises(ValueError, match="Товара не хватает на складе"):
            cart.buy()
