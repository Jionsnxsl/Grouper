from django.shortcuts import render, HttpResponse

# Create your views here.


def homepage(request):
    return render(request, "homepage.html")


def search_view(request):
    fish_batch = request.GET.get("fish_batch")
    print(fish_batch)
    result = {"fish_batch": fish_batch}
    return render(request, "search_result.html", result)
