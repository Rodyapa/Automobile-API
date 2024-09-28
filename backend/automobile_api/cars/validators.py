from django.core.validators import RegexValidator


class TitleValidator(RegexValidator):
    regex = r"^[A-zА-я0-9-\s]+$"
    message = ("В названии допустимы: "
               "кириллица и латинские символы, "
               "арабские цифры, пробел, а также дефис.")


class TextValidator(RegexValidator):
    regex = r"^[:;.,?!A-zА-я0-9-\s]+$"
    message = ("В текстовом описании допустимы: "
               "кириллица и латинские символы, "
               "арабские цифры, пробел, знаки препинания, "
               "а также дефис.")


class CarYearValidator(RegexValidator):
    regex = r"^[0-9]{4}$"
    message = "Год должен состоять из 4 арабских цифр."
