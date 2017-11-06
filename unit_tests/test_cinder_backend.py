#!/usr/bin/python3

"""
A set of unit tests for the cinder-backend interface.
"""

import os
import sys
import unittest

import mock

root_path = os.path.realpath('.')
if root_path not in sys.path:
    sys.path.insert(0, root_path)

lib_path = os.path.realpath('unit_tests/lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


class MockReactive(object):
    def r_clear_states(self):
        self.states = set()

    def __init__(self):
        self.r_clear_states()

    def set_state(self, name):
        self.states.add(name)

    def remove_state(self, name):
        if name in self.states:
            self.states.remove(name)

    def is_state(self, name):
        return name in self.states

    def r_get_states(self):
        return set(self.states)

    def r_set_states(self, states):
        self.states = set(states)


r_state = MockReactive()


def mock_reactive_states(f):
    def inner1(inst, *args, **kwargs):
        @mock.patch('charms.reactive.set_state', new=r_state.set_state)
        @mock.patch('charms.reactive.remove_state', new=r_state.remove_state)
        @mock.patch('charms.reactive.helpers.is_state', new=r_state.is_state)
        def inner2(*args, **kwargs):
            return f(inst, *args, **kwargs)

        return inner2()

    return inner1


import provides as testee_provides


CONFIGURE_STATE = 'storage-backend.configure'


class TestCinderBackend(unittest.TestCase):
    """
    Test the trivial notification issued by the cinder-backend interface.
    """
    def setUp(self):
        """
        Clean up the reactive states information between tests.
        """
        super(TestCinderBackend, self).setUp()
        r_state.r_clear_states()

    @mock_reactive_states
    def test_provides(self):
        """
        Test that the provider interface sets a reactive state.
        """
        no_alert = set(['something', 'something else'])
        alert = no_alert.union(set([CONFIGURE_STATE]))
        self.assertNotEquals(no_alert, alert)

        obj = testee_provides.CinderBackendProvides('relation-name')
        r_state.r_set_states(no_alert)
        obj.changed()
        self.assertEquals(alert, r_state.r_get_states())

        # That's all, folks!
