import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Malgarin1720@"
)

crs = mydb.cursor()

execsq3cmd = lambda cmd, crs: crs.execute(cmd)

execcreatetable = lambda table, attrs, crs: execsq3cmd("CREATE TABLE " + table + " (" + attrs + ");", crs)
execcreatedatabase = lambda dname, crs: execsq3cmd("CREATE DATABASE " + dname + ";", crs)
execdropdatabase = lambda dname, crs: execsq3cmd("DROP DATABASE IF EXISTS " + dname + ";", crs)
execdroptable = lambda dname, crs: execsq3cmd("DROP TABLE IF EXISTS " + dname + ";", crs)
execusedatabase = lambda dname, crs: execsq3cmd("USE " + dname + ";", crs)
execinsertinto = lambda table, values, crs: execsq3cmd("INSERT INTO " + table + " VALUES (" + values + ");", crs)
execselectfromwhere = lambda attrs, table, wherecond, crs: execsq3cmd("SELECT " + attrs + " FROM " + table + " WHERE " + wherecond + ";", crs)


print_result = lambda table_name, results: print(f"Tabela {table_name}:\n{results}\n") #implementei um print separando e nomeando tabelas


execcreatedatabase("mydatabase", crs)
execusedatabase("mydatabase", crs)


execcreatetable("USERS", "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), country VARCHAR(255), id_console INT", crs)
execcreatetable("VIDEOGAMES", "id_console INT, name VARCHAR(255), id_company INT, release_date DATE", crs)
execcreatetable("GAMES", "id_game INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), genre VARCHAR(255), release_date DATE, id_console INT", crs)
execcreatetable("COMPANY", "id_company INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), country VARCHAR(255)", crs)


execinsertinto("USERS", "DEFAULT, 'Anthony', 'USA', 1", crs)
execinsertinto("USERS", "DEFAULT, 'Geneva', 'Mexico', 2", crs)
execinsertinto("USERS", "DEFAULT, 'Samuel', 'Brasil', 3", crs)

execinsertinto("VIDEOGAMES", "1, 'Super Mario Bros', 1, '1985-09-13'", crs)
execinsertinto("VIDEOGAMES", "2, 'Halo Combat', 2, '2001-11-15'", crs)
execinsertinto("VIDEOGAMES", "3, 'Assassin Creed', 3, '2007-11-13'", crs)

execinsertinto("GAMES", "DEFAULT, 'God of War', 'Ação-Aventura', '2018-04-20', 1", crs)
execinsertinto("GAMES", "DEFAULT, 'Pokemon', 'RPG', '2022-11-18', 2", crs)
execinsertinto("GAMES", "DEFAULT, 'FIFA 23', 'RPG', '2022-09-30', 3", crs)

execinsertinto("COMPANY", "DEFAULT, 'Nintendo', 'Japão'", crs)
execinsertinto("COMPANY", "DEFAULT, 'Microsoft', 'EUA'", crs)
execinsertinto("COMPANY", "DEFAULT, 'Ubisoft', 'França'", crs)


execselectfromwhere("*", "USERS", "TRUE", crs)
print_result("USERS", crs.fetchall())

execselectfromwhere("*", "VIDEOGAMES", "TRUE", crs)
print_result("VIDEOGAMES", crs.fetchall())

execselectfromwhere("*", "GAMES", "TRUE", crs)
print_result("GAMES", crs.fetchall())

execselectfromwhere("*", "COMPANY", "TRUE", crs)
print_result("COMPANY", crs.fetchall())

execdroptable("USERS", crs)
execdroptable("VIDEOGAMES", crs)
execdroptable("GAMES", crs)
execdroptable("COMPANY", crs)

execdropdatabase("mydatabase", crs)