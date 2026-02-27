from turbo_quiz import text_check, length_check, format_check

def test_text_check():
    assert text_check("James") == True
    assert text_check("Bob") == True
    assert text_check("") == False

def test_length_check():
    assert length_check("James") == True
    assert length_check("A") == True
    assert length_check("A" * 25) == True
    assert length_check("A" * 26) == False

def test_format_check():
    assert format_check("James") == True
    assert format_check("James Smith") == True
    assert format_check("James!!!") == False
    assert format_check("Bob1000") == False