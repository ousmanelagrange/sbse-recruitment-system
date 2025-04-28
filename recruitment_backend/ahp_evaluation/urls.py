from django.urls import path
from .views import CandidateFormViewSet

candidate_form_list = CandidateFormViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

candidate_form_detail = CandidateFormViewSet.as_view({
    'delete': 'destroy'
})

urlpatterns = [
    path('candidate-forms/', candidate_form_list, name='candidate-form-list-create'),
    path('candidate-forms/<int:pk>/', candidate_form_detail, name='candidate-form-delete'),
]
