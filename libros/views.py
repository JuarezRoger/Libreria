from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Categoria, Libro, Resena, CarritoItem, Contacto
import json
import random

def home(request):
    libros_list = Libro.objects.all()
    categorias = Categoria.objects.all()
    
    paginator = Paginator(libros_list, 15)
    page = request.GET.get('page', 1)
    
    try:
        libros = paginator.page(page)
    except PageNotAnInteger:
        libros = paginator.page(1)
    except EmptyPage:
        libros = paginator.page(paginator.num_pages)
    
    return render(request, 'libros/home.html', {
        'libros': libros,
        'categorias': categorias
    })

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    resenas = libro.resenas.all()[:10]
    libros_relacionados = []
    if libro.categoria:
        libros_relacionados = Libro.objects.filter(categoria=libro.categoria).exclude(id=libro_id)[:4]
    return render(request, 'libros/detalle_libro.html', {
        'libro': libro,
        'resenas': resenas,
        'libros_relacionados': libros_relacionados
    })

def por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    libros = Libro.objects.filter(categoria=categoria)
    categorias = Categoria.objects.all()
    return render(request, 'libros/por_categoria.html', {
        'categoria': categoria,
        'libros': libros,
        'categorias': categorias
    })

def buscar(request):
    query = request.GET.get('q', '')
    libros = []
    if query:
        libros = Libro.objects.filter(titulo__icontains=query) | Libro.objects.filter(autor__icontains=query)
    return render(request, 'libros/buscar.html', {
        'query': query,
        'libros': libros
    })

def agregar_carrito(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.user.is_authenticated:
        item, created = CarritoItem.objects.get_or_create(
            usuario=request.user,
            libro=libro,
            defaults={'cantidad': 1}
        )
        if not created:
            item.cantidad += 1
            item.save()
    else:
        cart = request.session.get('cart', {})
        libro_id_str = str(libro_id)
        if libro_id_str in cart:
            cart[libro_id_str] += 1
        else:
            cart[libro_id_str] = 1
        request.session['cart'] = cart
    
    messages.success(request, f'{libro.titulo} agregado al carrito')
    return redirect('libros:detalle_libro', libro_id=libro_id)

def eliminar_carrito(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
        item.delete()
    else:
        cart = request.session.get('cart', {})
        item = get_object_or_404(CarritoItem, id=item_id)
        libro_id_str = str(item.libro_id)
        if libro_id_str in cart:
            del cart[libro_id_str]
            request.session['cart'] = cart
        item.delete()
    return redirect('libros:carrito')

@require_POST
def actualizar_carrito(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    else:
        item = get_object_or_404(CarritoItem, id=item_id)
    
    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad > 0:
        item.cantidad = cantidad
        item.save()
    else:
        item.delete()
    return redirect('libros:carrito')

def carrito(request):
    if request.user.is_authenticated:
        items = CarritoItem.objects.filter(usuario=request.user)
    else:
        cart = request.session.get('cart', {})
        items = []
        for libro_id, cantidad in cart.items():
            try:
                libro = Libro.objects.get(id=libro_id)
                item = CarritoItem(libro=libro, cantidad=cantidad)
                items.append(item)
            except Libro.DoesNotExist:
                pass
    
    total = sum(item.subtotal for item in items)
    return render(request, 'libros/carrito.html', {
        'items': items,
        'total': total
    })

@require_POST
def agregar_resena(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    calificacion = int(request.POST.get('calificacion', 5))
    comentario = request.POST.get('comentario', '')
    nombre = request.POST.get('nombre', 'Anonimo')
    
    if request.user.is_authenticated:
        Resena.objects.create(
            libro=libro,
            usuario=request.user,
            calificacion=calificacion,
            comentario=comentario
        )
    else:
        Resena.objects.create(
            libro=libro,
            usuario=None,
            calificacion=calificacion,
            comentario=f"{comentario} (por: {nombre})"
        )
    
    messages.success(request, 'Resena agregada correctamente')
    return redirect('libros:detalle_libro', libro_id=libro_id)

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')
        Contacto.objects.create(nombre=nombre, email=email, telefono=telefono, mensaje=mensaje)
        messages.success(request, 'Mensaje enviado correctamente')
        return redirect('libros:contacto')
    return render(request, 'libros/contacto.html')

def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '').lower()
            
            libros = list(Libro.objects.all()[:10])
            
            respuestas = {
                'hola': 'Hola! Bienvenido a nuestra libreria. En que puedo ayudarte hoy?',
                'buenos': 'Hola! En que puedo ayudarte?',
                'adios': 'Hasta luego! Que disfrutes de tu lectura.',
                'chau': 'Hasta luego! Que disfrutes de tu lectura.',
                'precio': 'Los precios de nuestros libros varian. Hay algum libro en particular que te interese?',
                'costo': 'Los precios de nuestros libros varian. Hay algum libro en particular que te interese?',
                'catalogo': f'Tenemos {len(libros)} libros disponibles. Que genero te interesa?',
                'libros': f'Tenemos {len(libros)} libros disponibles. Que genero te interesa?',
                'disponible': 'Si! Tenemos libros disponibles. Cual te gustaria comprar?',
                'comprar': 'Puedes agregar libros al carrito y proceder con la compra. Que libro te interesa?',
                'recomendar': 'Con gusto te recomiendo! Que genero o tema te interesa?',
                'recomendacion': 'Con gusto te recomiendo! Que genero o tema te interesa?',
                'autor': 'Buscas libros de algum autor en particular? Tenemos muchas opciones.',
                'genero': 'Tenmos generos varios: Ficcion, Ciencia, Historia, Infantil y mas. Cual te interesa?',
                'ninos': 'Tenmos una seccion de libros infantiles. Para que edad?',
                'infantil': 'Tenmos una seccion de libros infantiles. Para que edad?',
                'contacto': 'Puedes contactarnos a traves de la pagina de contacto. En que puedo ayudarte?',
                'ayuda': 'Puedo ayudarte a buscar libros, recomendarte segun tus intereses, o resolver dudas sobre precios y disponibilidad.',
            }
            
            respuesta = None
            for clave, valor in respuestas.items():
                if clave in mensaje:
                    respuesta = valor
                    break
            
            if not respuesta:
                if libros:
                    libro_random = random.choice(libros)
                    respuesta = f"Te recomiendo '{libro_random.titulo}' de {libro_random.autor}. Es un excelente libro! Te gustaria saber mas?"
                else:
                    respuesta = 'Por favor, visita nuestro catalogo para ver todos nuestros libros disponibles.'
            
            return JsonResponse({'respuesta': respuesta})
        except Exception as e:
            return JsonResponse({'respuesta': 'Lo siento, estoy tenendo problemas. Puedes repetir?'}, status=500)
    return render(request, 'libros/chatbot.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('libros:home')
        else:
            messages.error(request, 'Usuario o contrasena incorrectas')
    return render(request, 'libros/login.html')

def logout_view(request):
    logout(request)
    return redirect('libros:home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente')
            return redirect('libros:home')
    else:
        form = UserCreationForm()
    return render(request, 'libros/register.html', {'form': form})

@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('libros:home')
    
    total_libros = Libro.objects.count()
    total_resenas = Resena.objects.count()
    total_contactos = Contacto.objects.count()
    libros_stock_bajo = Libro.objects.filter(stock__lte=5)
    
    reseñas_mes = Resena.objects.filter(
        fecha_creacion__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    libros_top = Libro.objects.annotate(
        num_resenas=Count('resenas')
    ).order_by('-num_resenas')[:5]
    
    reseñas_por_libro = []
    for libro in libros_top:
        reseñas_por_libro.append({
            'titulo': libro.titulo,
            'autor': libro.autor,
            'categoria': libro.categoria,
            'precio': libro.precio,
            'stock': libro.stock,
            'resenas': libro.resenas.count(),
            'promedio': libro.promedio_resenas
        })
    
    todos_libros = []
    for libro in Libro.objects.all().order_by('-id'):
        todos_libros.append({
            'titulo': libro.titulo,
            'autor': libro.autor,
            'categoria': libro.categoria,
            'precio': libro.precio,
            'stock': libro.stock,
            'resenas': libro.resenas.count(),
            'promedio': libro.promedio_resenas
        })
    
    ultimas_resenas = Resena.objects.all()[:10]
    
    context = {
        'total_libros': total_libros,
        'total_resenas': total_resenas,
        'total_contactos': total_contactos,
        'libros_stock_bajo': libros_stock_bajo,
        'reseñas_mes': reseñas_mes,
        'reseñas_por_libro': reseñas_por_libro,
        'todos_libros': todos_libros,
        'ultimas_resenas': ultimas_resenas,
    }
    return render(request, 'libros/admin_panel.html', context)

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('libros:admin_panel')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('libros:admin_panel')
        else:
            messages.error(request, 'Credenciales incorrectas o no tienes acceso de administrador')
    return render(request, 'libros/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('libros:admin_login')

@login_required
def editar_libro(request, libro_id):
    if not request.user.is_staff:
        return redirect('libros:home')
    
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        libro.titulo = request.POST.get('titulo')
        libro.autor = request.POST.get('autor')
        libro.descripcion = request.POST.get('descripcion')
        libro.isbn = request.POST.get('isbn')
        libro.fecha_publicacion = request.POST.get('fecha_publicacion')
        libro.precio = request.POST.get('precio')
        libro.stock = request.POST.get('stock')
        libro.en_oferta = request.POST.get('en_oferta') == 'on'
        libro.precio_oferta = request.POST.get('precio_oferta') or None
        
        categoria_id = request.POST.get('categoria')
        if categoria_id:
            libro.categoria = Categoria.objects.get(id=categoria_id)
        
        libro.save()
        messages.success(request, f'Libro "{libro.titulo}" actualizado correctamente')
        return redirect('libros:admin_panel')
    
    categorias = Categoria.objects.all()
    return render(request, 'libros/editar_libro.html', {
        'libro': libro,
        'categorias': categorias
    })

@login_required
def eliminar_libro(request, libro_id):
    if not request.user.is_staff:
        return redirect('libros:home')
    
    libro = get_object_or_404(Libro, id=libro_id)
    libro.delete()
    messages.success(request, 'Libro eliminado correctamente')
    return redirect('libros:admin_panel')

@login_required
def nuevo_libro(request):
    if not request.user.is_staff:
        return redirect('libros:home')
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        descripcion = request.POST.get('descripcion')
        isbn = request.POST.get('isbn')
        fecha_publicacion = request.POST.get('fecha_publicacion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        en_oferta = request.POST.get('en_oferta') == 'on'
        precio_oferta = request.POST.get('precio_oferta') or None
        
        categoria_id = request.POST.get('categoria')
        categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
        
        libro = Libro.objects.create(
            titulo=titulo,
            autor=autor,
            descripcion=descripcion,
            isbn=isbn,
            fecha_publicacion=fecha_publicacion,
            precio=precio,
            stock=stock,
            en_oferta=en_oferta,
            precio_oferta=precio_oferta,
            categoria=categoria
        )
        
        messages.success(request, f'Libro "{libro.titulo}" creado correctamente')
        return redirect('libros:admin_panel')
    
    categorias = Categoria.objects.all()
    return render(request, 'libros/nuevo_libro.html', {'categorias': categorias})

@login_required
def gestionar_ofertas(request):
    if not request.user.is_staff:
        return redirect('libros:home')
    
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        libro = get_object_or_404(Libro, id=libro_id)
        libro.en_oferta = request.POST.get('en_oferta') == 'on'
        libro.precio_oferta = request.POST.get('precio_oferta') or None
        libro.save()
        messages.success(request, 'Oferta actualizada correctamente')
        return redirect('libros:gestionar_ofertas')
    
    libros = Libro.objects.all().order_by('-en_oferta', '-precio')
    return render(request, 'libros/gestionar_ofertas.html', {'libros': libros})
