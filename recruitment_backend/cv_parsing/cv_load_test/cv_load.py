# import openai
# import pdfplumber

# # Configurez votre clé API OpenAI
# openai.api_key = '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'


# def extract_text_from_pdf(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# def ask_question_from_pdf(pdf_path, question):
#     # Extraire le texte du PDF
#     pdf_text = extract_text_from_pdf(pdf_path)

#     # Demander à GPT-3 de répondre à la question sur le PDF
#     response = openai.ChatCompletion.create(
#         model="davinci-003",  # Ou "gpt-4" selon votre modèle préféré
#         messages=[
#             {"role": "system", "content": "Vous êtes un assistant AI qui répond aux questions basées sur un CV."},
#             {"role": "user", "content": f"Voici le contenu du CV :\n{pdf_text}\n\nQuestion : {question}"}
#         ]
#     )

#     # Renvoyer la réponse de GPT-3
#     return response['choices'][0]['message']['content']

# # Exemple d'utilisation
# pdf_path = r"C:\Users\NICK-TECH\Downloads\Documents\DONGMO.pdf"
# question = "Quelles sont les compétences du candidat en json ? je ne veux ni commentaire ni explication ni label. je veux juste le json"
# answer = ask_question_from_pdf(pdf_path, question)
# print(answer)


import pdfplumber
from transformers import pipeline

# Charger le modèle GPT-2 via Hugging Face
generator = pipeline("text-generation", model="gpt2")

# Fonction pour extraire le texte du PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Fonction pour poser une question à GPT-2 et obtenir une réponse
def ask_question_from_pdf(pdf_path, question):
    # Extraire le texte du PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Créer un prompt à partir du contenu du PDF et de la question
    prompt = f"Voici le contenu du CV :\n{pdf_text}\n\nQuestion : {question}"

    # Utiliser GPT-2 pour générer une réponse
    response = generator(prompt, max_length=500, num_return_sequences=1)

    # Renvoyer la réponse générée par GPT-2
    return response[0]['generated_text']

# Exemple d'utilisation
pdf_path = r"C:\Users\NICK-TECH\Downloads\Documents\DONGMO.pdf"
question = "Quelles sont les compétences du candidat en json ? je ne veux ni commentaire ni explication ni label. je veux juste le json"
question = "Resolver l'equation x+1=2"
answer = ask_question_from_pdf(pdf_path, question)
print("La reponse: \n")
print(answer)
