with open("name_city.txt", "r", encoding="utf-8") as infile, open("name_city_new.txt", "w", encoding="utf-8") as outfile:
  for line in infile:
    new_line = line.replace("_", " ")
    outfile.write(new_line)
    print(new_line)
