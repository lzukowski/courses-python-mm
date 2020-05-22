from copy import copy
from unittest import TestCase

from dev_droga_courses.shared.unchangable import UnchangeableMixIn


class TestUnchangeableMixIn(TestCase):
    def setUp(self) -> None:
        self.obj = UnchangeableMixIn(arg1=1, arg2=2)

    def test_access_to_attributes(self):
        assert getattr(self.obj, 'arg1') == 1
        assert getattr(self.obj, 'arg2') == 2
        self.obj.new = 'New'
        assert self.obj.new == 'New'

    def test_cannot_change_arguments_already_set(self):
        with self.assertRaises(AttributeError):
            self.obj.arg1 = 'Change'

        with self.assertRaises(AttributeError):
            self.obj.arg2 = 'Change'

        self.obj.new_attr = 'New'
        with self.assertRaises(AttributeError):
            self.obj.new_attr = 'Change'

    def test_equality(self):
        assert self.obj == UnchangeableMixIn(arg1=1, arg2=2)
        assert self.obj == copy(self.obj)
        self.obj.additional = 'New'
        assert self.obj == UnchangeableMixIn(arg1=1, arg2=2, additional='New')

    @staticmethod
    def test_not_equal_when_comparing_other_types():
        fst_type = type('First', (UnchangeableMixIn, ), {})
        snd_type = type('Other', (UnchangeableMixIn, ), {})
        assert fst_type() != snd_type()

    def test_is_hashable(self):
        expected_hash = hash((('arg1', 1), ('arg2', 2), type(self.obj)))
        assert hash(self.obj) == expected_hash
