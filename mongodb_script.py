import csv
from pymongo import MongoClient

#mongodb variables
client = MongoClient('mongodb://localhost:27017')
db = client["hetionet"]

def read_edges() : 
    desired_edges = {'DlA', 'AuG', 'AdG', 'DaG', 'CuG', 'CdG','CtD','CpD'}
    edges = []
    with open("edges.tsv", "r") as f:
        data = csv.DictReader(f, delimiter='\t') 

        for row in data :
            if row['metaedge'] in desired_edges:
                edges.append(row)
    f.close()
    return edges

def read_nodes() :
    nodes = {}
    with open("nodes.tsv", "r") as f:
        data = csv.DictReader(f, delimiter='\t')

        #make this index-able so we can lookup diseases and get info out of it later
        for row in data :
            nodes[row['id']] = {'name' : row['name'], 'kind' : row['kind']}
    f.close()
    return nodes

def valid_id(id):
    if "Disease::DOID:" not in id :
        clean_id = "Disease::DOID:" + id
        return clean_id
    else :
        return id

def create_db() :
    #delete old collection if any remain
    print("Clearing collections...")
    db.diseases.delete_many({})
    db.anatomy_gene.delete_many({})
    db.compound_gene.delete_many({})

    print("Reading files...")
    nodes = read_nodes()
    edges = read_edges()

    #contains all query1 information
    disease_data = {}

    #contains all query2 information
    anatomy_gene = []
    compound_gene = []

    print("Creating MongoDB database...")
    for edge in edges : 
        source = edge['source']
        target = edge['target']
        metaedge = edge['metaedge']

        #item 2: compound treat disease
        if metaedge in ['CtD','CpD'] and nodes[source]['kind'] == "Compound" : 
            disease = nodes[target] 
            if disease and disease['kind'] == 'Disease' :
                disease_id = target
                compound_id = source
                compound_name = nodes[compound_id]['name']
                #if entry for this disease id not made, then make one
                if disease_id not in disease_data :
                    disease_data[disease_id] = {
                        '_id' : disease_id,
                        'name' : nodes[disease_id]['name'], #item 1, disease name
                        'compounds' : [],
                        'genes' : [],
                        'anatomy' : []
                    }
                
                disease_data[disease_id]['compounds'].append(compound_name)
        #item 3: gene causing disease
        elif metaedge == 'DaG' :
            disease_id = source
            gene_name = nodes[target]['name']

            if disease_id not in disease_data :
                    disease_data[disease_id] = {
                        '_id' : disease_id,
                        'name' : nodes[disease_id]['name'], #item 1, disease name
                        'compounds' : [],
                        'genes' : [],
                        'anatomy' : []
                    }
            disease_data[disease_id]['genes'].append(gene_name)

        #item 4: disease affecting anatomy
        elif metaedge == 'DlA' :
            disease_id = source
            anatomy_name = nodes[target]['name']

            if disease_id not in disease_data :
                    disease_data[disease_id] = {
                        '_id' : disease_id,
                        'name' : nodes[disease_id]['name'], #item 1, disease name
                        'compounds' : [],
                        'genes' : [],
                        'anatomy' : []
                    }
            disease_data[disease_id]['anatomy'].append(anatomy_name)
        
        #query2 items
        elif metaedge in ['AuG','AdG'] :
            anatomy_id = source
            gene_id = target

            anatomy_name = nodes[anatomy_id]['name']
            gene_name = nodes[gene_id]['name'] 

            anatomy_gene.append(
                {"anatomy_name": anatomy_name, "relationship": metaedge, "gene_name": gene_name}
            )

        elif metaedge in ['CuG','CdG'] :
            compound_id = source
            gene_id = target

            compound_name = nodes[compound_id]['name']
            gene_name = nodes[gene_id]['name'] 

            compound_gene.append(
                {"compound_name": compound_name, "relationship": metaedge, "gene_name": gene_name}
            )


    print("Inserting data...")
    db.diseases.insert_many(list(disease_data.values()))
    db.anatomy_gene.insert_many(anatomy_gene)
    db.compound_gene.insert_many(compound_gene)
    
    print("MongoDB database created")

#query1 function
def query1(d_id) : 
    disease_id = valid_id(d_id)
    print(f"Querying {disease_id}...")

    result = db.diseases.find_one({"_id": disease_id})
    
    q1_name = result['name']
    q1_compounds = result['compounds']
    q1_genes = result['genes']
    q1_anatomy = result['anatomy']

    return q1_name, q1_compounds, q1_genes, q1_anatomy
    
def query2(d_id) :    
    disease_id = valid_id(d_id)
    #run query1
    d_name, d_compounds, d_genes, d_anatomy = query1(disease_id)

    #get desired genes
    desired_genes = []
    for anatomy_name in d_anatomy :
        #anatomy_edges = ALL AuG and AdG nodes and edges
        anatomy_edges = db.anatomy_gene.find({"anatomy_name": anatomy_name})

        #filter anatomy_edges by only including DaG genes
        for edge in anatomy_edges :
            gene = edge['gene_name']
            relationship = edge['relationship']

            #desired_genes = Nodes((AuG OR AdG) AND DaG) for some given disease
            if gene in d_genes :
                desired_genes.append((gene, relationship))

    #get all desired compounds that affect some gene
    desired_compounds = set() #this may produce duplicates, use set
    for gene, rel in desired_genes :
        if rel == 'AdG' :
            opposite_rel = 'CuG'
        elif rel == 'AuG' :
            opposite_rel = 'CdG'

        #get all compounds that have opposite relationship, same gene
        all_compounds = db.compound_gene.find({"relationship": opposite_rel, "gene_name": gene})
        for compound in all_compounds :
            desired_compounds.add(compound['compound_name'])
    
    #remove any CtD or CpD compounds
    known_compounds = set(d_compounds)
    additional_compounds = list(desired_compounds - known_compounds)
    

    return additional_compounds



if __name__ == "__main__" :
    #create_mongodb()
    output = query2("Disease::DOID:4989")
    print(output)
    if "Gemcitabine" in output : 
        print("yes")
    if "Teniposide" in output :
        print("yes2")
    