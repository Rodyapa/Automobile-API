from django.core.exceptions import ValidationError
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

    def __call__(self, value):
        regex_matches = self.regex.search(str(value))
        invalid_input = (regex_matches if self.inverse_match
                         else not regex_matches)
        if invalid_input:
            raise ValidationError(self.message, code=self.code,
                                  params={"value": value})
        elif int(value) < 1885:
            raise ValidationError(
                'Год не может быть меньше 1885.',
                code=self.code,
                params={"value": value})
