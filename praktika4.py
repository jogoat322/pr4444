import json
import heapq
from collections import defaultdict
from datetime import datetime
import os

class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def walk(self, path='', code=None):
        if code is None:
            code = {}
        
        if isinstance(self.left, str):
            code[self.left] = path + '0'
        else:
            self.left.walk(path + '0', code)
        
        if isinstance(self.right, str):
            code[self.right] = path + '1'
        else:
            self.right.walk(path + '1', code)

def generate_huffman_code(text):
    frequency = defaultdict(int)
    
    for char in text:
        frequency[char] += 1
    
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def save_huffman_code_to_json(huffman_code):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    folder_name = f"{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    
    output_file_path = os.path.join(folder_name, "code.json")
    
    with open(output_file_path, "w") as json_file:
        json.dump(dict(huffman_code), json_file, ensure_ascii=False, indent=4)
    
    print(f"Huffman code saved in {output_file_path}")

# Получение имени файла от пользователя
input_file_name = input("Введите имя файла: ")

try:
    with open(input_file_name, "r", encoding="utf-8") as file:
        text_data = file.read()
except FileNotFoundError:
    print("Файл не найден.")
    exit()

huffman_code = generate_huffman_code(text_data)
save_huffman_code_to_json(huffman_code)
from huffman import CodeGenerator

def main():
    cgen = CodeGenerator()
    input_file_name = input("Введите имя файла: ")

    try:
        with open(input_file_name, "r", encoding="utf-8") as file:
            text_data = file.read()
    except FileNotFoundError:
        print("Файл не найден.")
        exit()

    huffman_code = cgen.generate_huffman_code(text_data)
    cgen.save_huffman_code_to_json(huffman_code)

if __name__ == "__main__":
    main()

