n = int(input("How many albums are you uploading: "))
album_dict = {}
album_list = []
for i in range(n):
    album = input("Enter album name and year in the format Name - Year:")
    try:
        name, year = album.split(" - ")
    except ValueError:
        name, year = album.split("-")
    album_dict = {"name": name.strip(), "year": int(year.strip())}
    album_list.append(album_dict)


print(album_list)
