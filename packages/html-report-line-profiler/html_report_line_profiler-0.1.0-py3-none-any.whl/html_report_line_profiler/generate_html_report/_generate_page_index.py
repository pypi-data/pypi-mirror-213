def generate_index_page():
    output_folder = "./profile/"

    # Obtenez la liste des fichiers de rapport dans le dossier de sortie
    reports = [file for file in os.listdir(output_folder) if file.endswith(".html")]

    # Générez le contenu de la page d'index avec des liens vers chaque rapport
    index_content = "<h1>Profiler Reports</h1>"
    for report in reports:
        report_path = os.path.join(output_folder, report)
        report_link = f'<a href="{report_path}">{report}</a>'
        index_content += f"<p>{report_link}</p>"

    # Écrivez le contenu de la page d'index dans un fichier
    index_path = os.path.join(output_folder, "index.html")
    with open(index_path, "w") as f:
        f.write(index_content)

    print(f">> WRITE {index_path}")
#
