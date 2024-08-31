from password_validator import PasswordValidator


class ValidatePassword:
    """
    Класс для валидации пароля:
    Минимум символов пароля 8;
    Обязательны числа;
    Обязательны символы английской раскладки.
    """
    password_validate = PasswordValidator()
    password_validate.min(8).has().digits().has().letters()

    def __call__(self, password):
        return not self.password_validate.validate(password)


password_validate = ValidatePassword()


def transformation_phone(phone: str) -> str:
    """Функция преобразовывает номер телефона"""
    return phone if phone[:2] == '+7' else phone.replace('8', '+7', 1)
