//CASE 1
MATCH 
  (d:Node {id: $input})-[l:Edge {relationship: "DlA"}]->(a:Node {kind:"Anatomy"}),
  (a)-[z:Edge {relationship: "AdG"}]->(g:Node {kind:"Gene"}),
  (c:Node {kind:"Compound"})-[y:Edge {relationship: "CuG"}]->(g),
  (d)-[s:Edge {relationship: "DaG"}]->(g)
WHERE NOT
  (c)-[:Edge{relationship: "CtD"}]->(d)
AND NOT
  (c)-[:Edge{relationship: "CpD"}]->(d)
RETURN c.id AS compoundID, c.name as compoundName

UNION 

//CASE 2
MATCH 
  (d:Node {id: $input})-[l:Edge {relationship: "DlA"}]->(a:Node {kind:"Anatomy"}),
  (a)-[z:Edge {relationship: "AuG"}]->(g:Node {kind:"Gene"}),
  (c:Node {kind:"Compound"})-[y:Edge {relationship: "CdG"}]->(g),
  (d)-[s:Edge {relationship: "DaG"}]->(g)
WHERE NOT
  (c)-[:Edge{relationship: "CtD"}]->(d)
AND NOT
  (c)-[:Edge{relationship: "CpD"}]->(d)
RETURN c.id AS compoundID, c.name as compoundName;