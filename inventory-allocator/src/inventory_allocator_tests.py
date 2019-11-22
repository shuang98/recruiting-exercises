# Run tests: python inventory_allocator_tests.py -v

import unittest
import json
from inventory_allocator import InventoryAllocator


class InventoryAllocatorTests(unittest.TestCase):
  def test_single_item(self):
    order = {'apple': 1}
    warehouses = [{'name': 'owd', 'inventory': {'apple': 1}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'owd': {'apple': 1}}]
    self.assertCountEqual(actual, expected)

  def test_single_item_no_shipment(self):
    order = {'apple': 1}
    warehouses = [{'name': 'owd', 'inventory': {'apple': 0}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = []
    self.assertCountEqual(actual, expected)

  def test_single_item_split(self):
    order = {'apple': 10}
    warehouses = [{'name': 'owd', 'inventory': {'apple': 5}},
                  {'name': 'dm', 'inventory': {'apple': 5}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'dm': {'apple': 5}}, {'owd': {'apple': 5}}]
    self.assertCountEqual(actual, expected)

  def test_single_item_split_few_warehouses(self):
    order = {'orange': 2}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 1}},
                  {'name': 'b', 'inventory': {'apple': 5, 'pear': 1}},
                  {'name': 'c', 'inventory': {'orange': 1, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'a': {'orange': 1}},
                {'c': {'orange': 1}}]
    self.assertCountEqual(actual, expected)

  def test_single_item_split_all_warehouses(self):
    order = {'orange': 3}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 1}},
                  {'name': 'b', 'inventory': {'apple': 5, 'pear': 1, 'orange': 1}},
                  {'name': 'c', 'inventory': {'orange': 1, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'a': {'orange': 1}},
                {'b': {'orange': 1}},
                {'c': {'orange': 1}}]
    self.assertCountEqual(actual, expected)

  def test_single_item_split_no_shipment(self):
    order = {'apple': 10}
    warehouses = [{'name': 'owd', 'inventory': {'apple': 5}},
                  {'name': 'dm', 'inventory': {'apple': 4}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = []
    self.assertCountEqual(actual, expected)

  def test_single_item_split_prioritize_cheaper_warehouse(self):
    order = {'apple': 10}
    warehouses = [{'name': 'owd', 'inventory': {'apple': 5}},
                  {'name': 'dm', 'inventory': {'apple': 10}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'dm': {'apple': 5}}, {'owd': {'apple': 5}}]
    self.assertCountEqual(actual, expected)

  def test_multi_items(self):
    order = {'apple': 10, 'orange': 2, 'pear': 5}
    warehouses = [{'name': 'a', 'inventory': {
        'apple': 10, 'orange': 2, 'pear': 5}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'a': {'apple': 10, 'orange': 2, 'pear': 5}}]
    self.assertCountEqual(actual, expected)

  def test_multi_items_split(self):
    order = {'apple': 10, 'orange': 2, 'pear': 5}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 1}},
                  {'name': 'b', 'inventory': {'apple': 5, 'pear': 1}},
                  {'name': 'c', 'inventory': {'orange': 1, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'a': {'apple': 5, 'orange': 1}},
                {'b': {'apple': 5, 'pear': 1}},
                {'c': {'orange': 1, 'pear': 4}}]
    self.assertCountEqual(actual, expected)

  def test_multi_items_split_prioritize_cheaper_warehouse(self):
    order = {'apple': 8, 'orange': 2, 'pear': 5}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 1}},
                  {'name': 'b', 'inventory': {'apple': 5, 'pear': 2}},
                  {'name': 'c', 'inventory': {'orange': 3, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'a': {'apple': 5, 'orange': 1}},
                {'b': {'apple': 3, 'pear': 2}},
                {'c': {'orange': 1, 'pear': 3}}]
    self.assertCountEqual(actual, expected)

  def test_multi_items_split_no_shipment(self):
    order = {'apple': 10, 'orange': 3, 'pear': 5}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 1}},
                  {'name': 'b', 'inventory': {'apple': 5, 'pear': 1}},
                  {'name': 'c', 'inventory': {'orange': 1, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = []
    self.assertCountEqual(actual, expected)

  def test_zero_item_in_warehouse(self):
    order = {'orange': 2}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 1}},
                  {'name': 'b', 'inventory': {'orange': 0}},
                  {'name': 'c', 'inventory': {'orange': 1, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'a': {'orange': 1}},
                {'c': {'orange': 1}}]
    self.assertCountEqual(actual, expected)

  def test_zero_item_in_order(self):
    order = {'orange': 0, 'pear': 6}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 1}},
                  {'name': 'b', 'inventory': {'orange': 4}},
                  {'name': 'c', 'inventory': {'orange': 1, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'c': {'pear': 6}}]
    self.assertCountEqual(actual, expected)

  def test_zero_item_in_order_and_warehouse(self):
    order = {'orange': 0, 'pear': 6}
    warehouses = [{'name': 'a', 'inventory': {'apple': 5, 'orange': 0}},
                  {'name': 'b', 'inventory': {'orange': 0}},
                  {'name': 'c', 'inventory': {'orange': 1, 'pear': 6}}]
    actual = InventoryAllocator(warehouses).allocate(order)
    expected = [{'c': {'pear': 6}}]
    self.assertCountEqual(actual, expected)


if __name__ == '__main__':
  unittest.main()
