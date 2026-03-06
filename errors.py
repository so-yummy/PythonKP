class InputValidationError(Exception):
    """Ошибка, связанная с некорректным вводом пользователя."""


def safe_int(value, field_name: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """
    Надёжное преобразование строки в целое число с проверками диапазона.

    :param value: строка из поля ввода
    :param field_name: название поля для понятного сообщения об ошибке
    :param min_value: минимально допустимое значение (если задано)
    :param max_value: максимально допустимое значение (если задано)
    :return: целое число
    :raises InputValidationError: при некорректном вводе или выходе за диапазон
    """
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        raise InputValidationError(f"{field_name}: введите целое число") from None

    if min_value is not None and ivalue < min_value:
        raise InputValidationError(
            f"{field_name}: значение должно быть не меньше {min_value}"
        )

    if max_value is not None and ivalue > max_value:
        raise InputValidationError(
            f"{field_name}: значение должно быть не больше {max_value}"
        )

    return ivalue


if __name__ == "__main__":
    # Простейший ручной тест модуля, чтобы можно было проверить обработку ошибок отдельно.
    samples = [
        ("10", "Размер ключа", 8, 4096),
        ("abc", "Размер ключа", 8, 4096),
        ("4", "Размер ключа", 8, 4096),
        ("10000", "Размер ключа", 8, 4096),
        ("", "Размер ключа", 8, 4096),
        ("", "Количество экспериментов", 1, 1000),
        ("100", "Количество экспериментов", 1, 1000),
    ]

    for raw, name, mn, mx in samples:
        print(f"Проверка: {name} = {raw!r}")
        try:
            value = safe_int(raw, name, mn, mx)
            print("  OK ->", value)
        except InputValidationError as e:
            print("  Ошибка ->", e)

