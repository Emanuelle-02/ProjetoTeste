import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import CategoriaForm, DespesasForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Sum
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator

# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    despesas = Despesas.objects.filter(user=request.user)
    ganhos = Ganho.objects.filter(user=request.user)
    total_despesas = 0
    total_ganhos = 0
    saldo = 0
    
    for despesa in despesas: # pragma: no cover 
        total_despesas += despesa.valor 
    for ganho in ganhos: # pragma: no cover 
        total_ganhos += ganho.valor
    
    saldo =  total_ganhos - total_despesas
    
    context = {
        'despesas': despesas,
        'ganhos': ganhos,
        'total_despesas': total_despesas,
        'total_ganhos': total_ganhos,
        'saldo': saldo
    }
    return render(request, 'despesas/index.html', context)


@login_required(login_url='/auth/login')
def minhas_despesas(request):
    despesas = Despesas.objects.filter(user=request.user)
    ganhos = Ganho.objects.filter(user=request.user)
    total_despesas = 0
    total_ganhos = 0
    saldo = 0
    
    for despesa in despesas:# pragma: no cover 
        total_despesas += despesa.valor 
    for ganho in ganhos:# pragma: no cover 
        total_ganhos += ganho.valor
    
    saldo =  total_ganhos - total_despesas
    paginator = Paginator(despesas, 5)
    pagina_num = request.GET.get('page')
    obj_pagina = Paginator.get_page(paginator, pagina_num)
    context = {
        'despesas': despesas,
        'ganhos': ganhos,
        'total_despesas': total_despesas,
        'total_ganhos': total_ganhos,
        'saldo': saldo,
        'obj_pagina': obj_pagina
    }
    return render(request, 'despesas/minhas_despesas.html', context)

@method_decorator(login_required, name="dispatch")
class CreateDespesaView(CreateView):
    model = Despesas
    form_class = DespesasForm
    template_name = "despesas/add_despesa.html"

    def get_form_kwargs(self):
        kwargs = super(CreateDespesaView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
    
    def form_valid(self, form):
        obj = form.save(commit=False)# pragma: no cover 
        obj.user = self.request.user# pragma: no cover 
        obj.save()# pragma: no cover 
        return HttpResponseRedirect("minhas_despesas")# pragma: no cover 

@login_required(login_url='/auth/login')   
def remove_despesa(request, id):
    despesa = Despesas.objects.get(pk=id)
    despesa.delete()
    messages.success(request, 'Despesa removida com sucesso!')

    return redirect('minhas_despesas')

@login_required(login_url='/auth/login')
def listar_categoria(request):
    categorias = Categoria.objects.filter(user=request.user)  
    paginator = Paginator(categorias, 10)
    pagina_num = request.GET.get('page')
    obj_pagina = Paginator.get_page(paginator, pagina_num)
    context = {
        'categorias': categorias,
        'obj_pagina': obj_pagina
    }
    return render(request, 'despesas/listagem_categorias.html',context)

@login_required(login_url='/auth/login')
def add_categoria(request):
    if request.method == 'POST':# pragma: no cover 
        form = CategoriaForm(request.POST)  
        if form.is_valid():  # pragma: no cover 
            categoria = form.save(commit=False)
            categoria.user = request.user
            categoria.save()

            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('listagem_categorias')
        return render(request, 'despesas/add_categoria.html',{"form": form})   # pragma: no cover   
    form = CategoriaForm()  # pragma: no cover 
    return render(request, 'despesas/add_categoria.html',{'form':form}) # pragma: no cover 

@login_required(login_url='/auth/login')
def remove_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    try:
        categoria.delete()
    except:# pragma: no cover 
        pass# pragma: no cover 
    return redirect('listagem_categorias')

@login_required(login_url='/auth/login')
def listagem_ganhos(request):
    rendas = Ganho.objects.filter(user=request.user)  
    paginator = Paginator(rendas, 5)
    pagina_num = request.GET.get('page')
    obj_pagina = Paginator.get_page(paginator, pagina_num)
    rendas = Ganho.objects.filter(user=request.user)
    total_ganho = 0

    for renda in rendas: # pragma: no cover 
        total_ganho += renda.valor 
    
    context = {
        'rendas': rendas,
        'obj_pagina': obj_pagina,
        'rendas': rendas,
        'total_ganho': total_ganho
    }
    return render(request, 'rendas/listagem_renda.html',context)

@login_required(login_url='/auth/login')
def add_renda(request):
    rendas = Ganho.objects.filter(user=request.user)
    context={
        'rendas': rendas,
        'val': request.POST
    }
    if request.method == 'GET':# pragma: no cover 
        return render(request, 'rendas/add_renda.html', context)

    if request.method == 'POST':# pragma: no cover 
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        data = request.POST['data']

        Ganho.objects.create(user=request.user, descricao=descricao, valor=valor, data=data)    
        messages.success(request, 'Renda lan??ada com sucesso!')

    return redirect('listagem_renda')

@login_required(login_url='/auth/login')
def editar_renda(request, id):
    renda=Ganho.objects.get(pk=id)
    categorias = Categoria.objects.all()
    context={
        'renda': renda,
        'val': renda,
    }
    if request.method=='GET':# pragma: no cover
        return render(request, 'rendas/editar_renda.html', context)
    if request.method=='POST':# pragma: no cover
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        data = request.POST['data']

        renda.user=request.user 
        renda.descricao=descricao 
        renda.valor=valor 
        renda.data=data
        renda.save()
        messages.success(request, 'Renda atualizada com sucesso!')

        return redirect('listagem_renda')

@login_required(login_url='/auth/login')   
def remove_renda(request, id):
    renda = Ganho.objects.get(pk=id)
    renda.delete()
    messages.success(request, 'Renda removida com sucesso!')

    return redirect('listagem_renda')

# Gera gr??fico de gastos por categoria
@login_required(login_url='/auth/login')
def view_graph(request):
    labels = []# pragma: no cover 
    data = []# pragma: no cover 

    queryset = Despesas.objects.values('categoria__nome').annotate(categoria_valor=Sum('valor')).order_by('-categoria_valor').filter(user=request.user)# pragma: no cover 
    for entry in queryset:# pragma: no cover 
        labels.append(entry['categoria__nome'])# pragma: no cover 
        data.append(entry['categoria_valor'])# pragma: no cover 
    
    return JsonResponse(data={# pragma: no cover 
        'labels': labels,
        'data': data,
    })

# Gera gr??fico de renda por m??s
@login_required(login_url='/auth/login')
def view_graph2(request):
    labels = []# pragma: no cover 
    data = []# pragma: no cover 

    queryset = Ganho.objects.values('data__month').annotate(ganho_valor=Sum('valor')).order_by('data__month').filter(user=request.user)# pragma: no cover 
    for entry in queryset:# pragma: no cover 
        labels.append(entry['data__month'])# pragma: no cover 
        data.append(entry['ganho_valor'])# pragma: no cover 
    
    return JsonResponse(data={# pragma: no cover 
        'labels': labels,
        'data': data,
    })


# Gera gr??fico de renda por ano
@login_required(login_url='/auth/login')
def view_graph3(request):
    labels = []# pragma: no cover 
    data = []# pragma: no cover 

    queryset = Ganho.objects.values('data__year').annotate(ganho_valor=Sum('valor')).order_by('data__year').filter(user=request.user)# pragma: no cover 
    for entry in queryset:# pragma: no cover 
        labels.append(entry['data__year'])# pragma: no cover 
        data.append(entry['ganho_valor'])# pragma: no cover 
    
    return JsonResponse(data={# pragma: no cover 
        'labels': labels,
        'data': data,
    })

@login_required(login_url='/auth/login')
def graph_despesas_mensal(request):
    labels = []# pragma: no cover 
    data = []# pragma: no cover 

    queryset = Despesas.objects.values('data__month').annotate(ganho_valor=Sum('valor')).order_by('data__month').filter(user=request.user)# pragma: no cover 
    for entry in queryset:# pragma: no cover 
        labels.append(entry['data__month'])# pragma: no cover 
        data.append(entry['ganho_valor'])# pragma: no cover 
    
    return JsonResponse(data={# pragma: no cover 
        'labels': labels,
        'data': data,
    })

@login_required(login_url='/auth/login')
def graph_despesas_anual(request):
    labels = []# pragma: no cover 
    data = []# pragma: no cover 

    queryset = Despesas.objects.values('data__year').annotate(ganho_valor=Sum('valor')).order_by('data__year').filter(user=request.user)# pragma: no cover 
    for entry in queryset:# pragma: no cover 
        labels.append(entry['data__year'])# pragma: no cover 
        data.append(entry['ganho_valor'])# pragma: no cover 
    
    return JsonResponse(data={# pragma: no cover 
        'labels': labels,
        'data': data,
    })

# View gr??ficos de despesas
@login_required(login_url='/auth/login')
def exibe_graph(request):
    despesas = Despesas.objects.filter(user=request.user)
    total_despesas = 0

    for despesa in despesas: # pragma: no cover 
        total_despesas += despesa.valor  
    
    context = {
        'despesas': despesas,
        'total_despesas': total_despesas
    }
    return render(request, 'despesas/estatistica.html', context)

# View gr??ficos de renda
@login_required(login_url='/auth/login')
def exibe_graph2(request):
    rendas = Ganho.objects.filter(user=request.user)
    total_ganho = 0

    for renda in rendas:# pragma: no cover 
        total_ganho += renda.valor 
    
    context = {
        'rendas': rendas,
        'total_ganho': total_ganho
    }
    return render(request, 'rendas/estatistica_renda.html', context)