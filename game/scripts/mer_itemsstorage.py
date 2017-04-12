# -*- coding: UTF-8 -*-


class ItemsStorage(object):

    def __init__(self):
        self.storage = []
        self.money = 0
        self.trade_level = 3

    def add_money(self, value):
        self.money += value

    def remove_money(self, value):
        self.money -= value

    def has_money(self, value):
        return self.money >= value

    def transfer_money(self, storage, value):
        self.remove_money(value)
        storage.add_money(value)

    def get_items(self, item_type):
        if item_type == 'all':
            return [i for i in self.storage]
        return [i for i in self.storage if i.type == item_type]

    def has_item(self, id_):
        for i in self.storage:
            if i.id == id_:
                return True
        return False

    def remove_item(self, item, value=1, return_item=True):
        get_item = None
        if isinstance(item, str):
            for i in self.storage:
                if i.id == item:
                    get_item = i
                    break
        else:
            for i in self.storage:
                if i == item:
                    get_item = i
                    break
        if get_item is not None:
            if get_item.stackable():
                if value == 'all':
                    values = get_item.amount
                returned = get_item.decrease_amount(value)
                if get_item.amount <= 0:
                    self.storage.remove(get_item)
            else:
                self.storage.remove(get_item)
                returned = get_item

        if return_item:
            return returned

    def add_item(self, item, value=1):
        if value < 0:
            raise Exception('value < 0 use remove_item instead')
        if item is None:
            return
        if item.stackable():
            current = self.get_by_id(item.id)
            if current is not None:
                current.increase_amount(value)
            else:
                self.storage.append(item)
                item.increase_amount(value - 1)
        else:
            if item not in self.storage:
                self.storage.append(item)

    @property
    def items(self):
        return [i for i in self.storage]

    def transfer_item(self, item, storage, value=1):
        item = self.remove_item(item, value)
        storage.add_item(item)

    def transfer_all(self, storage):
        for i in [i for i in self.storage]:
            self.transfer_item(i, storage, 'all')

    def get_by_id(self, id_):
        for i in self.storage:
            if i.id == id_:
                return i
