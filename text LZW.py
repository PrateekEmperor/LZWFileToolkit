def lzw_compress(input_string):

    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    compressed_data = []
    w = ""

    for c in input_string:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            compressed_data.append(dictionary[w])
            if next_code < 4096:
                dictionary[wc] = next_code
                next_code += 1
            w = c

    if w:
        compressed_data.append(dictionary[w])

    return compressed_data

def lzw_decompress(compressed_data):

    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    w = chr(compressed_data.pop(0))
    decompressed_data = [w]

    for k in compressed_data:
        if k in dictionary:
            entry = dictionary[k]
        elif k == next_code:
            entry = w + w[0]
        else:
            raise ValueError("Invalid compressed k: {}".format(k))

        decompressed_data.append(entry)

        if next_code < 4096:
            dictionary[next_code] = w + entry[0]
            next_code += 1

        w = entry

    return "".join(decompressed_data)

def compress_file(input_file, output_file):
    with open(input_file, 'r') as file:
        input_data = file.read()

    compressed_data = lzw_compress(input_data)

    with open(output_file, 'wb') as file:
        for data in compressed_data:
            file.write(data.to_bytes(2, byteorder='big'))  # 2 bytes per code

def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        compressed_data = []
        while True:
            bytes_data = file.read(2)
            if len(bytes_data) != 2:
                break
            compressed_data.append(int.from_bytes(bytes_data, byteorder='big'))

    decompressed_data = lzw_decompress(compressed_data)

    with open(output_file, 'w') as file:
        file.write(decompressed_data)


# compress_file('input.txt', 'compressed.lzw')
decompress_file('compressed.lzw', 'output.txt')
