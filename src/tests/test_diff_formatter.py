from diff_formatter import create_html_diff


def test_marks_deletions_and_additions():
    out = create_html_diff("I has a cat", "I have a cat")
    assert "<span style='color: red;'>" in out
    assert "<span style='color: green;'>" in out


def test_escapes_html_in_text():
    out = create_html_diff("a <b>", "a <script>x</script>")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_backticks_and_quotes_do_not_break_copy_button():
    after = 'run `ls` and "say" it\'s ok'
    out = create_html_diff("x", after)
    onclick = out.split('onclick="', 1)[1].split('" style=', 1)[0]
    assert '"' not in onclick  # quotes are escaped, so the attribute stays closed
    assert "`ls`" in onclick
