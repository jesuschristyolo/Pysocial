import subprocess

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
import traceback

from django.views.decorators.csrf import csrf_exempt

from ribbon.models import Posts, Comment, Like
from users.models import User


class TimeoutError(Exception):
    pass


def execute_code(code):
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
    if request.method == 'POST':

        if 'create_post' in request.POST:
            Posts.objects.create(text_content=request.POST.get('post_content', None),
                                 code_content=request.POST.get('codearea', None),
                                 output_content=execute_code(request.POST.get('codearea', None)),
                                 author=request.user)
            return redirect('ribbon:general_ribbon')

        if request.POST['codearea']:
            print(request.POST)
            codeareadata = request.POST['codearea'] if request.POST['codearea'] else None
            post_content = request.POST['post_content'] if request.POST['post_content'] else None
            output = execute_code(codeareadata)
            print(output)
            return render(request, 'ribbon/create_new_post.html',
                          {"code": codeareadata, "output": output, "post_content": post_content})

        return render(request, 'ribbon/create_new_post.html')

    if request.method == 'GET':
        return render(request, 'ribbon/create_new_post.html')


def change_post(request, post_id):
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
            print(request.POST)
            codeareadata = request.POST['codearea'] if request.POST['codearea'] else None
            post_content = request.POST['post_content'] if request.POST['post_content'] else None
            output = execute_code(codeareadata)
            print(output)
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
    posts = Posts.objects.all().order_by("timestamp")
    liked_posts = [post.id for post in posts if Like.objects.filter(author=request.user, post_like=post).exists()]
    liked_comments = [comment.id for comment in Comment.objects.all() if
                      Like.objects.filter(author=request.user, comment_like=comment).exists()]

    if request.method == 'POST':
        print(request.POST)
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
        print(request.GET, 'get')
        return render(request, 'ribbon/general_ribbon.html', {"posts": posts,
                                                              "liked_posts": liked_posts,
                                                              "liked_comments": liked_comments})


@csrf_exempt
def submit_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        print(request.POST, 'submit')
        post_id = request.POST['post_id']

        new_comment = Comment.objects.create(author=request.user, content=comment_text,
                                             post_comment=Posts.objects.get(pk=post_id))

        print('ok', "[", new_comment.author.username, new_comment.author.photo.url, new_comment.content,
              new_comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "]")
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
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        try:
            post = Posts.objects.get(pk=post_id)
        except:
            return JsonResponse({'success': False})

        if not Like.objects.filter(author=request.user, post_like=post).exists():
            new_like = Like.objects.create(author=request.user, post_like=post)
            likes_count = post.count_likes()
            print('add')
            return JsonResponse({'success': True, 'likes_count': likes_count, 'action': 'add'})
        else:
            Like.objects.filter(author=request.user, post_like=post).delete()
            likes_count = post.count_likes()
            print('delete')
            return JsonResponse({'success': True, 'likes_count': likes_count, 'action': 'delete'})

    return JsonResponse({'success': False})


def like_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        try:
            comment = Comment.objects.get(pk=comment_id)
        except:
            return JsonResponse({'success': False})

        user = request.user
        liked = Like.objects.filter(author=user, comment_like=comment).exists()
        if liked:
            Like.objects.filter(author=user, comment_like=comment).delete()
            action = 'delete'
        else:
            Like.objects.create(author=user, comment_like=comment)
            action = 'add'
        likes_count = comment.comment_like.count()
        return JsonResponse({'success': True, 'action': action, 'likes_count': likes_count})
    return JsonResponse({'success': False})
