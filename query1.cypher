MATCH
  (d: Node {id: $input}),
  (d)-[: Edge {relationship: "DaG"}]->(g: Node {kind: "Gene"}),
  (d)-[: Edge {relationship: "DlA"}]->(a: Node {kind: "Anatomy"})
OPTIONAL MATCH
  (c: Node {kind: "Compound"})-[: Edge {relationship: "CtD"}]->(d)
OPTIONAL MATCH
  (c: Node {kind: "Compound"})-[: Edge {relationship: "CpD"}]->(d)
RETURN
  d.name as DiseaseName,
  g.name as Genes, 
  a.name as Anatomy, 
  c.name as Compounds;