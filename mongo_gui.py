import PySimpleGUI as sg
import mongodb_script as mongo

layout = [
    [sg.Text("Disease ID:"), sg.InputText(key="DISEASE_ID"), sg.Button("Search")],
    [sg.Button("Generate DB"), sg.Button("Exit")],
    [sg.Multiline(size=(160, 40), key="OUTPUT", autoscroll=True)]
]

window = sg.Window("HetioNet - MongoDB", layout)

while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "Generate DB":
        try:
            mongo.create_db()
            sg.popup("Databases created successfully!")
        except Exception as e:
            sg.popup_error("Error creating databases", str(e))
    elif event == "Search":
        disease_id = values["DISEASE_ID"].strip()
        if not disease_id:
            #handle empty inputs
            sg.popup("Please enter a Disease ID")
            continue
        try:
            name, compounds, genes, anatomy = mongo.query1(disease_id)
            additional_compounds = mongo.query2(disease_id)
            
            output = (
                "................................................................................\n"
                f"Name: {name}\n\n"
                f"Compounds: {compounds}\n\n"
                f"Genes: {genes}\n\n"
                f"Anatomy: {anatomy}\n\n"
                f"Additional Compounds: {additional_compounds}\n"
                "................................................................................"
            )
            window["OUTPUT"].update(output)
        except Exception as e:
            #any other error thats not an empty input
            sg.popup_error("Error querying disease", str(e))

window.close()