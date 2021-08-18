from unittest import TestCase

from specable.dicts import is_valid, parse_dict


class TestConfigparseBasics(TestCase):
    def test_is_config_valid(self):
        valid = {"a": {"b": 3}}

        self.assertTrue(is_valid(valid))

    def test_is_config_invalid(self):
        invalid = {3: {"b": 3}}
        self.assertFalse(is_valid(invalid))

        invalid = {3: {"b": 3}, "b": 3}
        self.assertFalse(is_valid(invalid))

        invalid = [3, {"b": 3}]
        self.assertFalse(is_valid(invalid))

        invalid = {"b": 3}
        self.assertFalse(is_valid(invalid))

    def test_parse_valid_config(self):
        valid = {"a": {"b": 3}}
        kind, config = parse_dict(valid)

        self.assertEqual(kind, "a")
        self.assertEqual(config, {"b": 3})

    def test_parse_valid_config_with_allow_stubs(self):
        valid = "test"
        kind, config = parse_dict(valid, allow_stubs=True)

        self.assertEqual(kind, "test")
        self.assertEqual(config, {})

    def test_parse_invalid_config(self):
        with self.assertRaises(ValueError):
            invalid = {3: {"b": 3}, "b": 3}
            parse_dict(invalid)

    def test_parse_invalid_config_with_allow_stubs(self):
        with self.assertRaises(ValueError):
            invalid = {3: {"b": 3}, "b": 3}
            parse_dict(invalid, allow_stubs=True)
