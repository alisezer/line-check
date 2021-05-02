from lc.utils import check_line_name_validity

def test_check_line_name_validity_singular_success_case():
    test_name = "a"
    accepted_lines = ["a", "b"]
    assert check_line_name_validity(test_name, accepted_lines)

def test_check_line_name_validity_multiple_success_case():
    test_name = "a,b"
    accepted_lines = ["a", "b"]
    assert check_line_name_validity(test_name, accepted_lines)

def test_check_line_name_validity_singular_error_case():
    test_name = "c"
    accepted_lines = ["a", "b"]
    assert not check_line_name_validity(test_name, accepted_lines)

def test_check_line_name_validity_multiple_error_case():
    test_name = "c,d"
    accepted_lines = ["a", "b"]
    assert not check_line_name_validity(test_name, accepted_lines)
