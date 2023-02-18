from django.shortcuts import render
from storage.models import game
from django.forms.models import model_to_dict
import json

from storage.models import settings


# Create your views here.
def play(request):
    user = request.user
    instance = settings.objects.get(user=user)
    game_config = model_to_dict(instance, fields=[field.name for field in instance._meta.fields if field.name not in ['id', 'user']])


    if request.method == 'POST':
        problems = request.POST['problems']
        score = json.loads(request.POST['score'])
        params = request.POST['params']            
        game.objects.create(user=user, score=score, ques=problems, params=params)
        return render(request, 'play/play.html', {'game_config': game_config})
    else:
        return render(request, 'play/play.html', {'game_config': game_config})