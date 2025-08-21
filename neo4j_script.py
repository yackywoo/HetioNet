import csv
from neo4j import GraphDatabase
import subprocess

#neo4j driver 
URI = "neo4j://localhost:7687"
driver = GraphDatabase.driver(URI)

#writes to new tsv formatted file
def write_part(filename, data_list):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data_list[0].keys(), delimiter='\t')
        writer.writeheader()  
        writer.writerows(data_list) 

#generates tsv file with desired edges and moves file + nodes.tsv to neo4j import folder
def clean_edge() :
    desired_edges = {'DlA', 'AuG', 'AdG', 'DaG', 'CuG', 'CdG','CtD','CpD'}
    edges = []
    print("Reading data...")
    with open("edges.tsv", "r") as f:
        data = csv.DictReader(f, delimiter='\t') 

        for row in data :
            if row['metaedge'] in desired_edges :
                edges.append(row)
    f.close()

    print("Writing to clean_edge.tsv...")
    write_part("clean_edge.tsv", edges)

def move_to_import():
    print("Moving files to import path...")
    subprocess.call("./move_files.sh", shell=True)

#runs import cypher files
def import_cypher(file) :
    with open(file,"r") as f :
        node_cypher = f.read()
    print(f"Running {file}...")

    with driver.session() as session :
        session.run(node_cypher)

def valid_id(id):
    if "Disease::DOID:" not in id :
        clean_id = "Disease::DOID:" + id
        return clean_id
    else :
        return id


#cleans edges and runs import cyphers, generating neo4j database
def create_db() :
    #cypher files used for importing data
    node_cypher = "import_node.cypher"
    edge_cypher = "import_clean_edge.cypher"

    #cleans edge and moves data files to import directory
    clean_edge()
    move_to_import() #uses "move_clean_edge.sh"

    #reads import_cyphers and creates neo4j database
    print("Creating Neo4j database...")
    import_cypher(node_cypher)
    import_cypher(edge_cypher)
    print("Neo4j database created")

#returns set of compounds that satisfy query 2
def query2(d_id):
    disease_id = valid_id(d_id)
    query = "query2.cypher"
    with open(query,"r") as f :
        node_cypher = f.read()
    print(f"Running cypher {query}...")
    with driver.session() as session :
        result = session.run(node_cypher, input=disease_id)
        compounds = {record for record in result}
     
    compound_names = []
    for record in compounds :
        #compound_id's stored in record[0]
        compound_names.append(record[1])
    
    return compound_names

def query1(d_id):
    disease_id = valid_id(d_id)
    query = "query1.cypher"
    with open(query,"r") as f :
        node_cypher = f.read()
    print(f"Running cypher {query}...")
    with driver.session() as session :
        result = session.run(node_cypher, input=disease_id)
        output = {record for record in result}

    #avoid dupes
    genes = set()
    anatomy = set()
    compounds = set()

    for records in output:
        disease_name = records[0]
        genes.add(records[1])
        anatomy.add(records[2])
        compounds.add(records[3])

    #turn back to list for usability
    genes = list(genes)
    anatomy = list(anatomy)
    compounds = list(compounds)

    return disease_name, compounds, genes, anatomy

if __name__ == "__main__" :
    #create_neo4jdb()
    #output = query2("Disease::DOID:4989")
    output = query1("Disease::DOID:14268")
    print(output)