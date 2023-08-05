import appstream_python
import pathlib


DATA_DIR = pathlib.Path(__file__).parent / "data" / "Description"


def test_to_plain_text() -> None:
    component = appstream_python.AppstreamComponent.from_file(DATA_DIR / "DescriptionTest.metainfo.xml")

    assert component.description.to_plain_text() == (DATA_DIR / "DefaultPlainText.txt").read_text(encoding="utf-8").strip()
    assert component.description.to_plain_text("de") == (DATA_DIR / "GermanPlainText.txt").read_text(encoding="utf-8").strip()
    assert component.description.to_plain_text("NotExistingLanguage") == (DATA_DIR / "DefaultPlainText.txt").read_text(encoding="utf-8").strip()


def test_to_html() -> None:
    component = appstream_python.AppstreamComponent.from_file(DATA_DIR / "DescriptionTest.metainfo.xml")

    assert component.description.to_html() == (DATA_DIR / "DefaultHtml.html").read_text(encoding="utf-8").strip()
    assert component.description.to_html("de") == (DATA_DIR / "GermanHtml.html").read_text(encoding="utf-8").strip()
    assert component.description.to_html("NotExistingLanguage") == (DATA_DIR / "DefaultHtml.html").read_text(encoding="utf-8").strip()
