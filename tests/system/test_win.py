# tests/system/test_win.py

import pytest

from file_conversor.system.win import WinRegFile, WinRegKey


def test_winregkey_add_and_del_value():
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key.add_value("TestValue", "TestContent")
    assert key._data["TestValue"] == "TestContent"
    key.del_value("TestValue")
    assert "TestValue" not in key._data


def test_winregkey_add():
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key.add_value("IntValue", 123)
    assert key._data["IntValue"].startswith("dword:")
    assert key._data["IntValue"].endswith(f"{123:08x}")

    key.add_value("BytesValue", b"\x01\x02")
    assert key._data["BytesValue"].startswith("hex:")
    assert key._data["BytesValue"].endswith(f"{b"\x01\x02".hex()}")

    key.add_value("StrValue", "TEST")
    assert key._data["StrValue"] == "TEST"


def test_winregkey_update_with_dict():
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key.update({"A": "B", "C": 42})
    assert key._data["A"] == "B"
    assert key._data["C"].startswith("dword:")
    assert key._data["C"].endswith(f"{42:08x}")


def test_winregkey_repr_and_str():
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key.add_value("A", "B")
    s = str(key)
    r = repr(key)
    assert r.startswith("[HKEY_CURRENT_USER\\Software\\Test]")
    assert "\"A\"=\"B\"" in r
    assert s == r"HKEY_CURRENT_USER\Software\Test"


def test_winregfile_add_and_del_key():
    regfile = WinRegFile()
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    regfile.add_key(key)
    assert key.path in regfile._data
    regfile.del_key(key)
    assert key.path not in regfile._data


def test_winregfile_add_same_key():
    key1 = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key1.add_value("A", "B")
    key2 = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key2.add_value("C", "D")

    regfile = WinRegFile()
    regfile.add_key(key1)
    regfile.add_key(key2)

    r = repr(regfile)
    assert "HKEY_CURRENT_USER\\Software\\Test" in r
    assert '"A"="B"' in r
    assert '"C"="D"' in r

    key3 = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key3.add_value("C", "X")
    regfile.add_key(key3)

    r = repr(regfile)
    assert '"C"="X"' in r


def test_winregfile_update_with_iterable():
    regfile = WinRegFile()
    key1 = WinRegKey(r"HKEY_CURRENT_USER\Software\Test1")
    key2 = WinRegKey(r"HKEY_CURRENT_USER\Software\Test2")
    regfile.update([key1, key2])
    assert key1.path in regfile._data
    assert key2.path in regfile._data


def test_winregfile_str_and_repr():
    regfile = WinRegFile()
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key.add_value("A", "B")
    regfile.add_key(key)
    s = str(regfile)
    r = repr(regfile)
    assert "Windows Registry Editor Version 5.00" in r
    assert "[HKEY_CURRENT_USER\\Software\\Test]" in r
    assert s == r


def test_winregfile_getitem():
    regfile = WinRegFile()
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    regfile.add_key(key)
    assert regfile[key.path] == key
    assert regfile[key] == key
    with pytest.raises(KeyError):
        regfile[123]  # type: ignore


def test_winregfile_items_iter():
    regfile = WinRegFile()
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    regfile.add_key(key)
    items = list(regfile.items())
    assert items[0][0] == key.path
    assert items[0][1] == key
    assert next(iter(regfile)) == key.path


def test_winregfile_dumps_and_dump(tmp_path):
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key.add_value("A", "B")

    regfile = WinRegFile()
    regfile.add_key(key)

    s = regfile.dumps()
    assert "Windows Registry Editor Version 5.00" in s
    assert "[HKEY_CURRENT_USER\\Software\\Test]" in s
    assert '"A"="B"' in s

    out_file = tmp_path / "test.reg"
    regfile.dump(out_file)
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-16")
    assert "Windows Registry Editor Version 5.00" in content
    assert "[HKEY_CURRENT_USER\\Software\\Test]" in content
    assert '"A"="B"' in content


def test_winregfile_load(tmp_path):
    key = WinRegKey(r"HKEY_CURRENT_USER\Software\Test")
    key.add_value("A", "B")

    out_file = tmp_path / "test.reg"
    regfile = WinRegFile()
    regfile.add_key(key)
    regfile.dump(out_file)

    loaded = WinRegFile(out_file)
    assert "HKEY_CURRENT_USER\\Software\\Test" in loaded._data
    assert loaded._data["HKEY_CURRENT_USER\\Software\\Test"]._data["A"] == "B"
    assert '[HKEY_CURRENT_USER\\Software\\Test]' in repr(loaded)
    assert '"A"="B"' in repr(loaded)


def test_winregfile_load_invalid_file(tmp_path):
    bad_file = tmp_path / "bad.reg"
    bad_file.write_text("not a reg file", encoding="utf-16")
    with pytest.raises(RuntimeError):
        WinRegFile(bad_file)
