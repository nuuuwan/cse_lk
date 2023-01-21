from dataclasses import dataclass


@dataclass
class StockListBase:
    stock_list: list

    def __getitem__(self, index):
        return self.stock_list[index]

    def __len__(self):
        return len(self.stock_list)

    def __iter__(self):
        return iter(self.stock_list)
