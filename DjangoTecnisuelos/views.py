# views.py
import math
from pyexpat.errors import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from core.models import LegalClient, Client, FielTrial, Inventory, LaboratoryTrial, LaboratoryWorker
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from core.forms import CustomUserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from io import BytesIO


def index(request):
    return render(request, "index.html")

def inicio(request):
    return render(request, "inicio.html")

def servicios(request):
    return render(request, "servicios.html")


def agendar(request):
    return render(request, "agendar.html")


def cronograma(request):
    return render(request, "cronograma.html")


def administrador(request):
    return render(request, "administrador.html")


def histoInformes(request):
    return render(request, "histoInformes.html")


def contacto(request):
    return render(request, "contactos.html")


def recuperar_contrasena(request):
    return render(request, "RecupContra.html")


def error404(request, exceptiopn):
    return render(request, "404.html", status=404)


def error500(request):
    return render(request, "500.html", status=500)


def laboratorista(request):
    return render(request, "laboratorista.html")


def persona_natural(request):
    return render(request, "Pnatural.html")

def persona_juridica(request):
    return render(request, "Pjuridica.html")

def anuncioR(request):
    return render(request, "AnuncioR.html")

def nuevaC(request):
    return render(request, "nuevaC.html")

def contraseñaC(request):
    return render(request, "contraseñaC.html")


def reset_done (request):
    return render(request, "reset_done.html")


def confirmar_cita_email(request):
    return render(request, "confirmar_cita_email.html")

def export_pdf_report_test(request):
    # Mapeo de nombres de campos en inglés a español
    field_names = {
        "id": "ID",
        "engineer_name": "Nombre del Ingeniero",
        "natural_client": "Cliente Natural",
        "legal_client": "Cliente Legal",
        "date": "Fecha",
        "TypeOfTest_es": "Tipo de Prueba (Escarificaciones)",
        "TypeOfTest_soi": "Tipo de Prueba (Análisis de suelo)",
        "TypeOfTest_comp": "Tipo de Prueba (Prueba de Compactación)",
        "city": "Ciudad",
        "address": "Dirección",
        "pdf_file": "PDF 1",
        "pdf_file_1": "PDF 2",
        "pdf_file_2": "PDF 3",
    }

    # Crear la respuesta HTTP y el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="laboratory_trial_report.pdf"'

    # Obtener los datos de los FielTrial
    fiel_trials = FielTrial.objects.all()

    # Crear el documento PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Informe de Prueba de Campo")

    for trial in fiel_trials:
        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        image_width = 200
        image_height = 50
        image_x = 50
        image_y = 700  # Ajusta esta posición hacia abajo para dejar espacio para las tablas

        pdf.drawImage(image_path, x=image_x, y=image_y, width=image_width, height=image_height)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 650, "Resultado de Pruebas de Campo")  # Ajusta la posición del título

        # Separador
        pdf.line(50, 670, 450, 670)  # Ajusta la posición de la línea

        # Coordenadas iniciales
        x = 50
        y = 550

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Resultado"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 250, line_height, fill=True)
        pdf.rect(x + 250, y, 250, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 250 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for field in field_names.keys():
            # Obtener el valor del campo
            field_value = str(getattr(trial, field))

            # Calcular la altura necesaria para el texto
            text_height = pdf.stringWidth(field_value, "Helvetica", 10)
            num_lines = max(1, int(math.ceil(text_height / (250 - 20))))  # 250 es el ancho del cuadro

            # Ajustar la posición Y si se necesita más espacio
            if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                pdf.showPage()  # Cambiar de página
                y = 750  # Restablecer la posición Y inicial

                # Logo
                pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

                # Título
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(50, 700, "Resultado de Prueba de Campo")

                # Separador
                pdf.line(50, 690, 550, 690)

                # Coordenadas iniciales
                x = 50
                y = 650

                # Encabezados de tabla
                pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
                pdf.rect(x, y, 250, line_height, fill=True)
                pdf.rect(x + 250, y, 250, line_height, fill=True)

                # Color de texto para los encabezados
                pdf.setFillColor(colors.white)
                pdf.setFont("Helvetica-Bold", 12)

                # Dibujar encabezados
                pdf.drawString(x + 20, y + 4, headers[0])
                pdf.drawString(x + 250 + 20, y + 4, headers[1])

                # Restaurar color de texto
                pdf.setFillColor(colors.black)

            # Dibujar cuadro alrededor del campo
            pdf.rect(x, y - num_lines * line_height, 250, num_lines * line_height, stroke=True)
            pdf.rect(x + 250, y - num_lines * line_height, 250, num_lines * line_height, stroke=True)

            # Escribir el nombre del campo
            pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, field_names[field])

            # Si el campo es un PDF, mostrar el nombre del archivo
            if field.startswith("pdf_file"):
                pdf.drawString(x + 250 + 5, y - 10 - (num_lines - 1) * line_height, field_value if field_value else "No disponible")

            # Si no es un PDF, escribir el valor del campo
            else:
                pdf.drawString(x + 250 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

            # Actualizar la posición Y
            y -= num_lines * line_height

        # Agregar espacio entre pruebas
        pdf.showPage()

    # Guardar el PDF y devolver la respuesta
    pdf.save()

    return response

def export_pdf_report_labo(request):
    # Mapeo de nombres de campos en inglés a español
    field_names = {
        "id": "ID",
        "laboratory_name": "Nombre del Laboratorista",
        "natural_client": "Cliente Natural",
        "legal_client": "Cliente Legal",
        "test_date": "Fecha de Prueba",
        "test_type_1": "Tipo de Prueba 1",
        "test_type_2": "Tipo de Prueba 2",
        "test_type_3": "Tipo de Prueba 3",
        "city": "Ciudad",
        "address": "Dirección",
        "pdf_file_1": "PDF 1",
        "pdf_file_2": "PDF 2",
        "pdf_file_3": "PDF 3",
    }

    # Crear la respuesta HTTP y el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="laboratory_trial_report.pdf"'

    # Obtener los datos de los LaboratoryTrial
    laboratory_trials = LaboratoryTrial.objects.all()

    # Crear el documento PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Informe de Prueba de Laboratorio")

    for trial in laboratory_trials:
        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        image_width = 200
        image_height = 50
        image_x = 50
        image_y = 700  # Ajusta esta posición hacia abajo para dejar espacio para las tablas

        pdf.drawImage(image_path, x=image_x, y=image_y, width=image_width, height=image_height)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 650, "Resultado de Laboratorio")  # Ajusta la posición del título

        # Separador
        pdf.line(50, 670, 450, 670)  # Ajusta la posición de la línea

        # Coordenadas iniciales
        x = 50
        y = 550

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Resultado"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 250, line_height, fill=True)
        pdf.rect(x + 250, y, 250, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 250 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for field in field_names.keys():
            # Obtener el valor del campo
            field_value = str(getattr(trial, field))

            # Calcular la altura necesaria para el texto
            text_height = pdf.stringWidth(field_value, "Helvetica", 10)
            num_lines = max(1, int(math.ceil(text_height / (250 - 20))))  # 250 es el ancho del cuadro

            # Ajustar la posición Y si se necesita más espacio
            if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                pdf.showPage()  # Cambiar de página
                y = 750  # Restablecer la posición Y inicial

                # Logo
                pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

                # Título
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(50, 700, "Resultado de Laboratorio")

                # Separador
                pdf.line(50, 690, 550, 690)

                # Coordenadas iniciales
                x = 50
                y = 650

                # Encabezados de tabla
                pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
                pdf.rect(x, y, 250, line_height, fill=True)
                pdf.rect(x + 250, y, 250, line_height, fill=True)

                # Color de texto para los encabezados
                pdf.setFillColor(colors.white)
                pdf.setFont("Helvetica-Bold", 12)

                # Dibujar encabezados
                pdf.drawString(x + 20, y + 4, headers[0])
                pdf.drawString(x + 250 + 20, y + 4, headers[1])

                # Restaurar color de texto
                pdf.setFillColor(colors.black)

            # Dibujar cuadro alrededor del campo
            pdf.rect(x, y - num_lines * line_height, 250, num_lines * line_height, stroke=True)
            pdf.rect(x + 250, y - num_lines * line_height, 250, num_lines * line_height, stroke=True)

            # Escribir el nombre del campo
            pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, field_names[field])

            # Si el campo es un PDF, mostrar el nombre del archivo
            if field.startswith("pdf_file_"):
                pdf.drawString(x + 250 + 5, y - 10 - (num_lines - 1) * line_height, field_value if field_value else "No disponible")

            # Si no es un PDF, escribir el valor del campo
            else:
                pdf.drawString(x + 250 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

            # Actualizar la posición Y
            y -= num_lines * line_height

        # Agregar espacio entre pruebas
        pdf.showPage()

    # Guardar el PDF y devolver la respuesta
    pdf.save()

    return response

def export_pdf_report_inve(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Inventory_report.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))
    image_path = 'static/Imagenes/logito.jpg'   
    pdf.drawImage(image_path, x=20, y=550, width=200, height=50)
    col_widths = [pdf.stringWidth(field.verbose_name, 'Helvetica', 10) + 35 for field in Inventory._meta.fields]
    row_height = 16  
    table_width = sum(col_widths)
    table_height = row_height * 2
    x = 90
    y = pdf._pagesize[1] - 120  
    text_y = y + (row_height / 2) - 4
    pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.rect(x, y, table_width, row_height, fill=True)
    pdf.setFont("Helvetica-Bold", 10) 
    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    for i, field in enumerate(Inventory._meta.fields):
        pdf.setFillColor(colors.white)
        text_width = pdf.stringWidth(field.verbose_name, 'Helvetica', 10)
        text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
        pdf.drawString(text_x, text_y, field.verbose_name)
        pdf.setFillColor(colors.black) 

    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    inventorys = Inventory.objects.all()
    pdf.setFont("Helvetica", 10) 
    for inventory in inventorys:
        y -= row_height
        for i, field in enumerate(Inventory._meta.fields):
            value = str(getattr(inventory, field.name))
            text_width = pdf.stringWidth(value[:15], 'Helvetica', 10)
            text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
            pdf.drawString(text_x, y, value[:15])  

    pdf.setTitle("Informe de Inventario")

    pdf.showPage()
    pdf.save()
    return response

def export_pdf_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="client_natural_report.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))
    image_path = 'static/Imagenes/logito.jpg'   
    pdf.drawImage(image_path, x=20, y=550, width=200, height=50)
    col_widths = [pdf.stringWidth(field.verbose_name, 'Helvetica', 10) + 35 for field in Client._meta.fields]
    row_height = 16  
    table_width = sum(col_widths)
    table_height = row_height * 2
    x = 30
    y = pdf._pagesize[1] - 120  
    text_y = y + (row_height / 2) - 4
    pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.rect(x, y, table_width, row_height, fill=True)
    pdf.setFont("Helvetica-Bold", 10) 
    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    for i, field in enumerate(Client._meta.fields):
        pdf.setFillColor(colors.white)
        text_width = pdf.stringWidth(field.verbose_name, 'Helvetica', 10)
        text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
        pdf.drawString(text_x, text_y, field.verbose_name)
        pdf.setFillColor(colors.black) 

    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    clients = Client.objects.all()
    pdf.setFont("Helvetica", 10) 
    for client in clients:
        y -= row_height
        for i, field in enumerate(Client._meta.fields):
            value = str(getattr(client, field.name))
            text_width = pdf.stringWidth(value[:15], 'Helvetica', 10)
            text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
            pdf.drawString(text_x, y, value[:15])  

    pdf.setTitle("Informe Clientes Naturales")

    pdf.showPage()
    pdf.save()
    return response

def export_pdf_report_juri(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="client_juiridico_report.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))
    image_path = 'static/Imagenes/logito.jpg'   
    pdf.drawImage(image_path, x=20, y=550, width=200, height=50)
    col_widths = [pdf.stringWidth(field.verbose_name, 'Helvetica', 10) + 35 for field in LegalClient._meta.fields]
    row_height = 16  
    table_width = sum(col_widths)
    table_height = row_height * 2
    x = 30
    y = pdf._pagesize[1] - 120  
    text_y = y + (row_height / 2) - 4
    pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.rect(x, y, table_width, row_height, fill=True)
    pdf.setFont("Helvetica-Bold", 10) 
    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    for i, field in enumerate(Client._meta.fields):
        pdf.setFillColor(colors.white)
        text_width = pdf.stringWidth(field.verbose_name, 'Helvetica', 10)
        text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
        pdf.drawString(text_x, text_y, field.verbose_name)
        pdf.setFillColor(colors.black) 

    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    clients = Client.objects.all()
    pdf.setFont("Helvetica", 10) 
    for client in clients:
        y -= row_height
        for i, field in enumerate(Client._meta.fields):
            value = str(getattr(client, field.name))
            text_width = pdf.stringWidth(value[:15], 'Helvetica', 10)
            text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
            pdf.drawString(text_x, y, value[:15])  

    pdf.setTitle("Informe Clientes Juridicos")

    pdf.showPage()
    pdf.save()
    return response

def store_cliente(request):
    if request.method == "POST":
        # Obtén los datos del formulario POST
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        numero = request.POST.get("numero")
        direccion = request.POST.get("direccion")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        email = request.POST.get("email")

        # Crea una nueva instancia de Client con los datos recibidos
        nuevo_cliente = Client(
            name_client=nombre,
            last_name_client=apellido,
            cell_number=numero,
            address=direccion,
            date=fecha,
            time=hora,
            email=email,
        )
        # Guarda el nuevo cliente en la base de datos
        nuevo_cliente.save()

        # Envío del correo de confirmación
        subject = 'Confirmación de Cita'
        message = f'Gracias por confirmar su cita señor(a) {nombre}. Su cita está programada para el {fecha} a las {hora}. Esperamos verte pronto.\nFecha de la cita:{fecha}\n - Hora de la cita: {hora}'
        from_email = settings.EMAIL_HOST_USER
        to_email = email  # Utiliza el correo del cliente como destinatario

        # Puedes usar un template de correo HTML para un formato más sofisticado
        html_message = render_to_string('confirmar_cita_email.html', {'message': message})

        send_mail(subject, message, from_email, [to_email], html_message=html_message)


        # Redirige a una página de éxito o a donde desees
        return HttpResponseRedirect("/servicios/")

    # Si no es una solicitud POST, renderiza la página del formulario
    return render(request, "servicios.html")

def store_cliente_juridica(request):
    if request.method == "POST":
        # Obtén los datos del formulario POST
        razonSocial = request.POST.get("razonSocial")
        nit = request.POST.get("nit")
        numero = request.POST.get("numero")
        direccion = request.POST.get("direccion")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        email = request.POST.get("email")

        # Crea una nueva instancia de Client con los datos recibidos
        nuevo_cliente = LegalClient(
            registered_name=razonSocial,
            nit=nit,
            cell_number=numero,
            address=direccion,
            date=fecha,
            time=hora,
            email=email,
        
           
        )

        # Guarda el nuevo cliente en la base de datos
        nuevo_cliente.save()
        # Envío del correo de confirmación
        subject = 'Confirmación de Cita'
        message = f'Gracias por confirmar su cita {razonSocial} con numero de nit: {nit} . Su cita está programada para el {fecha} a las {hora}. Esperamos verte pronto.'
        from_email = settings.EMAIL_HOST_USER
        to_email = email  # Utiliza el correo del cliente como destinatario

        # Puedes usar un template de correo HTML para un formato más sofisticado
        html_message = render_to_string('confirmar_cita_email.html', {'message': message})

        send_mail(subject, message, from_email, [to_email], html_message=html_message)

        # Redirige a una página de éxito o a donde desees
        return HttpResponseRedirect("/servicios/")

    # Si no es una solicitud POST, renderiza la página del formulario
    return render(request, "servicios.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Bienvenido {}".format(user.username))
            return redirect("admin:index")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "inicio.html", {})

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión finalizada")
    return redirect("inicio")

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inicio")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, "crearCuenta.html", {"form": form})


