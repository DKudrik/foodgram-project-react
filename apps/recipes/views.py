from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RecipeForm


def index(request):
    return render(
        request,
        "index.html",
    )


@login_required
def new_recipe(request):
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(request, "new_recipe.html", {"form": form})
    recipe = form.save(commit=False)
    recipe.author = request.user
    form.save()
    return redirect("index")
