from django.shortcuts import render, HttpResponse
from core.models import Topics, Messages
import sqlite3


def main_page(request):
    Topics_ = Topics.objects.all()
    Messages_ = Messages.objects.all()
    return render(request, 'core/Main_page.html', {'Topics': Topics_, 'Messages': Messages_})

def load(request):
    conn = sqlite3.connect('/home/dmitriy/work/demo_wristbands_git/server/db.sqlite3')
    cursor = conn.cursor()
    topic_id = request.GET['topic_id']
    data = cursor.execute('SELECT message_id, topic_id, message, time FROM core_messages WHERE topic_id='+topic_id)
    text = '\n'.join(list(map(str, data)))
    topic = cursor.execute('SELECT topic FROM core_topics WHERE topic_id='+topic_id)
    text = 'topic_id=' + topic_id + ';  ' + str(topic.fetchall()) + '\n\n' + text
    return HttpResponse(text)
