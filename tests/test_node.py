import pytest

from Node import Node


def test_node_creation():
    n = Node(0, 0)
    assert hasattr(n, 'x') or hasattr(n, 'row')


def test_node_attributes_default():
    n = Node(1, 2)
    # basic flags should exist
    assert hasattr(n, 'is_wall')
    assert hasattr(n, 'is_start')
