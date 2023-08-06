from autocast import becomes, coerces


def test_noop():
    @coerces
    def fun(x: int) -> int:
        assert not isinstance(x, int)
        return x

    fun("5")
    fun(x=5.0)


def test_simple_coercion():
    @coerces
    def fun(x: becomes[int]) -> None:
        assert isinstance(x, int)

    fun("5")
    fun(x=5.0)
