import stripe
from config.settings import STRIPE_API_KEY
from forex_python.converter import CurrencyRates


stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""
    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(amount * rate)


def create_stripe_price(amount):
    """Создает цену в страйпе"""
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Purchasing a course"},
    )

    return price

def create_stripe_session(price):
    """Создает сессию для оплаты"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )

    return session.get('id'), session.get('url')


def create_check_status_payment(session_id):
    """Реализует проверку статуса платежа"""
    session = stripe.checkout.Session.retrieve(
        session_id
    )

    return session.payment_status