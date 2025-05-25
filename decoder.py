import json


# Чтение словаря
def load_dict_from_file(filename):
    """
    Загружает словарь из файла в формате JSON.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        shannon_dict = json.load(file)
    return {v: k for k, v in shannon_dict.items()}

# Чтение сжатого файла
def read_compressed_file(input_file):
    """
    Читает сжатый файл и извлекает строку битов.
    """
    with open(input_file, 'rb') as f:
        padding = int.from_bytes(f.read(1), 'big')
        byte_data = f.read()
        bit_string = ''.join(f"{byte:08b}" for byte in byte_data)
        return bit_string[:-padding]

# Декодирование данных
def decode_data(bit_string, reverse_dict):
    """
    Декодирует строку битов в исходный текст.
    """
    decoded_text = ''
    buffer = ''
    for bit in bit_string:
        buffer += bit
        if buffer in reverse_dict:
            decoded_text += reverse_dict[buffer]
            buffer = ''
    return decoded_text

# Запись несжатого файла
def write_decompressed_file(data, output_file):
    """
    Записывает декодированный текст в файл.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data)



# Декодировщик
def shannon_decoder(compressed_file):
    """
    Декодирует сжатый файл с использованием словаря.
    """
    dict_file = 'shannon_dict.json'
    output_file = 'output.txt'
    reverse_dict = load_dict_from_file(dict_file)
    bit_string = read_compressed_file(compressed_file)
    decoded_text = decode_data(bit_string, reverse_dict)
    write_decompressed_file(decoded_text, output_file)

    print("Декодирование завершено.")
    print(f"Несжатый файл сохранен в {output_file}")


shannon_decoder('compressed.bin')
