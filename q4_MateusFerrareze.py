#fazer importação e alterações do scaffold como usuário quiser

generate_inner_join_query = lambda: """
SELECT GAMES.title, COUNT(DISTINCT COMPANY.id_company) AS num_companies
FROM GAMES
INNER JOIN VIDEOGAMES ON GAMES.id_console = VIDEOGAMES.id_console
INNER JOIN COMPANY ON VIDEOGAMES.id_company = COMPANY.id_company
GROUP BY GAMES.title
HAVING num_companies > 1;
"""
generate_select_query = lambda attributes: f"SELECT {attributes} FROM GAMES INNER JOIN VIDEOGAMES ON GAMES.id_console = VIDEOGAMES.id_console INNER JOIN COMPANY ON VIDEOGAMES.id_company = COMPANY.id_company;"

inner_join_query = generate_inner_join_query()
print("Resultado do INNER JOIN entre GAMES, VIDEOGAMES e COMPANY:")
print(inner_join_query)

select_query = generate_select_query("GAMES.title, COMPANY.name")
print("\nResultado do comando SELECT dos atributos title e name:")
print(select_query)


