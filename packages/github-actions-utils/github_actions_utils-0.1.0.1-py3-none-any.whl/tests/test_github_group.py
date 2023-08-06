from github_actions_utils.log_utils import github_group


def test_simple(capsys):
    @github_group("simple")
    def simple():
        print("Hello, world!")

    simple()
    out, err = capsys.readouterr()
    assert out == "::group::simple\nHello, world!\n::endgroup::\n"
    assert err == ""


def test_using_parameter_value(capsys):
    @github_group("$parameter_value")
    def using_parameter_value(parameter_value):
        print(parameter_value)

    using_parameter_value("Hello, world!")
    out, err = capsys.readouterr()
    assert out == "::group::Hello, world!\nHello, world!\n::endgroup::\n"
    assert err == ""


def test_using_parameter_value_with_multiple_parameters(capsys):
    @github_group("$parameter_value1 $parameter_value2")
    def using_parameter_value_with_multiple_parameters(parameter_value1, parameter_value2):
        print(parameter_value1, parameter_value2)

    using_parameter_value_with_multiple_parameters("Hello,", "world!")
    out, err = capsys.readouterr()
    assert out == "::group::Hello, world!\nHello, world!\n::endgroup::\n"
    assert err == ""


def test_using_object_attributes(capsys):
    class TestObject:
        def __init__(self):
            self.attribute = "Hello, world!"

    @github_group("$(obj.attribute)")
    def using_object_attributes(obj):
        print(obj.attribute)

    test_object = TestObject()
    using_object_attributes(test_object)
    out, err = capsys.readouterr()
    assert out == "::group::Hello, world!\nHello, world!\n::endgroup::\n"
    assert err == ""
