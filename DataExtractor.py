import csv
import sys
import imp

googleImg = imp.load_source('GoogleImage', './GoogleImage.py')

def getActorsList(fileName):
	csvFile = open(fileName)
	data = []
	try:
		csvReader = csv.reader(csvFile, delimiter="\t")
		header = csvReader.next()
		actorColIdx = header.index("Actor")
		incomeColIdx = header.index("Total income")
		for row in csvReader:
			newRow = row
			newRow[incomeColIdx] = row[incomeColIdx][1:].replace(",","").replace("+","")
			data.append(row)

		#Extract actors column
		actors = [x[actorColIdx] for x in data]
		actorsIncome = [(x[actorColIdx],x[incomeColIdx]) for x in data]
	finally:
		csvFile.close()

	return actors

def main():
	actorsList = getActorsList('./Data/TopPaidActors.csv')
	print(actorsList)
	for actor in actorsList:
		googleImg.query('%s face' % actor, '.\\Data\\Faces')

if __name__ == '__main__':
	main()