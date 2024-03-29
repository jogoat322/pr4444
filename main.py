import json
import heapq
from collections import defaultdict
from datetime import datetime
import os
import math

class HuffmanCoding:
    def __init__(self):
        self.huffman_code = None

    def generate_huffman_code(self, text):
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

        self.huffman_code = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

    def save_huffman_code_to_json(self):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder_name = f"{timestamp}"
        os.makedirs(folder_name, exist_ok=True)

        code_file_path = os.path.join(folder_name, "code.json")

        with open(code_file_path, "w") as code_file:
            json.dump(dict(self.huffman_code), code_file, ensure_ascii=False, indent=4)

        print(f"Huffman code saved in {code_file_path}")

    def save_decoded_text_to_file(self, decoded_text):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder_name = f"{timestamp}"
        os.makedirs(folder_name, exist_ok=True)

        decoded_file_path = os.path.join(folder_name, "decoded_text.txt")

        with open(decoded_file_path, "w", encoding="utf-8") as decoded_file:
            decoded_file.write(decoded_text)

        print(f"Decoded text saved in {decoded_file_path}")

    def decode_huffman(self, encoded_text):
        reversed_huffman_code = {code: char for char, code in dict(self.huffman_code).items()}
        decoded_text = ""
        current_code = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in reversed_huffman_code:
                decoded_text += reversed_huffman_code[current_code]
                current_code = ""

        return decoded_text

def calculate_entropy(file_path):
    with open(file_path, 'rb') as file:
        byte_freq = {}
        total_bytes = 0
        byte = file.read(1)
        while byte:
            total_bytes += 1
            byte_freq[byte] = byte_freq.get(byte, 0) + 1
            byte = file.read(1)

        entropy = 0
        for freq in byte_freq.values():
            probability = freq / total_bytes
            entropy -= probability * math.log2(probability)

        return entropy

def calculate_file_size(file_path):
    return os.path.getsize(file_path)

def calculate_compression_ratio(original_size, compressed_size):
    return original_size / compressed_size

def main():
    huffman_coder = HuffmanCoding()

    while True:
        print("1. Кодирование Huffman")
        print("2. Декодирование Huffman")
        print("3. Вывод информации о файлах")
        print("4. Завершить программу")

        choice = input("Выберите действие (1, 2, 3 или 4): ")

        if choice == "1":
            input_file_name = input("Введите имя файла: ")

            try:
                with open(input_file_name, "r", encoding="utf-8") as file:
                    text_data = file.read()
            except FileNotFoundError:
                print("Файл не найден.")
                continue

            huffman_coder.generate_huffman_code(text_data)
            huffman_coder.save_huffman_code_to_json()

        elif choice == "2":
            json_file_path = input("Введите путь до файла JSON с кодом Huffman: ")

            try:
                with open(json_file_path, "r", encoding="utf-8") as json_file:
                    huffman_code_json = json_file.read()
                    huffman_coder.huffman_code = json.loads(huffman_code_json)
            except FileNotFoundError:
                print("Файл JSON не найден.")
                continue
            except json.JSONDecodeError:
                print("Ошибка при декодировании JSON.")
                continue

            encoded_text = input("Введите закодированный текст: ")
            decoded_text = huffman_coder.decode_huffman(encoded_text)
            print(f"Декодированный текст: {decoded_text}")

            save_option = input("Сохранить декодированный текст в файл? (y/n): ")
            if save_option.lower() == "y":
                huffman_coder.save_decoded_text_to_file(decoded_text)

        elif choice == "3":
            input_file_path = input("Введите путь к исходному файлу: ")
            compressed_file_path = input("Введите путь к закодированному файлу: ")

            # Размер исходного файла (байт)
            original_size = calculate_file_size(input_file_path)
            print(f"Размер исходного файла: {original_size} байт")

            # Размер закодированного файла (байт)
            compressed_size = calculate_file_size(compressed_file_path)
            print(f"Размер закодированного файла: {compressed_size} байт")

            # Энтропия исходного текстового файла
            entropy = calculate_entropy(input_file_path)
            print(f"Энтропия исходного файла: {entropy}")

            # Среднее количество бит на символ в закодированном файле
            avg_bits_per_symbol = compressed_size * 8 / original_size
            print(f"Среднее количество бит на символ в закодированном файле: {avg_bits_per_symbol:.2f} бит")

            # Степень сжатия
            compression_ratio = calculate_compression_ratio(original_size, compressed_size)
            print(f"Степень сжатия: {compression_ratio:.2%}")

        elif choice == "4":
            print("Программа завершена.")
            break

        else:
            print("Неверный выбор. Выберите 1, 2, 3 или 4.")

if __name__ == "__main__":
    main()
