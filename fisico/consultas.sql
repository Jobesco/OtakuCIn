-- Group by/Having
-- Seleciona tipo e a quantidade dos usuários publicadores
-- ? seria melhor o usuário com mais amigos?
SELECT tipo, COUNT(cpf) AS quantidade -- ? string ou nromal?
FROM Usuario 
GROUP BY tipo
HAVING tipo = 'Publicador';

-- Junção interna
-- Seleciona nome e quantidade dos que tem mais de 2 amigos
SELECT u.nome, COUNT(a.cpf_convidado)
FROM Usuario u INNER JOIN
-- ! SERÁ QUE ISSO \/ GERA VALORES REPETIDOS?!?!?!?
-- ? não, pois é pra cada amizade
    Amizade a ON (a.cpf_convidado = u.cpf OR a.cpf_convidador = u.cpf)
GROUP BY u.nome
HAVING a.cpf_convidado = u.cpf OR a.cpf_convidador = u.cpf; -- ? isso aq talvez é desnecessário

-- Junção externa
-- Obras e seus respectivos selos, se houver
SELECT o.nome_obra, s.nome_selo
FROM Obras o LEFT OUTER JOIN
    Ganhou g ON o.id_obra = g.id_obra INNER JOIN
    Selo s ON g.nome_selo = s.nome_selo

-- Semi junção
-- (exibir os dados da tabela a esquerda a partir de uma comparação entre 
-- duas tabelas até encontrar o primeiro resultado verdadeiro. isto é, não há 
-- produto cartesiano, tampouco resultados repetidos)
-- TODO

-- Anti-junção
-- TODO

-- Subconsulta do tipo escalar
-- usuário e quantidade de obras assistidas
-- cuja média das obras assistidas é maior que a média geral
SELECT u.nome, COUNT(o.id_obra)
FROM Usuario u INNER JOIN
    Assiste a ON u.cpf = a.cpf INNER JOIN Obra o ON a.id_obra = o.id_obra
GROUP BY u.nome
WHERE AVG(o.nota) >=
    (SELECT AVG(nota)
    FROM Amizade);

-- Subconsulta do tipo linha 
-- número de episódios cuja obra é mangá, é de fulano e nota é a mesma do mangá dele
-- ! não terminada
SELECT COUNT(e.numero), o.nota
FROM Episodio e INNER JOIN
    Obra o ON e.id_obra = o.id_obra
WHERE (o.eh_manga, o.nota) = (SELECT eh_manga, nota FROM Obra WHERE eh_manga AND autor = 'fulano')

-- numero de usuarios cujo sexo e tipo é igual ao de certo alguém
SELECT COUNT(*) as usuarios
FROM Usuario
WHERE (sexo, tipo) = (SELECT sexo, tipo from Usuario WHERE cpf = 'CPF!!!!!')

-- Subconsulta do tipo tabela (você pode pegar um escalar dela ou usar IN)
-- publicador e obras, publicadas por publicadores mulheres
-- ! não terminada
SELECT u.nome, o.nome_obra
FROM Usuario u INNER JOIN
    Obra o ON u.cpf = o.cpf
GROUP BY u.nome
WHERE AVG(o.nota) >=
    (SELECT AVG(nota)
    FROM Amizade);

WHERE name in (select nome mulheres)

-- obras cuja nota é maior que a média das obras de fulano
SELECT nome_obra
FROM Obra
WHERE nota <= AVG(SELECT nota
    FROM Obra
    WHERE autor = 'fulano');

-- obras que são mangás e anime
SELECT nome_obra
FROM Obra
WHERE eh_anime AND (nome_obra IN (SELECT nome_obra
                                    FROM Obra
                                    WHERE eh_manga))

-- Operação de conjunto
-- , todos os selos e categorias de uma obra
SELECT s.nome_selo
FROM Selo s INNER JOIN
    Ganhou g ON s.nome_selo = g.nome_selo
WHERE g.id_obra = (SELECT id_obra 
                FROM Obra 
                WHERE nome_obra = 'NOME DA OBRA!!!!!!!'
                FETCH FIRST 1 ROWS ONLY) -- ! reutilizável?
UNION ALL(
SELECT c.nome_categoria
FROM Categoria c INNER JOIN
WHERE g.id_obra = (SELECT id_obra 
                FROM Obra 
                WHERE nome_obra = 'NOME DA OBRA!!!!!!!'
                FETCH FIRST 1 ROWS ONLY));


