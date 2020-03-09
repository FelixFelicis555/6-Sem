
from csv import reader
from collections import defaultdict
from itertools import combinations

popped_idx = []


def load_csv(filename):
    dataset = []
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            row_temp = []
            for k in row:
                if k != '':
                    row_temp.append(k)
            dataset.append(row_temp)
    return dataset


def check_termination(prev_dataset, dataset):

    if prev_dataset == dataset:
        return True

    else:
        return False


def support_count(dataset):

    arr = defaultdict(int)

    for i in dataset:
        for j in range(len(i)):
            if arr[i[j]] is None:
                arr[i[j]] = 1
            else:
                arr[i[j]] += 1
    return arr


def cardinality_count(dataset):

    arr = []

    for i in dataset:
        arr.append(len(i))

    return arr


def preprocessing_on_support(dataset, support_count_of_dataset, min_sup):

    for i in list(support_count_of_dataset):

        if support_count_of_dataset[i] < min_sup:

            for j in dataset:
                try:
                    idx = j.index(i)
                    j.pop(idx)
                except:
                    continue
    return dataset


def preprocessing_on_cardinality(original_dataset, dataset, card_count_of_dataset, min_card):
    card_dataset = []
    for i in range(len(card_count_of_dataset)):
        if card_count_of_dataset[i] >= min_card:
            card_dataset.append(dataset[i])
        else:
            idx = original_dataset.index(dataset[i])
            popped_idx.append(i)

    return card_dataset


def preprocessing(dataset, number_of_items, min_sup, min_card):

    prev_dataset = dataset.copy()
    number_of_transaction = len(dataset)

    while True:
        support_count_of_dataset = support_count(dataset)
        dataset = preprocessing_on_support(
            dataset, support_count_of_dataset, min_sup)
        card_count_of_dataset = cardinality_count(dataset)
        dataset = preprocessing_on_cardinality(
            prev_dataset, dataset, card_count_of_dataset, min_card)

        bool_check = check_termination(prev_dataset, dataset)

        if bool_check:
            break
        else:
            prev_dataset = dataset.copy()

    return dataset


def find_enumeration_array(number_of_transaction):

    arr = []
    for i in range(number_of_transaction):
        if i not in popped_idx:
            arr.append(i)

    enumerated_array = []
    for j in range(2, number_of_transaction):
        enumerated_array.append(list(combinations(arr, j)))

    return enumerated_array


def intersection(arr1, arr2):

    intersection_array = []
    for i in arr2:
        if i in arr1:
            intersection_array.append(i)

    return intersection_array


def find_intersection(union_array):

    prev_intersection = intersection(union_array[0], union_array[1])
    for i in range(2, len(union_array)):
        prev_intersection = intersection(prev_intersection, union_array[i])

    return prev_intersection


def generate_bitvector(dataset):
    n = len(dataset)
    data = []
    for i in range(n):
        data += dataset[i]

    arr = list(set(list(data)))
    m = len(arr)
    arr.sort()

    for i in range(m):
        print('\tI'+str(i+1), end="\t")
    print()

    for i in range(0, n):
        print('T'+str(i+1), end="\t")
        j = dataset[i]

        for s in range(len(arr)):
            if arr[s] in j:
                print('1', end="\t\t")
            else:
                print('0', end="\t\t")
        print()
    return m


def find_bit_vector(intersection_array, m):

    arr = []
    for i in range(m):
        arr.append('0')

    for j in range(len(intersection_array)):
        x = intersection_array[j]
        arr[int(x[1])-1] = '1'

    str = ''
    for i in range(len(arr)):
        str += arr[i]

    return str


def row_enumeration(preprocessed_dataset, min_card, m):
    count = 0
    for i in range(len(preprocessed_dataset)):
        if i not in popped_idx:
            bit_vector = find_bit_vector(preprocessed_dataset[i], m)
            print(count, ':', i, '\t\t\t',
                  preprocessed_dataset[i], '\t\t\t\t\t', bit_vector)
        count += 1
    number_of_transaction = len(preprocessed_dataset)

    enumerated_array = find_enumeration_array(number_of_transaction)

    for i in enumerated_array:
        for enum in i:
            union_array = []
            union = []
            for s in range(len(enum)):
                union_array += [preprocessed_dataset[enum[s]]]

            intersection_array = find_intersection(union_array)
            if len(intersection_array) >= min_card:
                bit_vector = find_bit_vector(intersection_array, m)
                print(enum, '\t\t\t', intersection_array,
                      '\t\t\t\t\t', bit_vector)


def main():

    dataset = load_csv('test_dataset.csv')
    # dataset = load_csv('retail_dataset.csv')

    number_of_items = len(dataset)
    min_sup = int(input('-> Enter Minimum Support count: '))
    min_card = int(input('-> Enter Minimum Cardinality: '))
    print('Original Dataset:')
    for i in range(0, len(dataset)):
        print(dataset[i])
    print()
    print("Bit Vector:")
    print()
    m = generate_bitvector(dataset)
    print()
    preprocessed_dataset = preprocessing(
        dataset, number_of_items, min_sup, min_card)
    print("After Minimum support and minimum cardinality check:")
    if len(preprocessed_dataset) == 0:
        print("No frequent itemset avialable")
        exit()
    for i in range(0, len(preprocessed_dataset)):
        print(preprocessed_dataset[i])
    print()
    for i in range(len(popped_idx)):
        preprocessed_dataset.insert(popped_idx[i], None)
    print("Row Enumeration of dataset:")
    row_enumeration(preprocessed_dataset, min_card, m)


if __name__ == "__main__":
    main()
