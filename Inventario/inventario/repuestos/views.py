from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Repuesto, MovimientoStock

class RepuestoListView(ListView):
    model = Repuesto
    template_name = 'repuestos/list.html'
    context_object_name = 'repuestos'

class RepuestoCreateView(CreateView):
    model = Repuesto
    fields = ['categoria','numero_parte','nombre','descripcion','unidad_medida','minimo_reposicion','activo']
    template_name = 'repuestos/form.html'
    success_url = reverse_lazy('repuestos:list')

class RepuestoUpdateView(UpdateView):
    model = Repuesto
    fields = ['categoria','numero_parte','nombre','descripcion','unidad_medida','minimo_reposicion','activo']
    template_name = 'repuestos/form.html'
    success_url = reverse_lazy('repuestos:list')

class RepuestoDeleteView(DeleteView):
    model = Repuesto
    template_name = 'repuestos/confirm_delete.html'
    success_url = reverse_lazy('repuestos:list')

class MovimientoStockListView(ListView):
    model = MovimientoStock
    template_name = 'repuestos/movimientos_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']

class MovimientoStockCreateView(CreateView):
    model = MovimientoStock
    fields = ['repuesto','tipo','cantidad','referencia','notas']
    template_name = 'repuestos/movimientos_form.html'
    success_url = reverse_lazy('repuestos:movimientos_list')

    def form_valid(self, form):
        self.object = form.save()
        # TODO: ajustar stock basado en tipo y cantidad
        return super().form_valid(form)

class DashboardView(TemplateView):
    template_name = 'repuestos/dashboard.html'

    def get_context_data(self, **kwargs):
        from django.db.models import Sum
        context = super().get_context_data(**kwargs)
        context['total_repuestos'] = Repuesto.objects.count()
        context['total_movimientos'] = MovimientoStock.objects.count()
        context['stock_por_repuesto'] = Repuesto.objects.annotate(stock=Sum('movimientostock__cantidad'))
        return context
