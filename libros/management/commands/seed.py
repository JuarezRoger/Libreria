from django.core.management.base import BaseCommand
from libros.models import Categoria, Libro
from django.core.files import File
from urllib.request import urlopen
from tempfile import TemporaryFile
import os

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para la librería'

    def handle(self, *args, **options):
        self.stdout.write('Creando categorías...')
        
        categorias = [
            {'nombre': 'Ficción', 'descripcion': 'Novelas y historias de ficción'},
            {'nombre': 'Ciencia', 'descripcion': 'Libros de ciencia y tecnología'},
            {'nombre': 'Historia', 'descripcion': 'Libros históricos y biografías'},
            {'nombre': 'Infantil', 'descripcion': 'Libros para niños'},
            {'nombre': 'Autoayuda', 'descripcion': 'Desarrollo personal y motivación'},
        ]
        
        for cat_data in categorias:
            Categoria.objects.get_or_create(nombre=cat_data['nombre'], defaults={'descripcion': cat_data['descripcion']})
        
        ficcion = Categoria.objects.get(nombre='Ficción')
        ciencia = Categoria.objects.get(nombre='Ciencia')
        historia = Categoria.objects.get(nombre='Historia')
        infantil = Categoria.objects.get(nombre='Infantil')
        autoayuda = Categoria.objects.get(nombre='Autoayuda')
        
        self.stdout.write('Creando libros...')
        
        libros_data = [
            {
                'titulo': 'El Código Da Vinci',
                'autor': 'Dan Brown',
                'descripcion': 'Una novela de suspenso que gira en torno a los secretos del Priorato de Sion y los misterios del Santo Grial. El symbólogo Robert Langdon se ve envuelto en una conspiración religiosa que lo lleva a través de París y Londres.',
                'isbn': '978-0307474278',
                'fecha_publicacion': '2003-03-18',
                'precio': 24.99,
                'stock': 15,
                'categoria': ficcion,
            },
            {
                'titulo': 'Cien Años de Soledad',
                'autor': 'Gabriel García Márquez',
                'descripcion': 'La saga de la familia Buendía en el pueblo ficticio de Macondo. Una obra maestra de la literatura latinoamericana que mezcla realismo mágico con la historia de Colombia.',
                'isbn': '978-0060883287',
                'fecha_publicacion': '1967-05-30',
                'precio': 19.99,
                'stock': 8,
                'categoria': ficcion,
            },
            {
                'titulo': '1984',
                'autor': 'George Orwell',
                'descripcion': 'Una novela distópica que describe un futuro sombrío donde el gobierno controla cada aspecto de la vida. Winston Smith trabaja en el Ministerio de la Verdad alterando la historia.',
                'isbn': '978-0451524935',
                'fecha_publicacion': '1949-06-08',
                'precio': 15.99,
                'stock': 20,
                'categoria': ficcion,
            },
            {
                'titulo': 'El Principito',
                'autor': 'Antoine de Saint-Exupéry',
                'descripcion': 'Un飞行员坠机在沙漠中，遇到了来自另一个星球的小王子。这是一本关于爱情、失去和纯真的经典寓言书。',
                'isbn': '978-0156012195',
                'fecha_publicacion': '1943-04-06',
                'precio': 12.99,
                'stock': 25,
                'categoria': infantil,
            },
            {
                'titulo': 'Una Breve Historia del Tiempo',
                'autor': 'Stephen Hawking',
                'descripcion': 'Desde el Big Bang hasta los agujeros negros, Hawking explica los conceptos más complejos del universo de manera accesible para el lector común.',
                'isbn': '978-0553380163',
                'fecha_publicacion': '1988-04-01',
                'precio': 18.99,
                'stock': 12,
                'categoria': ciencia,
            },
            {
                'titulo': 'Sapiens: De Animales a Dioses',
                'autor': 'Yuval Noah Harari',
                'descripcion': 'Una breve historia de la humanidad, desde la Edad de Piedra hasta el siglo XXI. Explora cómo Homo sapiens llegó a dominar el planeta.',
                'isbn': '978-0062316097',
                'fecha_publicacion': '2011-01-01',
                'precio': 22.99,
                'stock': 18,
                'categoria': historia,
            },
            {
                'titulo': 'El Poder del Ahora',
                'autor': 'Eckhart Tolle',
                'descripcion': 'Una guía espiritual para vivir en el momento presente. El autor explora cómo liberarse del dolor emocional y encontrar la paz interior.',
                'isbn': '978-1577314806',
                'fecha_publicacion': '1997-08-16',
                'precio': 16.99,
                'stock': 30,
                'categoria': autoayuda,
            },
            {
                'titulo': 'Harry Potter y la Piedra Filosofal',
                'autor': 'J.K. Rowling',
                'descripcion': 'El primer libro de la saga de Harry Potter. Un niño huérfano descubre que es mago y comienza su educación en Hogwarts, donde hace amigos y enfrenta al maligno Voldemort.',
                'isbn': '978-0590353427',
                'fecha_publicacion': '1997-06-26',
                'precio': 21.99,
                'stock': 22,
                'categoria': infantil,
            },
            {
                'titulo': 'El Hobbit',
                'autor': 'J.R.R. Tolkien',
                'descripcion': 'Bilbo Bolsón, un hobbit放心地生活在夏尔，却被迫加入矮人探险队前往孤山，从恶龙史矛革手中夺回宝藏。',
                'isbn': '978-0547928227',
                'fecha_publicacion': '1937-09-21',
                'precio': 14.99,
                'stock': 16,
                'categoria': ficcion,
            },
            {
                'titulo': 'El富爸爸穷爸爸',
                'autor': 'Robert Kiyosaki',
                'descripcion': 'Un libro sobre educación financiera que presenta dos perspectivas diferentes sobre el dinero: la del padre rico y la del padre pobre.',
                'isbn': '978-1612680194',
                'fecha_publicacion': '1997-04-01',
                'precio': 17.99,
                'stock': 14,
                'categoria': autoayuda,
            },
        ]
        
        for libro_data in libros_data:
            libro, created = Libro.objects.get_or_create(
                titulo=libro_data['titulo'],
                defaults=libro_data
            )
            if created:
                self.stdout.write(f'  - Creado: {libro.titulo}')
        
        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(libros_data)} libros y {len(categorias)} categorías'))
