import pandas as pd

df = pd.read_csv('/home/jordan/Documents/rymscraper/examples/Exports/1688513855_export_url.csv', usecols =['Album', 'Date'])
df.dropna(inplace=True)


df['Year'] = df['Date'].str[-4:].astype(int)

album_dict = {}
album_list = []
for index, row in df.iterrows():
    name = row['Album']
    year = row['Year']
    album_dict = {"name":name, "year":year}
    album_list.append(album_dict)


print(album_list)

