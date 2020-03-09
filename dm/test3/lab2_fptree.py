import collections
import itertools
from itertools import combinations
from csv import reader
# from lab1_apriori import Generate_Association_Rules, sub_lists


d = collections.defaultdict(int)
min_support_count = int(input("->Enter minimum support value: "))
confidence = int(input("->Enter minimum confidence value: "))
frequent_itemset = []
frequent_itemset_count = []


CondPattern = []
CondPatternInd = []


class Node:
    def __init__(self):
        self.value = []
        self.children = []
        self.count = 0
        self.isEndOfWord = False

    def getNode(self):
        node = Node()
        return node

    def insert(self, root, key):
        temp = root
        for i in range(len(key)):
            if key[i] not in temp.value:
                temp.value.append(key[i])
                temp.children.append(root.getNode())
            ind = temp.value.index(key[i])
            temp.children[ind].count += 1
            temp = temp.children[ind]
        temp.isEndOfWord = True

    def getHeight(self, root):
        if root.children == []:
            return 1
        T = [0 for i in range(len(root.value))]
        for i in range(len(root.value)):
            T[i] = self.getHeight(root.children[i])
        return max(T)+1

    def DisplayEach(self, root, h):
        if h == 1:
            return root.value
        for i in range(len(root.value)):
            self.DisplayEach(root.children[i], h-1)

    def displayTree(self, root):
        h = self.getHeight(root)
        for i in range(1, h+1):
            #print("At height ",(i))
            self.DisplayEach(root, i)

    def search(self, root, key):
        temp = root
        for i in range(len(key)):
            if key[i] not in temp.value:
                return False
            ind = temp.value.index(key[i])
            temp = temp.children[ind]
        return (temp.isEndOfWord and temp != None)

    def searchPrefix(self, root, val, st):
        if root.children == []:
            return
        flag = False
        if val in root.value:
            ind = root.value.index(val)
            c = root.children[ind].count
            b = CondPatternInd.index(val)
            CondPattern[b].append((st, c))
            flag = True
        for i in range(len(root.value)):
            if root.value[i] == val and flag:
                continue
            root.searchPrefix(root.children[i], val, st+[root.value[i]])


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


def load_csv(filename):
    dataset = []
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            while row[len(row)-1] == '':
                row.pop()
            dataset.append(row)

    return dataset


def check(arr, brr):
    s = list(brr)
    a = s[0]
    flag = True
    for i in range(len(arr)):
        if arr[i] not in s[0]:
            return 0
    return s[1]


def display(item, arr):
    for i in range(len(item)):
        print(item[i], ":", end=" ")
        for j in range(len(arr[i])):
            s = list(arr[i][j])
            if s[0] == []:
                continue
            print(arr[i][j], end=" ")
        print()


def get_itemsets(dataset):
    list_of_items = []
    for i in dataset:
        for j in i:
            if j not in list_of_items:
                list_of_items.append(j)
    list_of_items.sort()
    return list_of_items


def get_sup_count(dataset, list_of_items):
    number_of_items = len(list_of_items)
    count = [0 for i in range(number_of_items)]
    for i in range(number_of_items):
        for j in dataset:
            if list_of_items[i] in j:
                count[i] += 1
    return count

# def find_subsets(itemset):

# 	items=len(itemset)
# 	subset=[]
# 	for i in range(1,items):

# 		subset.append(list(combinations(itemset,i)))

# 	sub=[]
# 	for i in range(0,len(subset)):
# 		sub+=subset[i]

# 	print(sub)
# 	return sub


# def Generate_Association_Rules(frequent_itemsets,frequent_itemsets_count,list_of_items,count):

# 	print("Association Rules")
# 	for i in frequent_itemsets:
# 		if len(i)==2:
# 			idx=frequent_itemsets.index(i)
# 			idx0=list_of_items.index(i[0])
# 			idx1=list_of_items.index(i[1])
# 			print(i[0],' => ',i[1], ' = ',count[idx]/count[idx0])
# 			print(i[1],' => ',i[0], ' = ',count[idx]/count[idx1])


# 		else:
# 			subsets=find_subsets(i)

# 			for i in range(len(subsets)):

def sub_lists(my_list):
    subs = []
    for i in range(0, len(my_list)+1):
        temp = [list(x) for x in combinations(my_list, i)]
        if len(temp) > 0:
            subs.extend(temp)

    ind = subs.index([])
    subs.pop(ind)
    return subs


def Generate_Association_Rules(frequent_itemset, frequent_itemset_count):

    print("Itemsets are:", frequent_itemset)
    # for m in range(len(frequent_itemset[n-1])):
    # 	print()
    for s in range(len(frequent_itemset)):
        arr = frequent_itemset[s]
        required = []

        # for j in frequent_itemset[len(frequent_itemset)-1]:
        # 	flag=True
        # 	for i in range(len(arr)):
        # 		if arr[i] not in j:
        # 			flag=False
        # 			break
        # 	if flag :
        # 		break

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
                        print(t1, "=>", t2, "=", con, "% - (strong)")
                    else:
                    	print(t1, "=>", t2, "=", con, "% x")
                    y += 1
                    con = d[un]/d[st2]*100
                    con = int(con+0.5)
                    if con >= confidence:
                        min_conf.append(y)
                        print(t2, "=>", t1, "=", con, "%  - (strong)")
                    else:
                    	print(t2, "=>", t1, "=", con, "%  x")
                    y += 1
            print()
            # print("rules",min_conf, "can be considered as strong Association Rules.")


def main():

    filename = '/Users/adityakaria/code/6-Sem/dm/test3/retail_dataset.csv'
    dataset = load_csv(filename)
    list_of_items = get_itemsets(dataset)
    count = get_sup_count(dataset, list_of_items)
    d1 = collections.defaultdict(int)
    crr = []
    for i in dataset:
        for j in i:
            d1[j] += 1
    for i in d1:
        if d1[i] >= min_support_count:
            crr.append([i, d1[i]])
            d[i] = d1[i]

    d1 = collections.defaultdict(int)
    crr.sort(key=lambda k: k[1], reverse=True)
    for i in crr:
        d1[i[0]] = []
    root = Node()

    for i in dataset:
        key = []
        for j in range(len(crr)):
            if crr[j][0] in i:
                key.append(crr[j][0])

        root.insert(root, key)

    for i in d1:
        if i not in CondPatternInd:
            CondPatternInd.append(i)
            CondPattern.append([])
        root.searchPrefix(root, i, [])

    print("Conditional Pattern Base:")
    print()

    for i in range(len(CondPatternInd)):
        res = []
        for j in CondPattern[i]:
            u = []
            s = list(j)
            a = s[0]
            b = s[1]
            a.sort()

    CondFPTreeInd = []
    CondFPTree = []
    CondFPTCount = []

    for i in range(len(CondPatternInd)):
        res = []
        resCount = []
        flag = False
        for j in range(len(CondPattern[i])):
            u = []
            v = []
            s = list(CondPattern[i][j])
            a = s[0]
            if a == []:
                continue
            b = s[1]
            n = len(a)
            for k in range(1, n+1):
                sub = findsubsets(a, k)
                for z in sub:
                    q = list(z)
                    if q not in res:
                        c = b
                        for h in range(j+1, len(CondPattern[i])):
                            ch = check(q, CondPattern[i][h])
                            if ch != 0:
                                c += ch
                        if c >= min_support_count:
                            flag = True
                            res.append(q)
                            resCount.append(c)
        if flag:
            CondFPTreeInd.append(CondPatternInd[i])
            CondFPTree.append((res))
            CondFPTCount.append((resCount))

    Frequent_Pattern_Generated = []
    Frequent_Pattern_Generated_count = []
    for i in range(len(CondFPTreeInd)):
        for j in range(len(CondFPTree[i])):
            arr = CondFPTree[i][j]+[CondFPTreeInd[i]]
            Frequent_Pattern_Generated.append(arr)
            Frequent_Pattern_Generated_count.append(CondFPTCount[i][j])
            brr = list(arr)
            brr.sort()
            st = ""
            for k in brr:
                st += k
            d[st] = CondFPTCount[i][j]

    print()
    print("Frequent_Pattern_Generated:")
    print("Itemset       	support count")
    for i in range(len(Frequent_Pattern_Generated)):
        print(Frequent_Pattern_Generated[i], ":	",
              Frequent_Pattern_Generated_count[i])

    frequent_itemset = Frequent_Pattern_Generated
    frequent_itemset_count = Frequent_Pattern_Generated_count

    Generate_Association_Rules(frequent_itemset, frequent_itemset_count)

    # Generate_Association_Rules(Frequent_Pattern_Generated,Frequent_Pattern_Generated_count,list_of_items,count)


if __name__ == '__main__':
    main()
