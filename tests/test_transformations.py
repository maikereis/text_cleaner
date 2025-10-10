from text_cleaner.transformations import (
    RemoveAccents,
    RemoveDateTime,
    RemoveEmails,
    RemoveEmojis,
    RemoveLongAlphanumerics,
    RemoveLongNumbers,
    RemoveNonAsciiExceptAccents,
    RemoveSubstrings,
    RemoveUserIDs,
    ReplaceMultipleSpaces,
    StripWhitespace,
)


def test_strip_whitespace():
    t = StripWhitespace()
    assert t.apply("  hello  ") == "hello"
    assert t.apply("\n\t hi \t\n") == "hi"
    assert t.apply("") == ""


def test_replace_multiple_spaces():
    t = ReplaceMultipleSpaces()
    assert t.apply("hello   world") == "hello world"
    assert t.apply("a \t  b   c") == "a b c"
    assert t.apply("no_spaces") == "no_spaces"


def test_remove_accents():
    t = RemoveAccents()
    assert t.apply("ação") == "acao"
    assert t.apply("Mañana") == "Manana"
    assert t.apply("naïve café") == "naive cafe"
    assert t.apply("") == ""


def test_remove_non_ascii_except_accents():
    t = RemoveNonAsciiExceptAccents()
    # keeps letters, removes emojis and symbols
    assert t.apply("café ☕") == "café "
    assert t.apply("naïve – test") == "naïve  test"  # en dash removed
    assert t.apply("纯中文text") == "text"  # removes non-Latin letters


def test_remove_emojis():
    t = RemoveEmojis()
    assert t.apply("hello 😊 world 🌍") == "hello  world "
    assert t.apply("no emoji") == "no emoji"
    assert t.apply("") == ""


def test_remove_emails():
    t = RemoveEmails()
    assert t.apply("contact me at user@example.com please") == "contact me at  please"
    assert t.apply("no email here") == "no email here"
    assert t.apply("multiple a@b.com and c@d.org") == "multiple  and "


def test_remove_user_ids():
    t = RemoveUserIDs()
    assert t.apply("user u12345 reported issue") == "user  reported issue"
    assert t.apply("User U9876 logged in") == "User  logged in"
    assert t.apply("no id here") == "no id here"


def test_remove_long_numbers():
    t = RemoveLongNumbers()
    assert t.apply("protocol 12345678901 invalid") == "protocol  invalid"
    assert t.apply("short number 1234 remains") == "short number 1234 remains"
    assert t.apply("mix 99999999999 and 12345") == "mix  and 12345"


def test_remove_long_alphanumerics():
    t = RemoveLongAlphanumerics()
    assert t.apply("hash 7434000304c3745cddbee9251a9cb6f5 found") == "hash  found"
    assert t.apply("short abc123 stays") == "short abc123 stays"
    assert t.apply("A1B2C3D4E5F6G7H8I9J0K1L2M3N4") == ""


def test_remove_datetime():
    t = RemoveDateTime()
    assert t.apply("Event on 17/05/2025 17:56:50 happened") == "Event on  happened"
    assert t.apply("Date 01/01/2020 00:00:00 end") == "Date  end"
    assert t.apply("No date here") == "No date here"


def test_remove_substrings_case_insensitive():
    t = RemoveSubstrings(["CONFIDENCIAL", "TESTE"])
    result = t.apply("Documento confidencial de teste")
    assert result == "Documento  de "


def test_remove_substrings_multiple_occurrences():
    t = RemoveSubstrings(["abc"])
    assert t.apply("abcabcABCdef") == "def"


def test_remove_substrings_empty_list():
    t = RemoveSubstrings([])
    assert t.apply("no change") == "no change"


def test_remove_substrings_empty_text():
    t = RemoveSubstrings(["abc"])
    assert t.apply("") == ""
