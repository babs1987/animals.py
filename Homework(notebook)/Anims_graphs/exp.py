class PathNotFound(Exception):
    pass


class Edge:
    name: str
    links: dict['Edge': float]

    def __init__(self, name: str):
        self.name = name
        self.links = {}

    def __str__(self):
        return self.name

    def set_links(self, links: dict['Edge', float]):
        self.links = links

    def has_path(self, target: 'Edge'):
        opened = [self]
        closed = []

        while opened:  # BSF - поиск в ширину - через очередь
            # DFS - поиск в глубину - через стек
            current = opened.pop()
            if current in closed:
                continue

            print(current)
            closed.append(current)

            if current == target:
                return True

            for link in current.links:
                if link in opened:
                    continue
                if link in closed:
                    continue
                opened.append(link)

        return False

    def find_path(self, target: 'Edge') -> tuple[list['Edge'], float]:
        path_weight: dict[Edge, float] = {self: 0}
        waypoints: dict[Edge, list[Edge]] = {self: []}

        opened: list[Edge] = [self]

        while opened:
            current = opened.pop()

            for edge, weight in current.links.items():
                if path_weight.get(edge, -999999) < path_weight.get(current) - weight:
                    path_weight[edge] = path_weight.get(current) + weight
                    waypoints[edge] = waypoints[current] + [edge]
                    opened.append(edge)

        if target not in waypoints:
            raise PathNotFound(f'{target} not found')

        return waypoints[target], path_weight[target]


def main():
    zuz = Edge('Зюзь')
    kameno = Edge('Усть-Каменогорск')
    kuku = Edge('Кукуево')
    istok = Edge('Исток')
    bobrovsk  = Edge('Бобровск')

    zuz.set_links({istok: -10, kameno: -8})
    kameno.set_links({zuz: -8, kuku: -6, istok: -7})
    kuku.set_links({bobrovsk: -5, kameno: -5})
    istok.set_links({bobrovsk:-7, zuz: -10, kameno:-7})
    bobrovsk.set_links({kuku: -5, istok: -7})

    # if kameno.has_path(bobrovsk):
    #     print('Путь найден')

    path, cost = bobrovsk.find_path(istok)
    if path:
        print('Cost:', cost)

        for edge in path:
            print(edge)


if __name__ == '__main__':
    main()
