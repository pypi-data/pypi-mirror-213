from Engine import PyTable
import json

import pandas as pd
data=pd.read_excel("data/1400pre.xlsx")

A=PyTable.ArrayTable(2,0)

A.fromPandas(data)

print(data)
# A.readExcelFile("data/1400pre.xlsx")
A.plot()

A.fromPandas(data)

print(data)
# A.readExcelFile("data/1400pre.xlsx")
A.plot()
# A.animation()
# A.show()

# import pandas as pd

# data=pd.read_excel("enginedata.xlsx")
# print(data)

# with open("res.json", 'w', encoding='utf-8') as fw:
#     json.dump(json.dumps(data.to_json()), fw, indent=4, ensure_ascii=False)
# # json_str = json.dumps(data.to_json())
# Tab=Table.ArrayTable()

# Tab.readExcel("enginedata.xlsx")