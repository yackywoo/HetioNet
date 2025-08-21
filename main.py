import neo4j_script as neo
import mongodb_script as mongo

db_options = """Database Options\n
    1) MongoDB
    2) Neo4j
    3) Exit
"""

def display(type) :
    options = f"""HetioNet Options - {type}\n
    1) Create database
    2) Query some disease ID
    3) Exit
    """
    print(options)

def run() :
    while True:
        print(db_options)
        choice = input("Enter choice: ").strip()

        if choice == str('1'):
            while True: 
                database = "MongoDB"
                display(database)
                choice = input("Enter choice: ").strip()
                if choice == str('1') :
                    mongo.create_db()
                elif choice == str('2'):
                    disease_id = input("Disease ID: ").strip()
                    name, compounds, genes, anatomy = mongo.query1(disease_id)
                    additional_compounds = mongo.query2(disease_id)

                    print(
                    "................................................................................\n"
                    f"Name: {name}\n\n"
                    f"Compounds: {compounds}\n\n"
                    f"Genes: {genes}\n\n"
                    f"Anatomy: {anatomy}\n\n"
                    f"Additional Compounds: {additional_compounds}\n"
                    "................................................................................"
                    )
                elif choice == str ('3'):
                    break
                else:
                    print("Invalid choice, try again.")
        elif choice == str('2'):
            while True: 
                database = "Neo4j"
                display(database)
                choice = input("Enter choice: ").strip()
                if choice == str('1') :
                    neo.create_db()
                elif choice == str('2'):
                    disease_id = input("Disease ID: ").strip()
                    name, compounds, genes, anatomy = neo.query1(disease_id)
                    additional_compounds = neo.query2(disease_id)

                    print(
                    "................................................................................\n"
                    f"Name: {name}\n\n"
                    f"Compounds: {compounds}\n\n"
                    f"Genes: {genes}\n\n"
                    f"Anatomy: {anatomy}\n\n"
                    f"Additional Compounds: {additional_compounds}\n"
                    "................................................................................"
                    )
                elif choice == str ('3'):
                    break
                else:
                    print("Invalid choice, try again.")
        elif choice == str('3'):
            break
        else:
            print("Invalid choice, try again.")
    

if __name__ == "__main__":
    run()