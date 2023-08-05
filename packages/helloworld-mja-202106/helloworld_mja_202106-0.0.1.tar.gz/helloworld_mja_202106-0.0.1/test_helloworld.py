from helloworld import hello_name


def test_helloworld_no_params():
    assert hello_name() == "Hello!"


def test_helloworld_with_param():
    assert hello_name('Everyone') == "Hello Everyone"
