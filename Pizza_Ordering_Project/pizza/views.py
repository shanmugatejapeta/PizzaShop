from django.shortcuts import render

from .forms import PizzaForm,MorePizzas

from django.forms import formset_factory

from .models import Pizza

def home(request):
    return render(request,"pizza/home.html",{})

def order(request):
    morepizzas=MorePizzas()
    if request.method == 'POST':
        # filled_form=PizzaForm(request.POST,request.FILES)
        filled_form=PizzaForm(request.POST)
        if filled_form.is_valid():
            created_form = filled_form.save()
            created_form_pk=created_form.id

            note="Thank You for Ordering! Your %s %s %s is on the way!" %(filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'],filled_form.cleaned_data['topping2'])
            new_form=PizzaForm()
            return render(request,"pizza/order.html",{'created_form_id':created_form_pk,'pizzaform':new_form,'note':note,'morepizzas':morepizzas})
    else:
        form=PizzaForm()
        return render(request,"pizza/order.html",{'pizzaform':form,'morepizzas':morepizzas})

def pizzas(request):
    number_of_pizzas=2
    more_form=MorePizzas(request.GET)
    if more_form.is_valid():
        print("HIIIII")
        number_of_pizzas=more_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm,extra=number_of_pizzas)
    formset=PizzaFormSet()
    if request.method == 'POST':
        filled_formset=PizzaFormSet(request.POST)
        if filled_formset.is_valid() :
            for form in filled_formset:
                form.save()
                print(form.cleaned_data['topping1'])
                note="Your Pizzas Have been Ordered Successfully"
            return render(request,'pizza/pizzas.html',{'formset':formset,'note':note})
        else:
            print("The form is not valid")
    return render(request,'pizza/pizzas.html',{'formset':formset})

def edit_pizza(request,pk):
    pizza=Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method=='POST':
        filled_form=PizzaForm(request.POST,instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form=filled_form
            note='The Pizza has been edited!'
            return render(request,'pizza/edit_form.html',{'pizza':pizza,'note':note,'form':form})
    return render(request,'pizza/edit_form.html',{'pizza':pizza,'form':form})


    

