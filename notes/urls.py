from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CategoryViewSet, TagViewSet, NoteViewSet, NoteHistoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = router.urls

# Adicionando a rota manualmente para o histórico
urlpatterns += [
    path('notes/<int:pk>/history/', NoteHistoryViewSet.as_view({'get': 'list'}), name='note-history'),
]
