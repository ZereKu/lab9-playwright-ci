import pytest
from playwright.sync_api import expect


# Случаи 1–8: граница бесплатной доставки 10000 для города и региона
@pytest.mark.parametrize("amount, zone, fee, total", [
    (0, "city", 1000, 1000),
    (9999, "city", 1000, 10999),
    (10000, "city", 0, 10000),
    (10001, "city", 0, 10001),
    (0, "region", 2000, 2000),
    (9999, "region", 2000, 11999),
    (10000, "region", 0, 10000),
    (10001, "region", 0, 10001),
])
def test_delivery(page, amount, zone, fee, total):
    page.get_by_label("Сумма заказа").fill(str(amount))
    page.get_by_label("Зона доставки").select_option(zone)
    page.get_by_role("button", name="Рассчитать").click()
    result = page.get_by_role("status")
    expect(result).to_be_visible()
    expect(result).to_have_text(
        f"Доставка: {fee} ₸. К оплате: {total} ₸."
    )
    expect(page.get_by_role("alert")).to_be_hidden()


# Случаи 9–11: пустая строка, отрицательное и дробное число
@pytest.mark.parametrize("amount", ["", "-1", "12.5"])
def test_invalid_amount(page, amount):
    page.get_by_label("Сумма заказа").fill(amount)
    page.get_by_role("button", name="Рассчитать").click()
    error = page.get_by_role("alert")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Введите целое неотрицательное число"
    )
    expect(page.get_by_role("status")).to_be_hidden()


# Случай 12: расчёт, затем сброс формы в начальное состояние
def test_reset(page):
    amount = page.get_by_label("Сумма заказа")
    zone = page.get_by_label("Зона доставки")
    amount.fill("5000")
    zone.select_option("region")
    page.get_by_role("button", name="Рассчитать").click()
    expect(page.get_by_role("status")).to_have_text(
        "Доставка: 2000 ₸. К оплате: 7000 ₸."
    )

    page.get_by_role("button", name="Сбросить").click()
    expect(amount).to_have_value("")
    expect(zone).to_have_value("city")
    expect(page.get_by_role("alert")).to_be_hidden()
    expect(page.get_by_role("status")).to_be_hidden()
