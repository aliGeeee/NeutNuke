import shutil
import os

inputs = 'rawCells'
outputs = 'cells'

try:
	os.mkdir(outputs)
except:
	pass

tallyDict = {}

for annot in [i for i in os.listdir(inputs) if '.DS_Store' not in i]:
	sample = annot.split(' - ')[0]
	destination = '{}/{}'.format(outputs, sample)
	if sample not in tallyDict:
		tallyDict[sample] = 0
		try:
			os.mkdir(destination)
		except:
			pass
	images = os.listdir('{}/{}'.format(inputs, annot))
	for image in [j for j in images if '.DS_Store' not in j]:
		shutil.copy2('{}/{}/{}'.format(inputs, annot, image), '{}/{}_cell_{}.jpg'.format(destination, sample, tallyDict[sample]))
		tallyDict[sample] += 1
