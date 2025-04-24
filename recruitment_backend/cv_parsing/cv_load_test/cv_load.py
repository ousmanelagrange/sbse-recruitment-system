import os
import google.generativeai as genai
from pypdf import PdfReader

# 1. Configuration de l'API
os.environ['GOOGLE_API_KEY'] = 'AIzaSyC_ZhkHoe5aTdBJnA74F098w8uVq_WhA6M'  # Ne pas exposer ta vraie clé ici publiquement ;)
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# 2. Lecture du PDF
def extraire_texte_pdf(chemin_pdf):
    texte = ""
    try:
        with open(chemin_pdf, 'rb') as fichier_pdf:
            lecteur_pdf = PdfReader(fichier_pdf)
            for page in lecteur_pdf.pages:
                contenu = page.extract_text()
                if contenu:
                    texte += contenu + "\n"
    except Exception as e:
        print(f"Erreur lors de la lecture du PDF: {e}")
        return None
    return texte

# 3. Traitement du PDF
#chemin_pdf = 'D:\\Cours\\M2\\Projet\\Depot\\master_doc\\newReference\\fertig2018.pdf'
chemin_pdf = 'D:\\Projets Ganalis\\DOCS\\fin\\Djouda\\CV Djouda.pdf'

texte_pdf = extraire_texte_pdf(chemin_pdf)

# 4. Utilisation correcte de Gemini
if texte_pdf:
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-001')
        chat = model.start_chat()

        prompt = (
            "Soit le cv suivant, je voudrais que vous extraiyez les infromations sous forme de json avec les champs:  experence professionnelle, competense technique, niveau de langue, localisation,certification,niveau d'etude. si les informations sur un champs n'existent pas, mettez null "
            "\n\n"
            f"{texte_pdf[:12000]}"  # Gemini a une limite de tokens ! On limite à ~12k caractères.
        )

        print("Envoi à Gemini, en cours...")
        response = chat.send_message(prompt)
        print("✅ Résultat de Gemini :\n")
        print(response.text)

    except Exception as e:
        print(f"Erreur lors de l’appel à Gemini : {e}")
else:
    print("❌ Aucun texte extrait du PDF.")
