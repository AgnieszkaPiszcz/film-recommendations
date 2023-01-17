// pliki do zaimportowania prz użyciu słowa LOAD CSV muszą być w folderze <neo4j-home>/import - u mnie to jest /var/lib/neo4j/import
// skrypt należy odpalić komendą: cypher-shell -f <nazwa pliku>


CREATE CONSTRAINT userIdConstraint FOR (user:User) REQUIRE user.id IS UNIQUE;
CREATE CONSTRAINT movieIdConstraint FOR (movie:Movie) REQUIRE movie.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM "file:///movies.csv" AS csvLine
CREATE (movie:Movie {id: toInteger(csvLine.movieId), title: csvLine.title});

LOAD CSV WITH HEADERS FROM "file:///ratings.csv" AS line
MERGE (u:User {id: toInteger(line.userId)}) WITH *
MATCH (m:Movie {id: toInteger(line.movieId)})
CREATE (u) -[:RATED {rating: toFloat(line.rating)}]-> (m);


