# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import pytest

from colourspace.util.settings import Settings

FILENAME = "test.pkl"


def remove_file(filename):
    try:
        os.remove(filename)
    except:
        pass


def setup_function():
    remove_file(FILENAME)


def teardown_function():
    remove_file(FILENAME)


def test_read_one_from_empty():
    settings = Settings(FILENAME, 1)
    # Reading from an empty file must return default
    assert settings.get("test1", 123) == 123


def test_save_one_read_default():
    settings = Settings(FILENAME, 1)
    settings.set("test2", "something")
    # Reading from a non-empty file without the setting
    # must return the default
    assert settings.get("test1", 123) == 123


def test_save_two_read_one():
    settings = Settings(FILENAME, 1)
    # Add the setting and some other setting
    settings.set("test1", "something")
    settings.set("test2", "other")
    assert settings.get("test1", 123) == "something"


def test_remove_one_from_empty():
    settings = Settings(FILENAME, 1)
    settings.remove("test1")


def test_save_two_remove_one_get_one_default():
    settings = Settings(FILENAME, 1)
    # Add the setting and some other setting
    settings.set("test1", "something")
    settings.set("test2", "other")
    settings.remove("test2")
    assert settings.get("test2", 123) == 123


def test_save_two_read_one_wrong_version():
    settings1 = Settings(FILENAME, 1)
    # Add the setting and some other setting
    settings1.set("test1", "something")
    settings1.set("test2", "other")

    settings2 = Settings(FILENAME, 2)
    assert settings2.get("test1", 123) == 123
