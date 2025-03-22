import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
# Instead of importing stop_words, use the following import
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stop_words

class PCAAnalyzerWithSelection:
    def __init__(self, n_components=2, max_features=1000):
        self.n_components = n_components
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words=list(sklearn_stop_words),  # Utilisation des stopwords français
            ngram_range=(1, 2),
            strip_accents='unicode',
            token_pattern=r'(?u)\b\w+\b'
        )
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=n_components)
        self.selected_candidates = []
        self.min_cvs = 3  # Nombre minimum de CVs requis

    def validate_analysis(self, cvs, employer_criteria):
        """Vérifie les préconditions pour l'analyse"""
        errors = []
        print(not len(cvs) > self.n_components, len(cvs) < self.n_components)
        if not len(cvs) > self.n_components:
            errors.append(f"number of  components must be between 0 and min(n_samples, n_features)={len(cvs)})")

        if not employer_criteria:
            errors.append("Liste de critères employeur vide")

        if len(set(cvs)) < 2:
            errors.append("Les CVs doivent être distincts")

        return errors

    def _calculate_criteria_score(self, cv, criteria):
        """Calcule un score personnalisé basé sur les critères employeur"""
        return sum(cv.lower().count(crit.lower()) for crit in criteria)

    def process_and_select(self, cvs, employer_criteria, threshold=0.8):
        """Traite une liste de CVs, extrait les caractéristiques, applique l'ACP et sélectionne les candidats."""
        # Validation initiale
        if errors := self.validate_analysis(cvs, employer_criteria):
            return None, None, errors

        # Extraction des caractéristiques
        tfidf_matrix = self.vectorizer.fit_transform(cvs).toarray()

        # Calcul des scores de critères
        criteria_scores = np.array([
            [self._calculate_criteria_score(cv, employer_criteria)]
            for cv in cvs
        ])

        # Combinaison des caractéristiques
        features = np.hstack((tfidf_matrix, criteria_scores))

        # Normalisation et ACP
        scaled = self.scaler.fit_transform(features)
        pca_results = self.pca.fit_transform(scaled)

        # Création du DataFrame avec scores
        df = pd.DataFrame(
            pca_results,
            columns=[f"PC{i+1}" for i in range(self.n_components)]
        )
        df['Critère_Score'] = criteria_scores
        df['CV'] = [f"Candidat {i+1}" for i in range(len(cvs))]

        # Sélection basée sur la position dans l'espace PCA et les scores
        mean_scores = df[['PC1', 'Critère_Score']].mean(axis=1)
        self.selected_candidates = df[mean_scores > threshold * mean_scores.max()]['CV'].tolist()

        return df, self.pca.explained_variance_ratio_, self.selected_candidates


# Test du module avec des CV complets
if __name__ == "__main__":
    # Exemple de CVs complets (des textes longs)
    cv_examples = [
        """Jean Dupont
        Développeur Python senior avec 8 ans d'expérience.
        Compétences : Machine Learning, Deep Learning, Data Analysis, Django, Flask, react.
        Diplômes : Master en Informatique de l'Université de Paris.
        Expérience dans des projets internationaux et en startup.""",

        """Marie Martin
        Ingénieure en informatique spécialisée en Data Science.
        Forte expérience en analyse de données, en statistiques, et en développement de solutions d'IA.
        Diplômes : Doctorat en Statistiques, certifications en Big Data et Python.""",

        """Luc Bernard
        Développeur web et mobile, expert en JavaScript, React, Node.js, et Flutter.
        5 ans d'expérience dans la création de solutions multiplateformes.
        Expérience dans des entreprises de technologie de pointe.""",
        """Alice Morel**  
           Spécialiste en cybersécurité avec 6 ans d'expérience en pentesting et en analyse de vulnérabilités.  
           Diplômes : Master en Sécurité Informatique.  
           Compétences : Kali Linux, SIEM, gestion des risques.  
        """,
        """Paul Lefevre**  
           Architecte logiciel avec 10 ans d'expérience dans la conception d'applications cloud.  
           Diplômes : Ingénieur en Informatique.  
           Compétences : AWS, Azure, Kubernetes, Microservices.  """,

        """Sophie Durand**  
           Data Analyst avec une expertise en BI et visualisation de données.  
           Diplômes : Master en Statistiques et Big Data.  
           Compétences : Tableau, Power BI, SQL, Python.  """,

        """Hugo Robert**  
           Ingénieur Machine Learning, passionné par l'IA et les modèles prédictifs.  
           Diplômes : Master en Intelligence Artificielle.  
           Compétences : TensorFlow, PyTorch, NLP, Computer Vision.  """,

        """Camille Laurent**  
       Développeuse backend spécialisée en Go et Rust.  
       Diplômes : Ingénieure en Informatique.  
       Expérience : 7 ans dans le développement d'APIs haute performance.  """,

        """Thomas Garnier**  
       Expert DevOps et automatisation d'infrastructure.  
       Diplômes : Master en Cloud Computing.  
       Compétences : Docker, Kubernetes, CI/CD, Terraform.  """,

        """
        Laura Fontaine**  
        Ingénieure Data Science, spécialisée en analyse et transformation de données massives.  
        Diplômes : Master en Science des Données.  
        Compétences : Spark, Hadoop, SQL, Python.  """,

        """Antoine Girard**  
         Ingénieur en intelligence artificielle et vision par ordinateur.  
         Diplômes : Doctorat en Informatique.  
         Compétences : Computer Vision, GANs, OpenCV, Deep Learning.  
         """,

    ]


    # Critères définis par l'employeur (optionnel)
    # employer_criteria = ["python", "machine learning", "data", "java", "react"]

    employer_needs = ["python", "machine learning", "data", "JavaScript", "react"]

    analyzer = PCAAnalyzerWithSelection(n_components=10)
    results, variance, selected = analyzer.process_and_select(cv_examples, employer_needs)

    print("Résultats PCA avec scores :")
    print(results)
    print("\nCandidats sélectionnés :", selected)
    print("Variance expliquée :", variance)