
from huffman_functions import *
import json
import os
huffman_coder = HuffmanCoding()



while True:
        print("1. Кодирование Huffman")
        print("2. Декодирование Huffman")
        print("3. Вывод информации о файлах")
        print("4. Завершить программу")
        print("5. Удаление выбранного файла")
        choice = input("Выберите действие (1, 2, 3 или 4, 5): ")

        if choice == "1":
            input_file_name = input("Введите путь до файла: ")

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
            save_choice=input("Хотите схранить файл (y/n)?: ")
            if save_choice.lower() == "y":
                output_file_path = input("Введите путь для сохранения декодированного текста: ")
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(decoded_text)
                print("Декодированный текст сохранен в файл.")

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
        
        
        elif choice == "5":
            file_to_delete = input("Введите путь к файлу, который хотите удалить: ")
            try:
                os.remove(file_to_delete)
                print("Файл успешно удален.")
            except FileNotFoundError:
                print("Файл не найден.")
        else:
            print("Неверный выбор. Выберите 1, 2, 3 или 4.")


