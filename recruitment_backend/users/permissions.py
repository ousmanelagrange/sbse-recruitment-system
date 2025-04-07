from rest_framework.permissions import BasePermission 


class IsEmployer(BasePermission):
    message = "Seuls les employeurs peuvent effectuer cette action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employer'    

class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'candidate'
    
    