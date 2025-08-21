Files

1. Main Files
--------------------
	main.py 
		- CLI version of HetioNet's implmentation
		- Options to use MongoDB or Neo4j as the database 

	mongo_gui.py
		- GUI version of HetioNet's implmentation
	neo4j_gui.py
		- GUI version of HetioNet's implmentation
		- PySimpleGUI used for both
	

2. Supporting Files
--------------------
	mongodb_script.py
		- All functions associated with MongoDB 
	neo4j_script.py
		- All functions associated with Neo4j 
	move_files.sh
		- Used in query2_main.py to automatically move nodes.tsv and clean_edge.tsv into the import directory

3. Cypher Files (Neo4j)
--------------------
	import_node.cypher 
	import_clean_edge.cypher
		- Files containing the cypher used to import data into Neo4j's database
	query1.cypher
	query2.cypher
		- Files containing the cypher used for query 1 and query 2

4. Data
--------------------
	nodes.tsv
	edges.tsv
		- Files containing the raw data
