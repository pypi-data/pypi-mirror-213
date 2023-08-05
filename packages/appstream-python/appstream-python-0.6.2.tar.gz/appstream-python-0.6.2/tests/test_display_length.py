import appstream_python
import pytest


def test_compare_px() -> None:
    assert appstream_python.Component.DisplayLength(px=420, compare="eq").compare_px(420) is True
    assert appstream_python.Component.DisplayLength(px=420, compare="eq").compare_px(410) is False
    assert appstream_python.Component.DisplayLength(px=420, compare="eq").compare_px(430) is False

    assert appstream_python.Component.DisplayLength(px=420, compare="ne").compare_px(420) is False
    assert appstream_python.Component.DisplayLength(px=420, compare="ne").compare_px(410) is True
    assert appstream_python.Component.DisplayLength(px=420, compare="ne").compare_px(430) is True

    assert appstream_python.Component.DisplayLength(px=420, compare="lt").compare_px(420) is False
    assert appstream_python.Component.DisplayLength(px=420, compare="lt").compare_px(410) is True
    assert appstream_python.Component.DisplayLength(px=420, compare="lt").compare_px(430) is False

    assert appstream_python.Component.DisplayLength(px=420, compare="gt").compare_px(420) is False
    assert appstream_python.Component.DisplayLength(px=420, compare="gt").compare_px(410) is False
    assert appstream_python.Component.DisplayLength(px=420, compare="gt").compare_px(430) is True

    assert appstream_python.Component.DisplayLength(px=420, compare="le").compare_px(420) is True
    assert appstream_python.Component.DisplayLength(px=420, compare="le").compare_px(410) is True
    assert appstream_python.Component.DisplayLength(px=420, compare="le").compare_px(430) is False

    assert appstream_python.Component.DisplayLength(px=420, compare="ge").compare_px(420) is True
    assert appstream_python.Component.DisplayLength(px=420, compare="ge").compare_px(410) is False
    assert appstream_python.Component.DisplayLength(px=420, compare="ge").compare_px(430) is True

    with pytest.raises(ValueError):
        assert appstream_python.Component.DisplayLength(px=420, compare="test").compare_px(420)


def test_string_to_px() -> None:
    assert appstream_python.Component.DisplayLength.string_to_px("xsmall") == 360
    assert appstream_python.Component.DisplayLength.string_to_px("small") == 420
    assert appstream_python.Component.DisplayLength.string_to_px("medium") == 760
    assert appstream_python.Component.DisplayLength.string_to_px("large") == 900
    assert appstream_python.Component.DisplayLength.string_to_px("xlarge") == 1200

    with pytest.raises(ValueError):
        appstream_python.Component.DisplayLength.string_to_px("test")


def test_equals() -> None:
    assert appstream_python.Component.DisplayLength(px=420, compare="eq") == appstream_python.Component.DisplayLength(px=420, compare="eq")
    assert appstream_python.Component.DisplayLength(px=420, compare="eq") != appstream_python.Component.DisplayLength(px=410, compare="eq")
    assert appstream_python.Component.DisplayLength(px=420, compare="eq") != appstream_python.Component.DisplayLength(px=420, compare="ne")
