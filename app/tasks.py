from __future__ import absolute_import, unicode_literals
from celery import shared_task
from PIL import Image
from django.apps import apps 
from django.conf import settings
import time

@shared_task(name="repeat_order_make_task")
def repeat_order_make_task():
    return "необязательная заглушка"

@shared_task(name="make_watermark_task")
def make_watermark_task(this_id):
    make_watermark = apps.get_model(app_label='app', model_name='MakeWatermark')
    curr_time = round(time.time()*1000)
    res = False
    try:
        background = Image.open(f'{settings.MEDIA_ROOT}/{make_watermark.objects.filter(id=this_id)[0].image_before}')
        foreground = Image.open(f'{settings.MEDIA_ROOT}/watermark.png').convert('RGBA')
        background.paste(foreground, (0, 0), foreground)
        background.save(f'{settings.MEDIA_ROOT}/afterWatermark/{curr_time}.png')
        make_watermark.objects.filter(id=this_id).update(image_after=f'afterWatermark/{curr_time}.png', done=True)
        return True
    except:
        pass
    return res