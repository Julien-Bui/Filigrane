import os
from watermarker import ajouter_filigrane_et_creer_pdf

def main():
    print("=== Générateur de Filigrane PDF ===")
    
    # S'assurer que les dossiers existent
    os.makedirs('images', exist_ok=True)
    os.makedirs('res', exist_ok=True)
    
    # Lister les images et PDF dans le dossier 'images'
    fichiers = [f for f in os.listdir('images') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.pdf'))]
    
    if not fichiers:
        print("❌ Aucun fichier (image ou PDF) trouvé dans le dossier 'images/'.")
        print("Veuillez y glisser vos images et relancer le script.")
        return
        
    print("\nImages disponibles :")
    for i, fichier in enumerate(fichiers, 1):
        print(f"[{i}] {fichier}")
        
    choix = input("\nEntrez le numéro de l'image à utiliser : ")
    try:
        index = int(choix) - 1
        if index < 0 or index >= len(fichiers):
            print("❌ Numéro invalide.")
            return
        image_choisie = fichiers[index]
    except ValueError:
        print("❌ Veuillez entrer un numéro valide.")
        return
        
    image_input = os.path.join('images', image_choisie)
    
    texte = input("\nEntrez le texte du filigrane : ")
    
    # Nom du PDF de sortie automatique basé sur le nom de l'image
    nom_base = os.path.splitext(image_choisie)[0]
    pdf_output = input(f"Nom du PDF de sortie (appuyez sur Entrée pour utiliser '{nom_base}.pdf') : ").strip('" \'')
    
    if not pdf_output:
        pdf_output = f"{nom_base}.pdf"
    elif not pdf_output.lower().endswith('.pdf'):
        pdf_output += '.pdf'
        
    pdf_output_path = os.path.join('res', pdf_output)

    ajouter_filigrane_et_creer_pdf(image_input, pdf_output_path, texte)

if __name__ == "__main__":
    main()
