import logging

from django.shortcuts import render

logging.basicConfig(filename='C:/Python Projects/django_social/py_logs.log', level=logging.INFO, encoding="UTF-8")
logger = logging.getLogger(__name__)


def index(request):
    logger.info(f"Пользователь зашёл на стартовую страницу")
    return render(request, 'social_network/index.html')
