
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from .forms import ClienteForm, VendedorForm, ProformaForm
from .models import Cliente, Vendedor, Proforma, Bu, Pago, Moneda

from django.contrib.auth.decorators import login_required

# Create your views here


@login_required
def inicio(request):
    return render(request, 'principal.html')


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(
                username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect(to='inicio')

        data["form"] = formulario
    return render(request, 'registration/registro.html', data)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'

# -------CLIENTE--------


class ClienteView(View):

    def get(self, request):
        listaClientes = Cliente.objects.all()
        formCliente = ClienteForm()
        context = {
            'clientes': listaClientes,
            'formClientes': formCliente
        }
        return render(request, 'clientes.html', context)


class ClienteAgregarView(View):
    def get(self, request):
        formCliente = ClienteForm()
        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)

    def post(self, request):
        formCliente = ClienteForm(request.POST)
        if formCliente.is_valid():
            formCliente.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('cliente')

        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)


class ClienteEditarView(View):
    def get(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        formCliente = ClienteForm(instance=cliente)
        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)

    def post(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        formCliente = ClienteForm(request.POST, instance=cliente)
        if formCliente.is_valid():
            formCliente.save()
            # Redirige a la lista de clientes después de guardar correctamente
            return redirect('cliente')

        context = {
            'formCliente': formCliente,
        }
        return render(request, 'agregarCliente.html', context)


class ClienteEliminarView(View):
    def post(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        cliente.delete()
        return JsonResponse({'message': 'Cliente eliminado correctamente'})

# ---------FIN CLIENTE---------------------------


class VendedorView(View):
    def get(self, request):
        listaVendedores = Vendedor.objects.all()
        formVendedor = VendedorForm()
        context = {
            'vendedores': listaVendedores,
            'formVendedores': formVendedor
        }
        return render(request, 'vendedor.html', context)


class VendedorAgregarView(View):
    def get(self, request):
        formVendedor = VendedorForm()

        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)

    def post(self, request):
        formVendedor = VendedorForm(request.POST)
        if formVendedor.is_valid():
            # Realizar validación personalizada si es necesario
            formVendedor.save()
            # Redireccionar a la misma página de agregar vendedor después de guardar correctamente
            return redirect('vendedor')

        # Si el formulario no es válido o hubo algún error, renderizar el template con el formulario y los errores
        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)


class VendedorEditarView(View):
    def get(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        formVendedor = VendedorForm(instance=vendedor)
        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)

    def post(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        formVendedor = VendedorForm(request.POST, instance=vendedor)
        if formVendedor.is_valid():
            formVendedor.save()
            # Redirige a la lista de vendedores después de guardar correctamente
            return redirect('vendedor')

        context = {
            'formVendedor': formVendedor,
        }
        return render(request, 'agregar_vendedor.html', context)


class VendedorEliminarView(View):
    def post(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        vendedor.delete()
        return JsonResponse({'message': 'Vendedor eliminado correctamente'})
# ---------FIN Vendedor---------------------------


class ProformaView(View):
    def get(self, request):
        listaProformas = Proforma.objects.all()
        context = {
            'proformas': listaProformas
        }
        return render(request, 'proforma.html', context)


class ProformaAgregarView(View):
    def get(self, request):
        # Obtener las listas de objetos para cada modelo
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        # Crear el formulario y ocultar los campos de "correo" y "celular"
        formProforma = ProformaForm()
        formProforma.fields['correo'].widget.attrs['hidden'] = True
        formProforma.fields['celular'].widget.attrs['hidden'] = True

        context = {
            'formProforma': formProforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }
        return render(request, 'agregar_proforma.html', context)

    def post(self, request):
        formProforma = ProformaForm(request.POST)
        if formProforma.is_valid():
            formProforma.save()
            return redirect('proforma')

        # Si el formulario no es válido, volvemos a mostrarlo con los errores
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        # Ocultar los campos de "correo" y "celular"
        formProforma.fields['correo'].widget.attrs['hidden'] = True
        formProforma.fields['celular'].widget.attrs['hidden'] = True

        context = {
            'formProforma': formProforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }
        return render(request, 'agregar_proforma.html', context)


class ProformaEditarView(View):
    def get(self, request, pk):
        proforma = get_object_or_404(Proforma, pk=pk)
        formProforma = ProformaForm(instance=proforma)

        # Obtener las listas de objetos para cada modelo
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        context = {
            'formProforma': formProforma,
            'proforma': proforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }

        return render(request, 'agregar_proforma.html', context)

    def post(self, request, pk):
        proforma = get_object_or_404(Proforma, pk=pk)
        formProforma = ProformaForm(request.POST, instance=proforma)

        if formProforma.is_valid():
            formProforma.save()
            return redirect('proforma')

        # Si el formulario no es válido, volvemos a mostrarlo con los errores
        lista_bu = Bu.objects.all()
        lista_pago = Pago.objects.all()
        lista_moneda = Moneda.objects.all()
        lista_vendedor = Vendedor.objects.all()

        context = {
            'formProforma': formProforma,
            'proforma': proforma,
            'lista_bu': lista_bu,
            'lista_pago': lista_pago,
            'lista_moneda': lista_moneda,
            'lista_vendedor': lista_vendedor,
        }

        return render(request, 'agregar_proforma.html', context)


class ProformaEliminarView(View):
    def post(self, request, pk):
        proforma = get_object_or_404(Proforma, pk=pk)
        proforma.delete()
        return JsonResponse({'message': 'Proforma eliminada correctamente'})


def get_vendedor_data(request, vendedor_id):
    try:
        vendedor = Vendedor.objects.get(pk=vendedor_id)
        data = {
            'correo': vendedor.correo,
            'celular': vendedor.celular,
        }
        return JsonResponse(data)
    except Vendedor.DoesNotExist:
        return JsonResponse({'error': 'Vendedor no encontrado'}, status=404)


def duplicar_proforma(request, proforma_id):
    original_proforma = Proforma.objects.get(pk=proforma_id)
    nueva_proforma = original_proforma
    nueva_proforma.pk = None  # Asignar None para crear una nueva proforma
    nueva_proforma.save()
    return redirect('proforma')  # Redirigir a la página de todas las proformas


class CotizacionView(View):
    def get(self, request):
        listaCotizaciones = Cotizacion.objects.all()
        context = {
            'cotizaciones': listaCotizaciones
        }
        return render(request, 'cotizacion.html', context)


class CotizacionAgregarView(View):
    def get(self, request):
        # Obtener las listas de objetos para cada modelo (puedes personalizar esto según tus necesidades)
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        # Crear una instancia del formulario de cotización
        form_cotizacion = CotizacionForm()

        context = {
            # Agregar esta línea para pasar la variable cotizacion al contexto
            'formCotizacion': form_cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes
        }

        return render(request, 'agregar_cotizacion.html', context)

    def post(self, request):
        # Obtener las listas de objetos para cada modelo (puedes personalizar esto según tus necesidades)
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        # Crear una instancia del formulario de cotización con los datos enviados por el usuario
        form_cotizacion = CotizacionForm(request.POST)

        if form_cotizacion.is_valid():
            form_cotizacion.save()
            # Redirige a la lista de cotizaciones después de guardar correctamente
            return redirect('cotizacion')

        context = {
            'form_cotizacion': form_cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes,
        }

        return render(request, 'agregar_cotizacion.html', context)


class CotizacionEditarView(View):
    def get(self, request, pk):
        cotizacion = get_object_or_404(Cotizacion, pk=pk)
        form_cotizacion = CotizacionForm(instance=cotizacion)

        # Obtener las listas de objetos para cada modelo
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        context = {
            'form_Cotizacion': form_cotizacion,
            'cotizacion': cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes
        }

        return render(request, 'agregar_cotizacion.html', context)

    def post(self, request, pk):
        cotizacion = get_object_or_404(Cotizacion, pk=pk)
        form_cotizacion = CotizacionForm(request.POST, instance=cotizacion)

        if form_cotizacion.is_valid():
            form_cotizacion.save()
            return redirect('cotizacion')

        # Si el formulario no es válido, volvemos a mostrarlo con los errores
        lista_proformas = Proforma.objects.all()
        lista_clientes = Cliente.objects.all()

        context = {
            'form_cotizacion': form_cotizacion,
            'cotizacion': cotizacion,
            'lista_proformas': lista_proformas,
            'lista_clientes': lista_clientes
        }

        return render(request, 'agregar_cotizacion.html', context)


class CotizacionEliminarView(View):
    def post(self, request, pk):
        cotizacion = get_object_or_404(Cotizacion, pk=pk)
        cotizacion.delete()
        return JsonResponse({'message': 'Cotizacion eliminada correctamente'})
    
def detalle_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion,pk=pk)
    context = {
        'cotizacion': cotizacion
    }
    return render(request, 'detalle_cotizacion.html', context)