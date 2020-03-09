li = [i.strip().split() for i in open("retail_dataset.csv").readlines()]
for i in li:
    for j in i:
        j=str(j)
print(type(li[0][0]))