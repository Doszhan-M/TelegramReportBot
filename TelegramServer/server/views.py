from django.views.generic import ListView
from .models import Payment, Score



class GraphicList(ListView):
    model = Score
    template_name = 'server/graphic.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        context['score'] = Score.objects.all()
        return context


