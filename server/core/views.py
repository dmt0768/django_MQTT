from django.shortcuts import render, HttpResponse
from core.models import Types, Messages
import sqlite3


def main_page(request):
    Types_ = Types.objects.all()
    Messages_ = Messages.objects.all()
    return render(request, 'core/Main_page.html', {'Topics': Types_, 'Messages': Messages_})


def load(request):
    conn = sqlite3.connect('/home/dmitriy/work/demo_wristbands_git/server/db.sqlite3')
    cursor = conn.cursor()
    type_id = request.GET['topic_id']
    data = cursor.execute('SELECT message_id, type_id, message, time FROM core_messages WHERE type_id='+type_id)
    text = '\n'.join(list(map(str, data)))
    topic = cursor.execute('SELECT topic FROM core_types WHERE type_id='+type_id)
    text = 'type_id=' + type_id + ';  ' + str(topic.fetchall()) + '\n\n' + text
    return HttpResponse(text)
