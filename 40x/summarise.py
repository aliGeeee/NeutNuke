import os
import sqlite3
import sys
sys.path.append('summaries')
import pandas as pd

outputDir = 'output_14d'
sumDir = 'summaries'

batchesRep = [i for i in os.listdir(outputDir) if '.DS_Store' not in i]
batchesRep.sort()
batchesPool = list(set([i.split('_')[0]+'_'+i.split('_')[1] for i in batchesRep]))
batchesPool.sort()

# for batchPool in batchesPool:
# 	x = []
# 	for batch in [i for i in batchesRep if batchPool in i]:
# 		conn = sqlite3.connect('{}/{}/outputDB_0.db'.format(outputDir, batch))
# 		c = conn.cursor()

# 		donutDF = pd.read_sql_query('''SELECT * FROM Cells WHERE acceptable;''', conn)

# 		for index, cell in donutDF.iterrows():
# 			c.execute('''SELECT donutObjs FROM NuclearBlobs WHERE cellID=?;''', (int(cell['id']),))
# 			w = sum([i[0] for i in c.fetchall()])
# 			x += [[batch, w]]
# 		c.close()
# 		conn.close()

# 	y = pd.DataFrame(data=x, columns = ['batch', 'donut'])
# 	print(batchPool, len(x), len([i for i in x if i[1]>2]))


for batchPool in batchesPool:
	???
	for batch in [i for i in batchesRep if batchPool in i]:
		