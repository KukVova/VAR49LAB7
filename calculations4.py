#Звичайний запис типу N повертає власне значення v
class RecordN:

    def __init__(self, value: int):#Зберігає значення v
        self.value = value

    def score(self) -> int:#іде звернення до value
        return self.value#повертає у незмінному вигляді


class RecordD(RecordN):

    def score(self) -> int:#іде звернення до value
        return 2 * self.value#і як раз тут множиться на два на значення v що треба по завданню

#окремий вузол дерева
class Node:

    def __init__(self, node_id: int, record, parent_id: int = 0):#задаємо значееня якими будемо користуватися в майбутьгбому
        self.id = node_id#номер вузлу
        self.record = record#RecordN або RecordD
        self.parent_id = parent_id#номер батьківсього вузлу
        self.children = []#створюю список для зберігання наслідуваних вузлів

#саме дерево
class Tree:

    def __init__(self):
        self.nodes = {}#створюю словник для більш легкого пошуку в майбутньому
        self.root = None#тепер це в нас значення яке наданий момент пусте але в майбетньмоу буде використовуватися

    #ця частинка коду відповідає за додаванням нових вузлів і головне перевірку деяких помилок
    def add_node(self, node: Node):
        if node.id in self.nodes:#перша помилка на дублювання
            raise ValueError(f"Дублювання ідентифікатора вузла: {node.id}")
        self.nodes[node.id] = node
        if node.parent_id == 0:
            if self.root is not None:#якщо в корені буде знайдено значення
                raise ValueError("Знайдено більше одного кореня")
            self.root = node
        else:
            parent = self.nodes.get(node.parent_id)#приєднання до батьківсьокго вузла
            if not parent:
                raise ValueError(f"Батьківський вузол {node.parent_id} не знайдено для вузла {node.id}")#це якщо не буде батька
            parent.children.append(node)
            parent.children.sort(key=lambda x: x.id)#сортує дітей за зростанням номерів

class Vertex:
    def __init__(self, vertex_id, record):
        self.id = vertex_id
        self.record = record
        self.neighbors = []#список сусідів-об'єктів

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)#додаємо сусіда у список якщо його там ще немає

class Graph:
    def __init__(self):
        self.vertices = {}#словник вершин за їхніми айді

    def add_vertex(self, vertex):
        self.vertices[vertex.id] = vertex#нову вершині у загальній структурі графа