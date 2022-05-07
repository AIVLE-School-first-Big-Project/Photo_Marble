import string
import re
from django.core.exceptions import ValidationError


def contains_special_character(value):
    for char in value:
        if char in string.punctuation:
            return True
    return False


def passwordCheck(value):
    if len(value) < 8 and not re.findall('[0-9]+', value) and not re.findall('[a-z]', value) or not re.findall('[A-Z]', value):
        return False
    return True


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if(
            len(password) < 8 or not passwordCheck(password) or not contains_special_character(password)
        ):
            raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다.")

    def get_help_text(self):
        return "8자 이상의 영문 대/소문자, 숫자, 특수문자 조합을 입력해 주세요.(get_help_text)"


def validate_no_special_characters(value):
    if contains_special_character(value):
        raise ValidationError("특수문자를 포함할 수 없습니다.")
