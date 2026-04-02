from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categorías'
    
    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    descripcion = models.TextField()
    isbn = models.CharField(max_length=20, unique=True)
    fecha_publicacion = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    en_oferta = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    @property
    def promedio_resenas(self):
        resenas = self.resenas.all()
        if resenas:
            return sum(r.calificacion for r in resenas) / len(resenas)
        return 0
    
    @property
    def precio_final(self):
        if self.en_oferta and self.precio_oferta:
            return self.precio_oferta
        return self.precio

class Resena(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    calificacion = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        if self.usuario:
            return f"{self.usuario.username} - {self.libro.titulo}"
        return f"Anónimo - {self.libro.titulo}"

class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cantidad} x {self.libro.titulo}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.libro.precio_final

class Contacto(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"{self.nombre} - {self.email}"
