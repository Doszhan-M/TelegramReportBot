from django.views.generic import ListView
from .models import Score



class GraphicList(ListView):
    model = Score
    template_name = 'server/report.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scores'] = Score.objects.all().order_by('date_score')
        return context


