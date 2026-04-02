from django.test import TestCase, Client
from django.urls import reverse
from .models import Categoria, Repuesto, MovimientoStock

class RepuestosTestCase(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Electrónica')
        self.rep = Repuesto.objects.create(
            categoria=self.cat,
            numero_parte='ABC123',
            nombre='Resistor 10k',
            unidad_medida='pcs'
        )
        self.client = Client()

    def test_repuesto_str(self):
        self.assertEqual(str(self.rep), 'Resistor 10k (ABC123)')

    def test_list_view(self):
        url = reverse('repuestos:list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Resistor 10k')

    def test_create_and_delete(self):
        create_url = reverse('repuestos:create')
        data = {'categoria': self.cat.pk, 'numero_parte': 'DEF456', 'nombre': 'Capacitor 1uF', 'descripcion':'', 'unidad_medida':'pcs','minimo_reposicion':0,'activo':True}
        res = self.client.post(create_url, data, follow=True)
        self.assertContains(res, 'Capacitor 1uF')
        rep_pk = Repuesto.objects.get(numero_parte='DEF456').pk
        delete_url = reverse('repuestos:delete', args=[rep_pk])
        res2 = self.client.post(delete_url, follow=True)
        self.assertNotContains(res2, 'Capacitor 1uF')

class MovimientoStockTestCase(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Mecánica')
        self.rep = Repuesto.objects.create(categoria=self.cat, numero_parte='XYZ789', nombre='Tuerca M8')
        self.client = Client()

    def test_movimiento_list_and_create(self):
        url_list = reverse('repuestos:movimientos_list')
        res = self.client.get(url_list)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Sin movimientos.')
        url_create = reverse('repuestos:movimientos_create')
        data = {'repuesto': self.rep.pk, 'tipo': MovimientoStock.TIPO_ENTRADA, 'cantidad': 5, 'referencia': 'ingreso', 'notas': ''}
        res2 = self.client.post(url_create, data, follow=True)
        self.assertContains(res2, 'Tuerca M8')

class ServicesTestCase(TestCase):
    def test_erp_client_defaults(self):
        from .services import ERPClient
        client = ERPClient()
        self.assertTrue(client.base_url.startswith('http'))
        self.assertIn('Authorization', client.headers)