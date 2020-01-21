import pandas as pd
data = pd.read_json('./data/variant_info.json')
print(data['name'])