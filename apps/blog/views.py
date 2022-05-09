from typing import Dict, Any
from django.views.generic import TemplateView
from .models import BigSlider, Feature

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['sliders'] = BigSlider.objects.filter(is_publish=True,
                                                      page='').order_by('-id')
        context['features'] = Feature.objects.filter(is_publish=True,
                                                     page='').order_by('-id')
        return context