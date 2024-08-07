import zipfile
import os

def extract_matching_archives(main_zip_path, output_dir, keywords):
    # Stellen Sie sicher, dass das Ausgabe-Verzeichnis existiert
    os.makedirs(output_dir, exist_ok=True)
    
    # Öffnen Sie das Haupt-ZIP-Archiv
    with zipfile.ZipFile(main_zip_path, 'r') as main_zip:
        # Durchlaufen Sie alle Dateien im Haupt-ZIP-Archiv
        for zip_info in main_zip.infolist():
            if zip_info.filename.endswith('.zip'):
                # Temporärer Pfad für das extrahierte ZIP-Archiv
                temp_zip_path = os.path.join(output_dir, zip_info.filename)
                
                # Stellen Sie sicher, dass das Verzeichnis für das temporäre ZIP-Archiv existiert
                os.makedirs(os.path.dirname(temp_zip_path), exist_ok=True)
                
                with open(temp_zip_path, 'wb') as temp_zip_file:
                    temp_zip_file.write(main_zip.read(zip_info))
                
                # Überprüfen Sie den Inhalt des extrahierten ZIP-Archivs
                with zipfile.ZipFile(temp_zip_path, 'r') as inner_zip:
                    # Überprüfen Sie, ob eine Datei im inneren ZIP-Archiv ein Schlüsselwort enthält
                    match_found = any(
                        any(keyword.lower() in inner_zip_info.filename.lower() for keyword in keywords)
                        for inner_zip_info in inner_zip.infolist()
                    )
                    
                    if match_found:
                        # Extrahieren Sie das gesamte ZIP-Archiv, wenn ein Schlüsselwort gefunden wird
                        inner_zip.extractall(output_dir)

                # Löschen Sie das temporäre ZIP-Archiv nach der Verarbeitung
                os.remove(temp_zip_path)

# Beispiel für die Nutzung des Skripts
main_zip_path = r"C:\Users\Maxim\Downloads\cylums-nintendo-ds-rom-collection.zip" # Pfad zum Haupt-ZIP-Archiv
output_dir = r"C:\Users\Maxim\Downloads\extrahiert"  # Verzeichnis, in dem die extrahierten Dateien gespeichert werden sollen
keywords = ['Mario', 'Zelda', 'Pokemon', 'Kirby']

extract_matching_archives(main_zip_path, output_dir, keywords)
