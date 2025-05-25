import json
from collections import Counter

# Построение словаря Шеннона
def build_shannon_dict(frequencies):
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    def recursive_shannon(symbols, prefix=""):
        if len(symbols) == 1:
            return {symbols[0][0]: prefix}
        total_freq = sum(freq for _, freq in symbols)
        cumulative_freq = 0
        split_index = 0
        for i, (_, freq) in enumerate(symbols):
            cumulative_freq += freq
            if cumulative_freq >= total_freq / 2:
                split_index = i + 1
                break
        left = recursive_shannon(symbols[:split_index], prefix + "0")
        right = recursive_shannon(symbols[split_index:], prefix + "1")
        return {**left, **right}

    return recursive_shannon(sorted_freq)

# Кодирование текста
def encode_data(data, shannon_dict):
    return ''.join(shannon_dict[char] for char in data)

# Запись сжатого файла
def write_compressed_file(encoded_data, output_file):
    padding = 8 - (len(encoded_data) % 8)
    encoded_data += '0' * padding

    with open(output_file, 'wb') as f:
        f.write(bytes([padding]))
        byte_array = bytearray(int(encoded_data[i:i+8], 2) for i in range(0, len(encoded_data), 8))
        f.write(byte_array)

# Сохранение словаря
def save_dict_to_file(dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False)

# Основная функция кодировщика
def shannon_encoder(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    compressed_file = 'compressed.bin'
    dict_file = 'shannon_dict.json'
    frequencies = Counter(text)
    shannon_dict = build_shannon_dict(frequencies)
    encoded_data = encode_data(text, shannon_dict)

    write_compressed_file(encoded_data, compressed_file)
    save_dict_to_file(shannon_dict, dict_file)

    print("Сжатие завершено.")
    print(f"Словарь сохранен в {dict_file}")
    print(f"Сжатый файл сохранен в {compressed_file}")


shannon_encoder('input.txt')
