from django.shortcuts import render

def main_page(request):
    return render(request, 'inmobiliariaVR/main_page.html')