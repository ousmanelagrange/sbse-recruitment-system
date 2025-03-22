from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class CVParsingView(APIView):
    """
    API view for parsing CV documents and extracting structured information.
    """
    
    def extract_info_from_cv(self, cv_text):
        """
        Extract relevant information from CV text using NLP techniques.
        
        Args:
            cv_text (str): The text content of the CV
            
        Returns:
            dict: Structured data extracted from the CV
        """
        # Initialize extracted data dictionary
        extracted_data = {
            'name': '',
            'email': '',
            'phone': '',
            'skills': [],
            'education': [],
            'experience': []
        }
        
        # Extract email using regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, cv_text)
        if email_matches:
            extracted_data['email'] = email_matches[0]
        
        # Extract phone number using regex
        phone_pattern = r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phone_matches = re.findall(phone_pattern, cv_text)
        if phone_matches:
            extracted_data['phone'] = phone_matches[0]
        
        # Extract skills (simplified approach)
        common_skills = ['python', 'java', 'javascript', 'react', 'angular', 'node.js', 
                         'django', 'flask', 'sql', 'nosql', 'mongodb', 'aws', 'docker', 
                         'kubernetes', 'machine learning', 'data analysis', 'git']
        
        tokens = word_tokenize(cv_text.lower())
        for skill in common_skills:
            if skill in ' '.join(tokens):
                extracted_data['skills'].append(skill)
        
        # Simple name extraction (first capitalized words in document)
        lines = cv_text.split('\n')
        for line in lines[:10]:  # Check first 10 lines for name
            words = line.strip().split()
            if len(words) >= 2 and len(words) <= 5:
                capitalized_words = [w for w in words if w[0].isupper() if len(w) > 1]
                if len(capitalized_words) >= 2:
                    extracted_data['name'] = ' '.join(capitalized_words)
                    break
        
        # Note: For a production system, more sophisticated extraction for education and experience would be needed
        # This is a simplified implementation
        
        return extracted_data
    
    def post(self, request, *args, **kwargs):
        """
        Process a CV document and extract structured information.
        
        Request body:
            {
                "cv_url": "URL to the CV document"
            }
            
        Returns:
            Structured JSON data extracted from the CV
        """
        cv_url = request.data.get('cv_url')
        if not cv_url:
            return Response({'error': 'CV URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the CV content from the provided URL
            response = requests.get(cv_url)
            if response.status_code != 200:
                return Response(
                    {'error': f'Failed to fetch CV from the provided URL. Status code: {response.status_code}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the content type to determine how to process the document
            content_type = response.headers.get('Content-Type', '')
            
            if 'application/pdf' in content_type:
                # For a real implementation, you would use a PDF parsing library here
                cv_text = "PDF parsing would be implemented here"
            elif 'text/plain' in content_type:
                cv_text = response.text
            elif 'application/msword' in content_type or 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
                # For a real implementation, you would use a Word document parsing library here
                cv_text = "Word document parsing would be implemented here"
            else:
                # Default to treating as plain text
                cv_text = response.text
            
            # Extract information from the CV text
            extracted_data = self.extract_info_from_cv(cv_text)
            
            return Response(extracted_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': f'Error processing CV: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
