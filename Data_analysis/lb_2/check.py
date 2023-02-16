import heapq
from heapq import heappop, heappush
 
 
def isLeaf(root):
    return root.left is None and root.right is None
 
 
# Узел дерева
class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right
 
    # Переопределить функцию `__lt__()`, чтобы заставить класс `Node` работать с приоритетной очередью.
    # таким образом, что элемент с наивысшим приоритетом имеет наименьшую частоту
    def __lt__(self, other):
        return self.freq < other.freq
 
 
# Пройти по дереву Хаффмана и сохранить коды Хаффмана в словаре
def encode(root, s, huffman_code):
 
    if root is None:
        return
 
    # обнаружил листовой узел
    if isLeaf(root):
        huffman_code[root.ch] = s if len(s) > 0 else '1'
 
    encode(root.left, s + '0', huffman_code)
    encode(root.right, s + '1', huffman_code)
 
 
# Пройти по дереву Хаффмана и декодировать закодированную строку
def decode(root, index, s):
 
    if root is None:
        return index
 
    # обнаружил листовой узел
    if isLeaf(root):
        print(root.ch, end='')
        return index
 
    index = index + 1
    root = root.left if s[index] == '0' else root.right
    return decode(root, index, s)
 
 
# строит дерево Хаффмана и декодирует заданный входной текст
def buildHuffmanTree(text):
 
    # Базовый случай: пустая строка
    if len(text) == 0:
        return
 
    # подсчитывает частоту появления каждого символа
    # и сохраните его в словаре
    freq = {i: text.count(i) for i in set(text)}
 
    # Создайте приоритетную очередь для хранения активных узлов дерева Хаффмана.
    pq = [Node(k, v) for k, v in freq.items()]
    heapq.heapify(pq)
 
    # делать до тех пор, пока в queue не окажется более одного узла
    while len(pq) != 1:
 
        # Удалить два узла с наивысшим приоритетом
        # (самая низкая частота) из queue
 
        left = heappop(pq)
        right = heappop(pq)
 
        # создает новый внутренний узел с этими двумя узлами в качестве дочерних и
        # с частотой, равной сумме частот двух узлов.
        # Добавьте новый узел в приоритетную очередь.
 
        total = left.freq + right.freq
        heappush(pq, Node(None, total, left, right))
 
    # `root` хранит указатель на корень дерева Хаффмана.
    root = pq[0]
 
    # проходит по дереву Хаффмана и сохраняет коды Хаффмана в словаре.
    huffmanCode = {}
    encode(root, '', huffmanCode)
 
    # распечатать коды Хаффмана
    print('Huffman Codes are:', huffmanCode)
    print('The original string is:', text)
 
    # распечатать закодированную строку
    s = ''
    for c in text:
        s += huffmanCode.get(c)
 
    print('The encoded string is:', s)
    print('The decoded string is:', end=' ')
 
    if isLeaf(root):
        # Особый случай: для ввода типа a, aa, aaa и т. д.
        while root.freq > 0:
            print(root.ch, end='')
            root.freq = root.freq - 1
    else:
        # снова пересекают дерево Хаффмана, и на этот раз
        # декодирует закодированную строку
        index = -1
        while index < len(s) - 1:
            index = decode(root, index, s)
 
 
# Реализация алгоритма кодирования # Хаффмана на Python
if __name__ == '__main__':
 
    text = 'в чащах юга жил бы цитрус? да но фальшивый экземпляр!'
    buildHuffmanTree(text)