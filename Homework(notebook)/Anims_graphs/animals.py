from typing import Any
from datetime import date
import os
import json


class BaseAnimal:
    name: str
    birthday: date
    pills: list[str]
    owner: str | None
    breed: str = NotImplemented

    def __init__(self, name: str, birthday: date, owner: str | None = None):
        self.name = name
        self.birthday = birthday
        self.owner = owner
        self.pills = []

    def __str__(self):
        return f'Имя: {self.name}, Вид: {self.breed}, День рождения: {str(self.birthday)}'

    def add_pill(self, pill_name: str):
        self.pills.append(pill_name)

    def set_owner(self, owner_name: str):
        self.owner = owner_name


class Cat(BaseAnimal):
    breed = 'Кошачьи'
    color: str

    def __init__(
            self,
            name: str,
            birthday: date,
            color: str,
            owner: str | None = None
    ):
        super().__init__(name, birthday, owner)
        self.color = color

    def to_json(self):
        return {
            'name': self.name,
            'birthday': str(self.birthday),
            'color': self.color,
            'owner': self.owner,
        }

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> 'Cat':
        return cls(
            name=json_data['name'],
            birthday=date(*map(int, json_data['birthday'].split("-"))),
            color=json_data['color'],
            owner=json_data['owner'],
        )

    def save_into_json_file(self, path):
        self.to_json()
        with open(path, mode='wt') as fp:
            json.dump(self.to_json(), fp)

    @classmethod
    def open_class_from_json(cls, path):
        if os.path.exists(path):
            with open(path, mode='rb') as fp:
                json_data = json.load(fp)
                return Cat.from_json(json_data)
        else:
            raise FileNotFoundError

    def __str__(self):
        return f'Цвет: {self.color} {super().__str__()}, '


def main():
    snick = Cat('Snickers', date(2011, 7, 12), 'gray', "Yuriy")
    lapa = Cat("Lapa", date(2019, 1, 11), 'orange', 'Olaf')
    snick.save_into_json_file("snickers.json")
    lapa.save_into_json_file("lapa.json")
    snickers = Cat.open_class_from_json("snickers.json")

    lapka = Cat.open_class_from_json("lapa.json")

    print(snickers)
    print(lapka)


if __name__ == "__main__":
    main()
