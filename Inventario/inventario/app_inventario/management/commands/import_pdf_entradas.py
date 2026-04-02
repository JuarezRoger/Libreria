import pdfplumber
import re
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app_inventario.models import Repuesto


def parse_int(value):
    if value is None:
        return 0
    s = str(value).strip()
    # eliminar separadores de miles comunes y reemplazar comas decimales por puntos si aplica
    s = s.replace('.', '').replace(',', '.')
    # extraer número entero (antes del punto) o convertir a float y tomar int
    try:
        f = float(re.findall(r'[-+]?[0-9]*[.,]?[0-9]+', s)[0])
        return int(round(f))
    except Exception:
        raise ValueError(f"No se pudo parsear cantidad: {value}")


class Command(BaseCommand):
    help = "Importa entradas desde un PDF. El PDF debe contener columnas con 'numero_parte' y 'cantidad'."

    def add_arguments(self, parser):
        parser.add_argument('pdf_path', type=str)
        parser.add_argument('--crear-si-no-existe', action='store_true', help='Crear repuesto si no existe (con nombre=numero_parte)')
        parser.add_argument('--referencia', type=str, default='', help='Referencia de importación (opcional)')

    def handle(self, *args, **options):
        path = options['pdf_path']
        crear = options['crear_si_no_existe']
        referencia = options['referencia']

        rows = []
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    # intenta extraer tablas
                    tables = page.extract_tables()
                    for t in tables:
                        # cada t es lista de filas; asumimos encabezado o columnas [numero_parte, cantidad, ...]
                        for row in t:
                            rows.append(row)
        except Exception as e:
            raise CommandError(f"Error abriendo PDF: {e}")

        if not rows:
            raise CommandError("No se encontraron tablas en el PDF. Revisa el formato o usa OCR si es escaneado.")

        # Intentaremos detectar cabeceras y columnas
        header = [c.lower().strip() if c else '' for c in rows[0]]
        col_numero = None
        col_cantidad = None
        for i, h in enumerate(header):
            if 'parte' in h or 'numero' in h or 'part' in h:
                col_numero = i
            if 'cant' in h or 'qty' in h or 'cantidad' in h:
                col_cantidad = i
        # si no detecta encabezado, asumimos que cada fila tiene numero_parte en 0 y cantidad en 1
        start = 1 if col_numero is not None and col_cantidad is not None else 0
        if col_numero is None:
            col_numero = 0
        if col_cantidad is None:
            col_cantidad = 1

        processed = 0
        errors = []
        with transaction.atomic():
            for r in rows[start:]:
                try:
                    numero = (r[col_numero] or '').strip()
                    cantidad_raw = r[col_cantidad] if len(r) > col_cantidad else ''
                    cantidad = parse_int(cantidad_raw)
                    if not numero:
                        continue
                    try:
                        repu = Repuesto.objects.get(numero_parte=numero)
                        repu.cantidad = (repu.cantidad or 0) + cantidad
                        repu.save()
                    except Repuesto.DoesNotExist:
                        if crear:
                            repu = Repuesto.objects.create(numero_parte=numero, nombre=numero, cantidad=cantidad)
                        else:
                            raise
                    processed += 1
                except Exception as e:
                    errors.append(f"Fila {r}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Procesadas {processed} filas."))
        if errors:
            for e in errors[:20]:
                self.stdout.write(self.style.ERROR(e))
            self.stdout.write(self.style.WARNING(f"Errores totales: {len(errors)}"))
