from csv import reader
from itertools import combinations
import itertools
import collections


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


def get_c1(dataset):
    list_of_items = []
    for i in dataset:
        for j in i:
            if j not in list_of_items:
                list_of_items.append(j)
    list_of_items.sort()
    return list_of_items


def get_sup_c1(list_of_items, dataset):
    number_of_items = len(list_of_items)
    count = [0 for i in range(number_of_items)]
    for i in range(number_of_items):
        for j in dataset:
            if list_of_items[i] in j:
                count[i] += 1
    return count


def calculate_support_count(dataset, crr):

    brr = [0 for i in range(len(crr))]
    for i in range(len(crr)):
        for j in range(len(dataset)):
            flag = True
            for k in crr[i]:
                if k not in dataset[j]:
                    flag = False
                    break
            if flag:
                brr[i] += 1
    return brr


def get_frequent_itemset(candidate_set, count, flag):
    brr = []
    count1 = []
    for i in range(len(candidate_set)):
        if count[i] >= min_support_count:
            brr.append(candidate_set[i])

            if flag:
                st = []
                for j in candidate_set[i]:
                    st.append(j)
                st.sort()
                st1 = ""
                for j in st:
                    st1 += j

                d[st1] = count[i]
            else:
                d[candidate_set[i]] = count[i]
            count1.append(count[i])
    return brr, count1


def generate_next_candidateset(L, n):

    crr = []
    if n == 2:

        for i in range(len(L)-1):
            temp = [[L[i], L[j]] for j in range(i+1, len(L))]
            for k in temp:
                crr.append(k)
    else:
        L_copy = list(L)
        temp = []
        r = []
        for i in range(len(L)):
            check = L[i][:-1]

            if check not in r:
                r.append(check)
                temp.append([L[i][-1]])
            else:
                ind = r.index(check)

                temp[ind].append(L[i][-1])

        for i in range(len(temp)):
            if len(temp[i]) > 1:

                comb = findsubsets(temp[i], 2)

                temp1 = [r[i]+list(comb[j]) for j in range(len(comb))]

                for k in temp1:
                    crr.append(k)

    return crr


def get__candidateset(prev, curr):
    n1 = len(curr[0])-1
    purened = []
    for i in range(len(curr)):
        subset = findsubsets(curr[i], n1)
        T = [False for i in range(len(subset))]
        for j in range(len(subset)):
            g = list(subset[j])
            for item in prev:
                flag = True
                for k in g:
                    if k not in item:
                        flag = False
                        break
                if flag:
                    T[j] = True
        if False not in T:
            purened.append(curr[i])
    return purened


def findsubsets(s, n):
    return list(itertools.combinations(s, n))


def sub_lists(my_list):
    subs = []
    for i in range(0, len(my_list)+1):
        temp = [list(x) for x in combinations(my_list, i)]
        if len(temp) > 0:
            subs.extend(temp)

    ind = subs.index([])
    subs.pop(ind)
    return subs


def Generate_Association_Rules(n):

    print("Itemsets are:", frequent_itemset[n-1])
    for m in range(len(frequent_itemset[n-1])):
        print()
        arr = frequent_itemset[n-1][m]
        required = []

        for j in frequent_itemset[len(frequent_itemset)-1]:
            flag = True
            for i in range(len(arr)):
                if arr[i] not in j:
                    flag = False
                    break
            if flag:
                break

        if flag:
            union = []
            for i in arr:
                union.append(i)
            union.sort()
            un = ''
            for i in union:
                un += i

            print("For Itemset:", arr)
            sublist = sub_lists(arr)
            min_conf = []
            y = 1
            print("Confidence:")
            for i in range(len(sublist)-1):
                for j in range(i+1, len(sublist)):
                    fg = True
                    for k in sublist[i]:
                        if k in sublist[j]:
                            fg = False
                            break
                    if fg and len(sublist[i])+len(sublist[j]) == len(arr):

                        t1 = []
                        t2 = []
                        for k in sublist[i]:
                            t1.append(k)
                        t1.sort()
                        for k in sublist[j]:
                            t2.append(k)
                        t2.sort()
                        st1 = ''
                        st2 = ''
                        for k in t1:
                            st1 += k
                        for k in t2:
                            st2 += k

                        con = d[un]/d[st1]*100
                        con = int(con+0.5)
                        if con >= confidence:
                            min_conf.append(y)
                            print(t1, "=>", t2, "=", con, "% / (strong)")
                        else:
                            print(t1, "=>", t2, "=", con, "% x")
                        y += 1
                        con = d[un]/d[st2]*100
                        con = int(con+0.5)
                        if con >= confidence:
                            min_conf.append(y)
                            print(t2, "=>", t1, "=", con, "% / (strong)")
                        else:
                            print(t2, "=>", t1, "=", con, "% x")
                        y += 1
            print()
            # print("rules",min_conf, "can be considered as strong Association Rules.")


def print_details(itemset, count):
    print("Frequent Itemset       	Support Value")
    for i in range(len(itemset)):
        print(itemset[i], "  	=>   	", count[i])


d = collections.defaultdict(int)
min_support_count = int(input("Minimum support value:  "))
confidence = int(input("Minimum confidence value:  "))
frequent_itemset = []
frequent_itemset_count = []


def main():
    dataset = load_csv(
        '/Users/adityakaria/code/6-Sem/dm/test3/test.csv')

    list_of_items = get_c1(dataset)

    number_of_items = len(list_of_items)

    # print("Candidate set C 1:",number_of_items)

    count = get_sup_c1(list_of_items, dataset)

    L, count = get_frequent_itemset(list_of_items, count, False)
    frequent_itemset.append(L)
    frequent_itemset_count.append(count)
    print("L 1:")
    print_details(L, count)

    prevL = list(L)
    n = 1
    while list_of_items:
        n += 1
        candidate_set = generate_next_candidateset(L, n)
        if candidate_set == []:
            break

        candidate_set = get__candidateset(prevL, candidate_set)
        # print("purened Candidate set C",n,":",candidate_set)
        count = calculate_support_count(dataset, candidate_set)

        flag = True
        for i in count:
            if i != 0:
                flag = False
                break
        if flag:
            break

        L, count = get_frequent_itemset(candidate_set, count, True)
        frequent_itemset.append(L)
        frequent_itemset_count.append(count)
        print("Frequent Itemset L", n, ":",)
        print_details(L, count)

        prevL = list(L)

    print()
    print("Number of frequent itemsets are: ", len(frequent_itemset))

    print("Given below are all Association rules:")
    for idx in range(2, len(frequent_itemset) + 1):
        Generate_Association_Rules(idx)


if __name__ == '__main__':
    main()
