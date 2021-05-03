from lc.data_retrieval import form_url


def test_form_url():
    test_line = "victoria"
    expected_output = f"https://api.tfl.gov.uk/Line/{test_line}/Disruption"
    assert form_url(test_line) == expected_output
