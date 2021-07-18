new_path = open("//mnt//c//Users//admin//Desktop//Automated Configuration//new_path.txt", "wt")
with open("//mnt//c/Users//admin//Desktop//Automated Configuration//path.txt", "rt") as file:
    for line in file:
        st = '"' + str(line) + '"'
        new_path.write(st.replace("\n", ""))  # .split('"')[1]
new_path.close()
