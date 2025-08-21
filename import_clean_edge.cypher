LOAD CSV WITH HEADERS FROM 'file:///clean_edge.tsv' AS row FIELDTERMINATOR '\t'

MATCH (a:Node {id: row.source})
MATCH (b:Node {id: row.target})
MERGE (a)-[e:Edge {relationship: row.metaedge}]->(b);