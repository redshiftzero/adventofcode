


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
    image = [[]]  # We'll have each layer be an element in this list.
    for pixel in raw_image:
        if len(image[current_layer_num]) >= width_in_pix * height_in_pix:
            current_layer_num += 1
            image.append([])
        image[current_layer_num].append(int(pixel))

    # Elves want to know the layer with the fewest 0s.
    lowest_number_of_zeros = float('inf')
    target_layer = []
    for layer in image:
        number_of_zeros = layer.count(0)
        if number_of_zeros < lowest_number_of_zeros:
            lowest_number_of_zeros = number_of_zeros
            target_layer = layer

    print(target_layer.count(2) * target_layer.count(1))
