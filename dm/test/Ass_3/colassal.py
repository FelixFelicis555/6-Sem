import pandas as pd 

minSupport=2
mincard=2

def pruneMinSupport(df,criteria,axisvalue):
	counter=0
	removeList=[]
	for i in df.sum(axis=axisvalue):
		if int(i) < criteria:
			if axisvalue==0:
				removeList.append(df.columns[counter])
			if axisvalue==1:
				removeList.append(counter)
		counter+=1
	if axisvalue==0:
		df=df.drop(removeList,axis=1)
	if axisvalue==1:
		df=df.drop(removeList)
	return df

def main():
	df =pd.read_csv("Test.csv")
	df=pruneMinSupport(df,minSupport,0)
	df=pruneMinSupport(df,mincard,1)
	df=pruneMinSupport(df,minSupport,0)
	df=pruneMinSupport(df,mincard,1)
	print(df)

if __name__=="__main__":
	main()
