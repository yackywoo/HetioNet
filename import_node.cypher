LOAD CSV WITH HEADERS FROM 'file:///nodes.tsv' AS row FIELDTERMINATOR '\t'

MERGE(n:Node {id: row.id, name: row.name, kind: row.kind});