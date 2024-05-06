import subprocess
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
import traceback
from django.views.decorators.csrf import csrf_exempt
from ribbon.models import Posts, Comment, Like
from users.models import User
import logging

# используем имя модуля для названия текущего логгера
logging.basicConfig(filename='C:/Python Projects/django_social/py_logs.log', level=logging.INFO, encoding="UTF-8")
logger = logging.getLogger(__name__)


class TimeoutError(Exception):
    """Исключение, возникающее при превышении времени выполнения кода."""


def execute_code(code):
    """
    Выполняет переданный пользователем код в отдельном процессе. С тайм-аутом в 5 секунд
    по истечении которого процесс завершается и срабатывает пользовательское исключение
    """

    try:
        # Запускаем выполнение кода в отдельном процессе
        process = subprocess.Popen(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Ждем выполнения процесса с таймаутом 5 секунд
        stdout, stderr = process.communicate(timeout=5)
        output = stdout.decode('utf-8')

        # Проверяем наличие ошибок в stderr
        if stderr:
            output += "\nErrors:\n" + stderr.decode('utf-8')

    except subprocess.TimeoutExpired:
        # Если превышено время ожидания, прекращаем процесс
        process.kill()
        process.communicate()
        output = str(TimeoutError("Execution timed out (5 seconds)"))
    except Exception as e:
        # Преобразуем исключение в строку
        output = str(e)
        traceback.print_exc()  # Для вывода трассировки стека в консоль, можно убрать в продакшене

    return output


def create_new_post(request):
    """
    Создает новый пост на основе данных, полученных из формы.
    Если метод запроса POST и в форме есть данные, создает новый пост и перенаправляет пользователя на общую ленту.
    Если в форме есть код, выполняет его и возвращает результат выполнения вместе с данными из формы для отображения.
    """

    if request.method == 'POST':

        if 'create_post' in request.POST:
            Posts.objects.create(text_content=request.POST.get('post_content', None),
                                 code_content=request.POST.get('codearea', None),
                                 output_content=execute_code(request.POST.get('codearea', None)),
                                 author=request.user)
            return redirect('ribbon:general_ribbon')

        if request.POST['codearea']:
            codeareadata = request.POST['codearea'] if request.POST['codearea'] else None
            post_content = request.POST['post_content'] if request.POST['post_content'] else None
            output = execute_code(codeareadata)
            return render(request, 'ribbon/create_new_post.html',
                          {"code": codeareadata, "output": output, "post_content": post_content})

        return render(request, 'ribbon/create_new_post.html')

    if request.method == 'GET':
        return render(request, 'ribbon/create_new_post.html')


def change_post(request, post_id):
    """
    Изменяет существующий пост на основе данных, полученных из формы.

    Если метод запроса POST и в форме есть данные, изменяет существующий пост и перенаправляет пользователя на общую ленту.
    Если в форме есть код, выполняет его и возвращает результат выполнения вместе с данными из формы для отображения.

    Поведение:

        - Если запрос отправлен методом POST и пользователь нажал кнопку "изменить пост":
         изменяет существующий пост и перенаправляет пользователя на общую ленту.
        - Если в форме есть код, и пользователь нажал кнопку: "Run Code":
         выполняет его и возвращает результат выполнения вместе с данными из формы для отображения.
        - Если запрос отправлен методом GET, отображает форму изменения поста с текущим содержимым
        (кодом и комментарием к коду).
        - Если запрашиваемый пост не существует или передан неверный идентификатор, возвращает ошибку 404.
        - В случае возникновения исключений при выполнении кода, возвращает ошибку с соответствующим сообщением.

    """
    if request.method == 'POST':

        if 'change_post' in request.POST:
            post = Posts.objects.get(pk=post_id)
            post.text_content = request.POST.get('post_content', None)
            post.code_content = request.POST.get('codearea', None)
            post.output_content = execute_code(request.POST.get('codearea', None))
            post.author = request.user
            post.save()
            return redirect('ribbon:general_ribbon')

        if request.POST['codearea']:
            codeareadata = request.POST['codearea'] if request.POST['codearea'] else None
            post_content = request.POST['post_content'] if request.POST['post_content'] else None
            output = execute_code(codeareadata)
            return render(request, 'ribbon/change_post.html',
                          {"code": codeareadata, "output": output, "post_content": post_content, 'post_id': post_id})

        return render(request, 'ribbon/change_post.html', {'post_id': post_id})

    if request.method == 'GET':
        changing_post = Posts.objects.get(pk=post_id)
        code = changing_post.code_content
        output = changing_post.output_content
        post_content = changing_post.text_content
        return render(request, 'ribbon/change_post.html',
                      {"code": code, "output": output, "post_content": post_content, 'post_id': post_id})


def data_generation(user_object=None, sort_category=None, sort_user=None):
    """
    Функция для генерации данных постов в зависимости от выбранных параметров сортировки.

    user_object (User, optional): Объект пользователя, для которого выполняется фильтрация (по умолчанию None).
    sort_category (str, optional): Категория сортировки постов (по количеству комментариев, лайков и т.д.)
                                   (по умолчанию None).
    sort_user (str, optional): Пользователь, для которого выполняется фильтрация постов (по умолчанию None).

    Поведение:
        - В зависимости от переданных параметров сортировки и фильтрации генерирует QuerySet с постами.
        - Посты могут быть отсортированы по различным категориям (количеству комментариев, лайков и т.д.),
          либо отфильтрованы по авторству конкретного пользователя.
        - Если не переданы параметры сортировки и фильтрации, возвращает все посты, отсортированные по дате добавления.
    """
    posts = None

    if sort_user is None:

        if sort_category == "count_comments":
            posts = Posts.objects.annotate(num_comments=Count('post_comment')).order_by('-num_comments')

        elif sort_category == 'count_likes_on_posts':
            posts = Posts.objects.annotate(num_likes=Count('post_like')).order_by('-num_likes')

        elif sort_category == 'new ones first':
            posts = Posts.objects.all().order_by("-timestamp")

        elif sort_category == 'only_friends':
            posts = Posts.objects.filter(author__in=user_object.friends.all())

    else:

        if sort_category == "count_comments":
            posts = Posts.objects.filter(author=User.objects.get(username=sort_user)).annotate(
                num_comments=Count('post_comment')).order_by(
                '-num_comments')

        elif sort_category == 'count_likes_on_posts':
            posts = Posts.objects.filter(author=User.objects.get(username=sort_user)).annotate(
                num_likes=Count('post_like')).order_by('-num_likes')

        elif sort_category == 'new ones first':
            posts = Posts.objects.filter(author=User.objects.get(username=sort_user)).order_by("-timestamp")

        elif sort_category == 'only_friends':
            posts = Posts.objects.filter(author__in=user_object.friends.all())

    return posts


def general_ribbon(request):
    """
    Представление для отображения общей ленты постов с возможностью добавления постов, фильтрации и сортировки.

    Поведение:
        - Если запрос отправлен методом POST и переданы параметры фильтрации и сортировки, генерирует и отображает
          ленту постов в соответствии с этими параметрами.
        - Если запрос отправлен методом GET, отображает ленту постов с применением текущих фильтров и сортировки.
        - Пользователь может фильтровать посты по категории (количеству комментариев, лайков и т.д.) и/или
          выбирать конкретного пользователя для отображения его постов.
    """
    posts = Posts.objects.all().order_by("timestamp")
    liked_posts = [post.id for post in posts if Like.objects.filter(author=request.user, post_like=post).exists()]
    liked_comments = [comment.id for comment in Comment.objects.all() if
                      Like.objects.filter(author=request.user, comment_like=comment).exists()]

    if request.method == 'POST':
        filter_user = request.POST.get('filter_user', None)
        category = request.POST.get('category', None)
        if filter_user == "-":
            # Обработка случая, когда выбрано значение "-"
            if category == "-":
                # Если выбраны оба значения "-", то просто перенаправляем обратно на страницу
                return redirect('ribbon:general_ribbon')
            else:
                # Только категория
                posts = data_generation(user_object=request.user, sort_category=category)

        else:
            if category == "-":
                # Обработка случая, когда выбран только пользователь
                posts = Posts.objects.filter(author=User.objects.get(username=filter_user)).order_by("timestamp")
            else:
                # Обработка случая, когда выбран пользователь и категория
                posts = data_generation(user_object=request.user, sort_category=category, sort_user=filter_user)

        return render(request, 'ribbon/general_ribbon.html', {"posts": posts,
                                                              "liked_posts": liked_posts,
                                                              "liked_comments": liked_comments})
    else:
        return render(request, 'ribbon/general_ribbon.html', {"posts": posts,
                                                              "liked_posts": liked_posts,
                                                              "liked_comments": liked_comments})


@csrf_exempt
def submit_comment(request):
    """

    Это представление отправляет новый комментарий к посту. Если метод запроса POST,
    создает новый комментарий на основе данных из запроса
    и возвращает JSON-ответ с данными нового комментария.
    Если метод запроса не POST, возвращает JSON-ответ об ошибке.

    """
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        post_id = request.POST['post_id']

        new_comment = Comment.objects.create(author=request.user, content=comment_text,
                                             post_comment=Posts.objects.get(pk=post_id))

        logger.info(f"{new_comment.author.username} Оставил комментарий"
                    f"Посту с id {new_comment.post_comment.pk}")

        new_comment_data = {
            'author_username': new_comment.author.username,
            'author_photo': new_comment.author.photo.url,
            'content': new_comment.content,
            'timestamp': new_comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Вернуть JSON-ответ с данными нового комментария
        return JsonResponse({'success': True, 'comment': new_comment_data})
    else:
        # Вернуть JSON-ответ об ошибке, если запрос не POST
        return JsonResponse({'success': False, 'error': 'Метод запроса должен быть POST'})


def like_post(request):
    """
     Это представление обрабатывает действия по лайку к посту. Если метод запроса POST,
     то оно добавляет лайк к посту, если пользователь еще не лайкал этот
     пост, или удаляет лайк, если пользователь уже лайкал пост.
     Возвращает JSON-ответ с информацией об успешности выполнения операции,
     количестве лайков после действия и типе действия (добавление или удаление).
    """

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        try:
            post = Posts.objects.get(pk=post_id)
        except:
            return JsonResponse({'success': False})

        if not Like.objects.filter(author=request.user, post_like=post).exists():
            new_like = Like.objects.create(author=request.user, post_like=post)
            likes_count = post.count_likes()
            logger.info(f"{new_like.author} Поставил лайк"
                        f"Посту с id {new_like.post_like.pk}")
            return JsonResponse({'success': True, 'likes_count': likes_count, 'action': 'add'})
        else:
            Like.objects.filter(author=request.user, post_like=post).delete()
            likes_count = post.count_likes()
            logger.info(f"{request.user.username} Удалил лайк"
                        f"с поста {post.pk}")
            return JsonResponse({'success': True, 'likes_count': likes_count, 'action': 'delete'})

    return JsonResponse({'success': False})


def like_comment(request):
    """
    Это представление обрабатывает действия по лайку к комментарию.
    Если метод запроса POST, то оно добавляет лайк к комментарию,
    если пользователь еще не лайкал этот комментарий, или удаляет лайк,
    если пользователь уже лайкал комментарий. Возвращает JSON-ответ
    с информацией об успешности выполнения операции, типе действия
    (добавление или удаление) и количестве лайков после действия.
    """

    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        try:
            comment = Comment.objects.get(pk=comment_id)
        except:
            return JsonResponse({'success': False})

        user = request.user
        if Like.objects.filter(author=user, comment_like=comment).exists():
            Like.objects.filter(author=user, comment_like=comment).delete()
            action = 'delete'
        else:
            Like.objects.create(author=user, comment_like=comment)
            action = 'add'
        likes_count = comment.comment_like.count()
        return JsonResponse({'success': True, 'action': action, 'likes_count': likes_count})
    return JsonResponse({'success': False})
