# Run tests: python inventory_allocator_tests.py -v


class InventoryAllocator():
  def __init__(self, warehouses):
    self.warehouses = warehouses

  def allocate(self, order):
    shipments = []
    for warehouse in self.warehouses:
      warehouse_order = {}
      for item in order.keys():
        if order[item] > 0 and warehouse['inventory'].get(item):
          # take amount to fill rest of order or rest of warehouse inventory
          amount = min(order[item], warehouse['inventory'][item])
          order[item] -= amount
          warehouse_order[item] = amount
      if warehouse_order != {}:
        shipments.append({warehouse['name']: warehouse_order})
    # order cannot be fulfilled if any value is > 0
    return [] if any(order.values()) else shipments
