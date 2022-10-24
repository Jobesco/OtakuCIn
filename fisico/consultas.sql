-- Group by/Having
-- Seleciona tipo e a quantidade dos usuários publicadores
-- ? seria melhor o usuário com mais amigos?
SELECT tipo, COUNT(cpf) AS quantidade -- ? string ou nromal?
FROM Usuario 
GROUP BY tipo
HAVING tipo = 'Publicador';

-- Junção interna
-- toda obra que ganhou selo
SELECT o.nome_obra, s.nome_selo
FROM Obra o INNER JOIN
    Ganhou g ON o.id_obra = g.id_obra INNER JOIN
    Selo s on g.nome_selo = s.nome_selo;

-- Junção externa
-- Obras e seus respectivos selos, se houver
SELECT o.nome_obra, s.nome_selo
FROM Obra o LEFT OUTER JOIN
    Ganhou g ON o.id_obra = g.id_obra LEFT OUTER JOIN
    Selo s ON g.nome_selo = s.nome_selo;

-- Semi junção
-- selecionar dubladores que dublaram (dublador, tem)
SELECT Dublador.nome_dublador
FROM Dublador
WHERE EXISTS(SELECT * FROM Tem WHERE Tem.id_dublador = Dublador.id_dublador);


-- Anti-junção
-- selecionar dubladores que nunca dublaram
SELECT Dublador.nome_dublador
FROM Dublador
WHERE NOT EXISTS(SELECT * FROM Tem WHERE Tem.id_dublador = Dublador.id_dublador);

-- Subconsulta do tipo escalar, Junção interna e Groupby/Having
-- usuário e quantidade de obras assistidas
-- cuja média das obras assistidas é maior que a média geral
-- inner join, groupby/having e subconsulta escalar
SELECT u.nome_usuario, COUNT(o.id_obra)
FROM Usuario u INNER JOIN
    Assiste ass ON u.cpf = ass.cpf INNER JOIN 
    Obra o ON ass.id_obra = o.id_obra
GROUP BY u.nome_usuario
HAVING AVG(o.nota) >= (SELECT AVG(nota) FROM Obra)

-- Subconsulta do tipo linha 
SELECT cpf, nome_usuario
FROM Usuario
FETCH FIRST 5 ROWS ONLY;

-- numero de usuarios cujo sexo e tipo é igual ao de certo alguém
SELECT COUNT(*) as usuarios_semelhantes
FROM Usuario
WHERE (sexo, tipo) = (SELECT sexo, tipo from Usuario WHERE cpf = '382.670.951-95')

-- Subconsulta do tipo tabela (você pode pegar um escalar dela ou usar IN)
-- obras que são mangás e anime
SELECT nome_obra
FROM Obra
WHERE eh_anime = 1 AND (nome_obra IN (SELECT nome_obra
                                    FROM Obra
                                    WHERE eh_manga = 1))

-- Operação de conjunto
-- , todos os selos e categorias de uma obra
SELECT s.nome_selo as selos_categorias
FROM Selo s INNER JOIN
    Ganhou ga ON s.nome_selo = ga.nome_selo
WHERE ga.id_obra = (SELECT id_obra 
                FROM Obra 
                WHERE nome_obra = 'AttackOnTitan'
                FETCH FIRST 1 ROWS ONLY) -- ! reutilizável?
UNION ALL(
SELECT ca.nome_categoria
FROM Categoria ca INNER JOIN
    Ganhou ga ON ca.id_categoria = ga.id_categoria
WHERE ga.id_obra = (SELECT id_obra 
                FROM Obra 
                WHERE nome_obra = 'AttackOnTitan'
                FETCH FIRST 1 ROWS ONLY));


