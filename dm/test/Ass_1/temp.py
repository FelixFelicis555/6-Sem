str1=""
for i in range(58,1000):
    str1+="item"+str(i)+","

print(str1)

filet = open("/Users/adityakaria/code/6-Sem/dm/test/Ass_1/tempFile.txt", "w")
filet.write(str1)
