
# Контекстный процессор который возвращает текущего пользователя
def user_object(request):
    return {'user_object': request.user}



