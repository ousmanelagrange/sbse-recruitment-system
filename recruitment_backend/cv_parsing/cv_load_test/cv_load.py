import openai
import pdfplumber

# Configurez votre clé API OpenAI
openai.api_key = 'Bearer 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'

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def ask_question_from_pdf(pdf_path, question):
    # Extraire le texte du PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Demander à GPT-3 de répondre à la question sur le PDF
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ou "gpt-4" selon votre modèle préféré
        messages=[
            {"role": "system", "content": "Vous êtes un assistant AI qui répond aux questions basées sur un CV."},
            {"role": "user", "content": f"Voici le contenu du CV :\n{pdf_text}\n\nQuestion : {question}"}
        ]
    )

    # Renvoyer la réponse de GPT-3
    return response['choices'][0]['message']['content']

# Exemple d'utilisation
pdf_path = r"C:\Users\NICK-TECH\Downloads\Documents\DONGMO.pdf"
question = "Quelles sont les compétences du candidat ?"
answer = ask_question_from_pdf(pdf_path, question)
print(answer)
