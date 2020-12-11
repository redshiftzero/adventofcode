


if __name__=="__main__":
    with open("input.txt", "r") as f:
        raw_image = f.read()

    # test input
    #raw_image = '123456789012'
    #width_in_pix = 3
    #height_in_pix = 2

    width_in_pix = 25
    height_in_pix = 6
    current_layer_num = 0
    row_num = 0
    image = [[[]]]  # We'll have each layer be an element in this list.
    # Each row will be an element of an element in the outer list.
    for pixel in raw_image:
        # Check if time to add a new layer
        flat_layer = [item for sublist in image[current_layer_num] for item in sublist]
        if len(flat_layer) >= width_in_pix * height_in_pix:
            current_layer_num += 1
            image.append([[]])
            row_num = 0

        # Check if time to add a new row
        if len(image[current_layer_num][row_num]) >= width_in_pix:
            row_num += 1
            image[current_layer_num].append([])

        image[current_layer_num][row_num].append(int(pixel))

    #print(image)

    # Elves want to know the layer with the fewest 0s.
    lowest_number_of_zeros = float('inf')
    target_layer = []
    for layer in image:
        flat_layer = [item for sublist in layer for item in sublist]
        number_of_zeros = flat_layer.count(0)
        if number_of_zeros < lowest_number_of_zeros:
            lowest_number_of_zeros = number_of_zeros
            target_layer = layer

    flat_target_layer = [item for sublist in target_layer for item in sublist]
    #print(flat_target_layer.count(2) * flat_target_layer.count(1))

    # Decode the image
    COLOR = {
        0: 'black',
        1: 'white',
        2: 'transparent',
    }

    # Decode starting at the top layer (reverse the list)
    decoded_image = ''
    for row in range(height_in_pix):
        for column in range(width_in_pix):
            for layer in reversed(range(current_layer_num, 0, -1)):
                pixel_value = image[layer][row][column]
                pixel_color = COLOR[pixel_value]
                if pixel_color == 'black':
                    decoded_image += '  '
                    break
                elif pixel_color == 'white':
                    decoded_image += '# '
                    break

            if column == width_in_pix - 1:
                decoded_image += '\n'

    print(decoded_image)
