#Варіант 49. План проєкту: дерево з відсіканням гілок та підсумки сусідів
#Завдання 1. Дерево з відсіканням гілок
import sys

from calculations4 import Tree, Node, RecordD, RecordN
def main():
    try:
        elements = []#список де буде зберігатися всі значення які ми вводмо
        line = sys.stdin.readline()#зчитування першого рядка
        if not line:#якщо рядок пустий то все закриваємо
            return
        elements.extend(line.split())
        if not elements:#якщо список пустий
            return

        n = int(elements[0])#беремо перше числоробимо його цілим це і буде кількість вузлів
        if not (0 <= n <= 100):#перевірка на дозволений діапазон
            raise ValueError(f"Недопустиме значення n: {n}. Діапазон: 0...100")

        target_count = 1 + n * 4 + 1 if n > 0 else 2#рахуємо скільки всього значень має бути

        while len(elements) < target_count:#поки всю кількість значенб яку ми повинні ввести буде меншим за target_count ми будемо продовжувати вводити(приклад в завданні ми беремо 6 то це виходить за формулою 26 24 елемента які будуть всередині і 2 інших їх закривають)
            line = sys.stdin.readline()
            if not line:
                break
            elements.extend(line.split())

        idx = 0#показник де знаходиться у списку елементів
        n = int(elements[idx])#перетворюємо перше число на ціле
        idx += 1# переносимо показник далі

        tree = Tree()#клас

        #Як раз тут буде ідти перевірка на 4 значення для кожного вущла номер вузла, номер батька, тип запису по завданню N D і саме значення v
        for i in range(1, n + 1):
            if idx + 3 >= len(elements):
                raise ValueError("Неповні дані для вузлів дерева")

            node_id = int(elements[idx])#номер вузла
            p = int(elements[idx + 1])#номер батька
            c_type = elements[idx + 2]#тип запису N або D(по завданню)
            v = int(elements[idx + 3])#само значення v
            idx += 4#зсувую на 4 позиції вперед для наступного вузла

            # перевірка чи йдуть айді по порядку
            if node_id != i:
                raise ValueError(f"Недопустимий або порушений порядок id: {node_id}, очікувалося {i}")

            if node_id == 1:
                if p != 0:
                    raise ValueError("Для id = 1 батько p має дорівнювати 0")
            else:
                if not (1 <= p <= node_id - 1):#перевірка чи існує такий батько
                    raise ValueError(f"Недопустиме значення p для id {node_id}: {p}. Допустимо: 1...{node_id - 1}")

            if c_type not in ("N", "D"):#перевірка типу
                raise ValueError(f"Недопустимий тип запису: {c_type}. Допустимо: N або D")

            if not (0 <= v <= 1000):#перевірка значення v
                raise ValueError(f"Недопустиме значення v: {v}. Допустимо: 0...1000")

            #створюю запис звичайний або помножений на 2(дивлячись які дані записуємо) і далі дані кидаються у вузол і дерево(класи які я створював раніше)
            rec = RecordN(v) if c_type == "N" else RecordD(v)
            node = Node(node_id, rec, p)
            tree.add_node(node)

        t = int(elements[idx]) if idx < len(elements) else 0#порогове число t в кінці
        if not (0 <= t <= 200000):
            raise ValueError(f"Недопустиме значення t: {t}. Допустимо: 0...200000")

        visited = []#створюю порожній список - номери вузлів які пройшли обхід

        if tree.root is not None:
            if tree.root.record.score() > t:#якщо корінь більший за t список залишається порожнім
                visited = []
            else:
                def dfs(node):#функція обходу дерева в глибину(по завданню)
                    visited.append(node.id)#додаємо вузол до перевірених
                    for child in node.children:
                        if child.record.score() <= t:#якщо значення дитини не перевищує t то виконуємо dfs
                            dfs(child)

                dfs(tree.root)

        visited_set = set(visited)
        all_node_ids = sorted(tree.nodes.keys())
        not_visited = [nid for nid in all_node_ids if nid not in visited_set]#ті вузли до яких не дійшли або удалили

        selected = []
        for nid in visited:
            node = tree.nodes[nid]
            if len(node.children) == 0:#відбираюю лише кінцеві перевірки у яких немає дітей
                selected.append(node)

        selected_ids = [node.id for node in selected]
        total_score = sum(node.record.score() for node in selected)#сума відібраних балів

        #виводжу все у чіткому форматі за завданням(як завжди за допомогою джойн

        print(f"Обхід: {' '.join(map(str, visited)) if visited else '-'}")
        print(f"Відібрано: {' '.join(map(str, selected_ids)) if selected_ids else '-'}")
        print(f"Кількість: {len(selected_ids)}")
        print(f"Сума: {total_score}")
        print(f"Пропущено: {' '.join(map(str, not_visited)) if not_visited else '-'}")

    except Exception as e:
        sys.stderr.write(f"Помилка: {e}\n")#якщо десь сталася помилка виводиться її текст
        sys.exit(1)

if __name__ == "__main__":
    main()