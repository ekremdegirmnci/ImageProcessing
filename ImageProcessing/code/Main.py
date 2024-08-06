inp_filename, operation, out_filename = input().split()


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
def read_imagefile(f):
    my_list = []
    our_values = [value for value in f.readline().split()]
    code, width, height, max_level = our_values[0], int(our_values[1]), int(our_values[2]), int(our_values[3])
    for i in range(height):
        rows = [int(value) for value in f.readline().split()]
        my_list.append(rows)
    return my_list


def write_imagefile(f, img_matrix):
    f.write(f"P2 {len(img_matrix[0])} {len(img_matrix)} 255\n")
    for i in range(len(img_matrix)):
        for j in range(len(img_matrix[0])):
            f.write(f"{img_matrix[i][j]}")
            if j < len(img_matrix[0]) - 1:
                f.write(" ")
        f.write("\n")


def misalign(img_matrix):
    for i in range(len(img_matrix) // 2 + 1):
        for j in range(len(img_matrix[0])):
            if j % 2 == 1 and i != len(img_matrix) // 2:
                a = img_matrix[i][j]
                b = img_matrix[len(img_matrix) - i - 1][j]
                img_matrix[i][j] = b
                img_matrix[len(img_matrix) - i - 1][j] = a
    return img_matrix


def sort_columns(img_matrix):
    for j in range(len(img_matrix[0])):
        column_list = [img_matrix[i][j] for i in range(len(img_matrix))]
        column_list.sort()
        for i in range(len(img_matrix)):
            img_matrix[i][j] = column_list[i]
    return img_matrix


def sort_rows_border(img_matrix):
    new_matrix = [[] for i in range(len(img_matrix))]
    for i in range(len(img_matrix)):
        sorted_list = []
        for j in range(len(img_matrix[0])):
            if not img_matrix[i][j] == 0:
                sorted_list.append(img_matrix[i][j])
            elif img_matrix[i][j] == 0:
                sorted_list = sorted(sorted_list)
                sorted_list.append(0)
                new_matrix[i] += sorted_list
                sorted_list = []
        if sorted_list:
            sorted_list = sorted(sorted_list)
            new_matrix[i] += sorted_list
    img_matrix = new_matrix
    return img_matrix


def convolution(img_matrix, kernel):
    height, width = len(img_matrix), len(img_matrix[0])
    resulted_matrix = [[0] * len(img_matrix[0]) for k in range(len(img_matrix))]

    new_matrix = [[0] * (len(img_matrix[0]) + 2) for _ in range(len(img_matrix) + 2)]
    for i in range(len(img_matrix)):
        for j in range(len(img_matrix[0])):
            new_matrix[i + 1][j + 1] = img_matrix[i][j]

    for i in range(1, height + 1):
        for j in range(1, width + 1):
            result_sum = 0
            for m in range(-1, 2):
                for n in range(-1, 2):
                    result_sum += new_matrix[i + m][j + n] * kernel[m + 1][n + 1]
            resulted_matrix[i - 1][j - 1] = max(0, min(result_sum, 255))

    return resulted_matrix


# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
f = open(inp_filename, "r")
img_matrix = read_imagefile(f)
f.close()

if operation == "misalign":
    img_matrix = misalign(img_matrix)

elif operation == "sort_columns":
    img_matrix = sort_columns(img_matrix)

elif operation == "sort_rows_border":
    img_matrix = sort_rows_border(img_matrix)

elif operation == "highpass":
    kernel = [
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ]
    img_matrix = convolution(img_matrix, kernel)

f = open(out_filename, "w")
write_imagefile(f, img_matrix)
f.close()
