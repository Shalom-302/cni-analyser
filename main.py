import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("La clé API Google n'a pas été trouvée dans le fichier .env.")
    st.stop()

genai.configure(api_key=api_key)

st.title("Extraction de données d'une CNI avec Gemini Vision")

# Ajout du sélecteur de format de sortie
output_format = st.radio(
    "Format de sortie :",
    options=["JSON", "Texte brut"],
    index=0
)

uploaded_file = st.file_uploader("Téléchargez une image de CNI", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Image téléchargée', use_container_width=True)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Définition dynamique du prompt selon le format
    if output_format == "JSON":
        format_instructions = """ 
**Format de Sortie:**
Fournis la réponse en format JSON valide avec la structure suivante :
{
    "documentType": "string",
    "number": "string",
    "nationality": "string",
    "firstName": "string",
    "lastName": "string",
    "dateOfBirth": "string",
    "sex": "string",
    "height": "string",
    "placeOfBirth": "string",
    "issueDate": "string",
    "expiryDate": "string",
    "placeOfIssue": "string"
}
"""
    else:
        format_instructions = """
**Format de Sortie:**
Fournis la réponse dans un format texte structuré avec :
- Des sections clairement identifiées (Informations personnelles)
- Des listes d'informations organisées

Exemple de structure :
**Informations personnelles:**
- Type de document: ...
- Numéro: ...
- Nationalité: ...
- Prénom: ...
- Nom: ...
- Date de naissance: ...
- Sexe: ...
- Taille: ...
- Lieu de naissance: ...
- Date d'émission: ...
- Date d'expiration: ...
- Lieu d'émission: ...
"""

    prompt = f"""
Analyse l'image d'un document de type "CNI". Ce document est une Carte Nationale d'Identité.

**Structure du document:**
Le document contient généralement :
- Des informations personnelles détaillées

**Instructions d'extraction:**
1. Informations personnelles:
   - documentType (type de document)
   - number (numéro de la CNI)
   - nationality (nationalité)
   - firstName (prénom)
   - lastName (nom)
   - dateOfBirth (date de naissance)
   - sex (sexe)
   - height (taille)
   - placeOfBirth (lieu de naissance)
   - issueDate (date d'émission)
   - expiryDate (date d'expiration)
   - placeOfIssue (lieu d'émission)

{format_instructions}

**Consignes importantes:**
- Sois précis et exhaustif
- Conserve la structure originale
- Ne modifie pas les valeurs
- Signale les éléments ambigus
"""

    response = model.generate_content([prompt, image])
    
    st.subheader("Résultat de l'analyse")
    
    if output_format == "JSON":
        try:
            # Tentative de formatage pour une meilleure lisibilité
            json_data = eval(response.text)
            st.json(json_data)
        except:
            st.write(response.text)
    else:
        st.markdown(response.text)