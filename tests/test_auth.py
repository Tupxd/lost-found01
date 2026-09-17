import re

import app


def test_valid_personal_email_passes():
    assert app.is_valid_email("student@gmail.com") is True
    assert app.is_valid_email("student@outlook.com") is True
    assert app.is_valid_email("student.name+tag@hotmail.com") is True


def test_invalid_email_is_rejected():
    assert app.is_valid_email("not-an-email") is False
    assert app.is_valid_email("student@") is False
    assert app.is_valid_email("@gmail.com") is False


def test_student_lookup_by_personal_email_works():
    student_id = app.find_student_by_email("student1@gmail.com")
    assert student_id == "65001"


def test_otp_generation_is_six_digits():
    otp = app.generate_otp()
    assert len(otp) == 6
    assert re.fullmatch(r"\d{6}", otp) is not None
    assert 100000 <= int(otp) <= 999999
