import appstream_python
import pathlib


DATA_DIR = pathlib.Path(__file__).parent / "data" / "AppStream"


def test_data_jdtextedit() -> None:
    component = appstream_python.AppstreamComponent.from_file(DATA_DIR / "com.gitlab.JakobDev.jdTextEdit.metainfo.xml")

    assert component.id == "com.gitlab.JakobDev.jdTextEdit"
    assert component.name.get_default_text() == "jdTextEdit"
    assert component.summary.get_default_text() == "An advanced text editor"
    assert component.project_license == "GPL-3.0-only"
    assert component.metadata_license == "CC0-1.0"
    assert component.project_group is None

    assert len(component.urls) == 4
    assert component.urls["homepage"] == "https://gitlab.com/JakobDev/jdTextEdit"
    assert component.urls["bugtracker"] == "https://gitlab.com/JakobDev/jdTextEdit/-/issues"
    assert component.urls["help"] == "https://jdtextedit.readthedocs.io"
    assert component.urls["vcs-browser"] == "https://gitlab.com/JakobDev/jdTextEdit"

    assert component.display_length["recommends"][0].px == 760
    assert component.display_length["recommends"][0].compare == "ge"
