#Варіант 49. План проєкту: графи та сусіди
#Завдання 2. Підсумки сусідів
import sys
from calculations4 import Vertex, RecordD, RecordN, Graph


def main():
    try:
        elements = []#список де буде зберігатися всі значення які ми вводмо
        line = sys.stdin.readline()#зчитування першого рядка з n m s
        if not line:
            return
        elements.extend(line.split())
        if not elements:
            return

        n = int(elements[0])#кількість вершин
        m = int(elements[1])#кількість ребер
        s = int(elements[2])#стартова вершина

        #перевірка помилок
        if not (0 <= n <= 100):
            raise ValueError(f"Недопустиме значення n: {n}")
        if not (0 <= m <= n * (n - 1) // 2):
            raise ValueError(f"Недопустиме значення m: {m}")
        if not (0 <= s <= n if n > 0 else s == 0):
            raise ValueError(f"Недопустиме значення s: {s}")

        #рахуємо скільки всього значень має бути
        target_count = 3 + n * 3 + m * 2 + 1 if n > 0 else 4

        #поки всю кількість значенб яку ми повинні ввести буде меншим за target_count ми будемо продовжувати вводити
        while len(elements) < target_count:
            line = sys.stdin.readline()
            if not line:
                break
            elements.extend(line.split())

        idx = 0#показник де знаходиться у списку елементів
        n = int(elements[idx])
        idx += 1#прибавляється кількість вершин
        m = int(elements[idx])
        idx += 1#прибавляється кількість ребер
        s = int(elements[idx])
        idx += 1#прибавляється стартова вершина

        graph = Graph()#створюємо граф клас

        #цикл для послідовного зчитування кожної вершини у форматі id c v( у минулому завданні було 4 значення як раз)
        for i in range(1, n + 1):
            if idx + 2 >= len(elements):
                raise ValueError("Неповні дані для вершин графа")
            node_id = int(elements[idx])#унікальний ідентифікатор вершини
            c_type = elements[idx + 1]#тип запису N або D
            v = int(elements[idx + 2])#власне значення запису
            idx += 3#переміщяємо показник на три позиції вперед для наступної вершини

            #перевірка коректності порядку id, типу запису та діапазону значення v
            if node_id != i:
                raise ValueError(f"Порушений порядок id: {node_id}")
            if c_type not in ("N", "D"):
                raise ValueError(f"Недопустимий тип запису: {c_type}")
            if not (0 <= v <= 1000):
                raise ValueError(f"Недопустиме значення v: {v}")

            #створюю запис звичайний або помножений на 2(дивлячись які дані записуємо) і далі дані кидаються у вузол і дерево(класи які я створював раніше)
            rec = RecordN(v) if c_type == "N" else RecordD(v)
            vertex = Vertex(node_id, rec)
            graph.add_vertex(vertex)

        #зчитуємо m ребер та додаємо зв'язки у вершини
        for _ in range(m):
            if idx + 1 >= len(elements):
                raise ValueError("Неповні дані для ребер графа")
            u = int(elements[idx])#перший кінець ребра
            w = int(elements[idx + 1])#другий кінець ребра
            idx += 2

            #перевірка кінців ребра на допустимі межі (1...n та u != w)
            if not (1 <= u <= n and 1 <= w <= n and u != w):
                raise ValueError(f"Недопустимі кінці ребра: {u} {w}")

            #якщо обидві вершини існують у графі додаємо їх одна одній у списки сусідів
            if u in graph.vertices and w in graph.vertices:
                vu = graph.vertices[u]
                vw = graph.vertices[w]
                vu.add_neighbor(vw)
                vw.add_neighbor(vu)

        #сортуємо сусідів за зростанням номерів
        for vertex in graph.vertices.values():
            vertex.neighbors.sort(key=lambda x: x.id)

        t = int(elements[idx]) if idx < len(elements) else 0#порогове значення t в кінці

        #перевірка діапазону для порогового значення t
        if not (0 <= t <= 200000):
            raise ValueError(f"Недопустиме значення t: {t}")

        visited = []#юди запишемо обхід DFS
        #Перевірка чи існують вершини і чи є стартова вершина у графі
        if n > 0 and s > 0 and s in graph.vertices:
            visited_set = set()

            def dfs(vertex):
                visited_set.add(vertex.id)#DFS — обхід у глибину з відвідуванням вершини(позавданню)
                visited.append(vertex.id)
                for neighbor in vertex.neighbors:
                    if neighbor.id not in visited_set:
                        dfs(neighbor)

            dfs(graph.vertices[s])#обхід з початкової вершини s

        #рахуємо суму оцінок для сусідів
        neighbor_sums = {}
        for nid in visited:
            vertex = graph.vertices[nid]
            current_sum = sum(neighbor.record.score() for neighbor in vertex.neighbors)
            neighbor_sums[nid] = current_sum

        selected = []
        for nid in visited:
            if neighbor_sums[nid] >= t:#перевірка
                selected.append(graph.vertices[nid])#якщо все пройшло збільшуємо кількість вершин

        selected_ids = [vertex.id for vertex in selected]
        total_score = sum(vertex.record.score() for vertex in selected)

        #формую рядок сусідів у форматі id:сума
        neighbors_output = []
        for nid in visited:
            neighbors_output.append(f"{nid}:{neighbor_sums[nid]}")

        #виводжу все у чіткому форматі за завданням(як завжди за допомогою джойн
        print(f"Обхід: {' '.join(map(str, visited)) if visited else '-'}")
        print(f"Сусіди: {' '.join(neighbors_output) if neighbors_output else '-'}")
        print(f"Відібрано: {' '.join(map(str, selected_ids)) if selected_ids else '-'}")
        print(f"Кількість: {len(selected_ids)}")
        print(f"Сума: {total_score}")



    except Exception as e:
        # за потреби для налагодження можна розкоментувати рядок нижче:
        # sys.stderr.write(f"Помилка: {e}\n")
        pass


if __name__ == "__main__":
    main()
