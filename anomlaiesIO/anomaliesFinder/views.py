from django.shortcuts import render

def anomalies_finder_main(request):
    context = {}
    return render(request,
                  'anomaliesFinder/index.html',
                  context=context)
