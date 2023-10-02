from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
import json
from books.forms import *
from books.models import *


def main_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    year_set = set()
    tags_with_count = []
    template = get_template('main_page.html')

    if current_user.is_authenticated:

        # fill in 'years' from user books
        date_of_books = list(BookRecord.objects.filter(
            user=request.user,
        ).order_by('dateEnd').values_list('dateEnd', flat=True))
        for dateOfBook in date_of_books:
            if dateOfBook is not None:
                year_set.add(dateOfBook.year)

        # Tag cloud
        tags_with_count = Tag.objects.filter(bookrecord__user=request.user) \
            .values('name') \
            .annotate(tag_count=Count('name')) \
            .distinct()
        min_count = min((tag['tag_count'] for tag in tags_with_count), default=0)
        max_count = max((tag['tag_count'] for tag in tags_with_count), default=0)
        for tag in tags_with_count:
            # Normalize count to the [10, 20] range for font-size
            if max_count == min_count:
                font_size = 15
            else:
                font_size = 10 + (tag['tag_count'] - min_count) * (20 - 10) / (max_count - min_count)
            tag['font_size'] = font_size

    variables = {
        'user': current_user,
        'years': year_set,
        'tags_with_count': tags_with_count,
    }
    output = template.render(variables)
    return HttpResponse(output)


def logout_page(request):
    return LogoutView.as_view()(request)


@csrf_exempt
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    template = get_template('registration/register.html')
    variables = {
        'form': form
    }
    output = template.render(variables)
    return HttpResponse(output)


@csrf_exempt
def edit_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')

    # Save the book record
    if request.method == 'POST':
        form = BookSaveForm(request.POST)
        if form.is_valid():
            book, _ = Book.objects.get_or_create(
                isbn=form.cleaned_data['isbn']
            )
            record, created = BookRecord.objects.get_or_create(
                user=request.user,
                book=book
            )

            # Save book info
            book.url = form.cleaned_data['link']
            if form.cleaned_data['imageLink'] != "":
                book.imageUrl = form.cleaned_data['imageLink']
            book.save()

            # Save book record info
            record.title = form.cleaned_data['title']
            record.author = form.cleaned_data['author']
            if len(form.cleaned_data['memo'].strip()) > 0:
                record.memo = form.cleaned_data['memo']
            else:
                record.memo = None
            record.publisher = form.cleaned_data['publisher']
            record.dateStart = form.cleaned_data['dateStart']
            record.dateEnd = form.cleaned_data['dateEnd']
            if form.cleaned_data['star1'] is not '':
                record.rating = form.cleaned_data['star1']
            else:
                record.rating = 0
            record.check1 = form.cleaned_data['check1']
            record.check2 = form.cleaned_data['check2']
            record.check3 = form.cleaned_data['check3']
            record.tags.clear()
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                record.tags.add(tag)
            record.save()
            # return HttpResponseRedirect('/user/%s' % request.user.username)
            return HttpResponseRedirect('/')
        else: # if form.is_valid():
            return HttpResponse(form.errors.as_json)

    # Edit existing book record
    elif request.method == 'GET':
        form = BookSaveForm()
        record = BookRecord()
        tags = ''
        # If isbn is given, fill in the form with the book record
        if request.GET != {}:
            book, _ = Book.objects.get_or_create(
                isbn=request.GET['isbn']
            )
            record, created = BookRecord.objects.get_or_create(
                user=request.user,
                book=book
            )
            if created is False:
                form_data = {
                    'title': record.title,
                    'isbn': record.book.isbn,
                    'author': record.author,
                    'publisher': record.publisher,
                    'check1': record.check1,
                    'check2': record.check2,
                    'check3': record.check3,
                    'link': record.book.url,
                    'imageLink': record.book.imageUrl
                }
                if record.rating is not None:
                    form_data['star1'] = record.rating
                if record.memo is not None:
                    form_data['memo'] = record.memo
                if record.dateEnd is not None:
                    form_data['dateEnd'] = record.dateEnd
                if record.dateStart is not None:
                    form_data['dateStart'] = record.dateStart
                if record.tags.all() is not None:
                    tags = ' '.join([tag.name for tag in record.tags.all()])
                    form_data['tags'] = tags
                form = BookSaveForm(form_data)
        template = get_template('edit_book.html')
        variables = {
            'user': current_user,
            'form': form,
            'record': record,
            'tags': tags,
        }
        output = template.render(variables)
        return HttpResponse(output)
    return HttpResponseRedirect('/')


#Check if user has the record of this book
def check_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        form = BookSaveForm(request.GET)
        if form.is_valid():
            book, _ = Book.objects.get_or_create(
                isbn=form.cleaned_data['isbn']
            )
            record, created = BookRecord.objects.get_or_create(
                user=request.user,
                book=book
            )
            if created:
                return HttpResponse(json.dumps({'checkisbn': False}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'checkisbn': True}), content_type="application/json")
        else:
            return HttpResponse(form.errors.as_json)
    return HttpResponse(json.dumps({'checkisbn': False}), content_type="application/json")


# List of finished years in json
def finish_year_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        records = BookRecord.objects.filter(
            user=request.user,
        )
        finish_years = list(set([record.dateEnd.year for record in records if record.dateEnd is not None]))
        return HttpResponse(json.dumps({'finish_year': finish_years}), content_type="application/json")
    return HttpResponse(json.dumps({'finish_year': []}), content_type="application/json")


# List of all books finished in that years
def list_of_year_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        template = get_template('list_page.html')
        year = request.GET.get('year', None)
        if year is not None:
            records = BookRecord.objects.filter(
                user=request.user,
                dateEnd__year=year
            )
            variables = {
                'ratings': [2, 4, 6, 8, 10],
                'year': year,
                'records': records,
                'user': current_user,
                'list_title': "Books finished on the year " + year,
            }
            output = template.render(variables)
            return HttpResponse(output)
        else:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


# List of all books with that tag
def list_of_tag_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        template = get_template('list_page.html')
        tag = request.GET.get('tag', None)
        if tag is not None and tag != '':
            records = BookRecord.objects.filter(
                user=request.user,
                tags__name=tag
            )
            variables = {
                'ratings': [2, 4, 6, 8, 10],
                'tag': tag,
                'records': records,
                'user': current_user,
                'list_title': "Books tagged with " + tag,
            }
            output = template.render(variables)
            return HttpResponse(output)
        else:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


# List of all books with that author
def list_of_author_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        template = get_template('list_page.html')
        author = request.GET.get('author', None)
        if author is not None and author != '':
            records = BookRecord.objects.filter(
                user=request.user,
                author__icontains=author
            )
            variables = {
                'ratings': [2, 4, 6, 8, 10],
                'author': author,
                'records': records,
                'user': current_user,
                'list_title': 'Books written by ' + author,
            }
            output = template.render(variables)
            return HttpResponse(output)
        else:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


# List of all books with flag1, flag2, flag3
def list_by_flags_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        template = get_template('list_page.html')
        flag1 = request.GET.get('flag1', None)
        flag2 = request.GET.get('flag2', None)
        flag3 = request.GET.get('flag3', None)
        bool1 = True if flag1 == 'true' else False
        bool2 = True if flag2 == 'true' else False
        bool3 = True if flag3 == 'true' else False
        if not bool1 and not bool2 and not bool3:
            return HttpResponseRedirect('/')
        q_objects = Q(user=request.user)
        if bool1:
            q_objects &= Q(check1=True)
        if bool2:
            q_objects &= Q(check2=True)
        if bool3:
            q_objects &= Q(check3=True)
        records = BookRecord.objects.filter(q_objects)
        variables = {
            'ratings': [2, 4, 6, 8, 10],
            'records': records,
            'user': current_user,
            'list_title': "Books with flags",
        }
        output = template.render(variables)
        return HttpResponse(output)
    return HttpResponseRedirect('/')


def delete_page(request):
    current_user = request.user
    if 'user' in request.session:
        current_user = request.session['user']
    if not current_user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        form = BookSaveForm(request.GET)
        if form.is_valid():
            try:
                book = Book.objects.get(
                    isbn=form.cleaned_data['isbn']
                )
                record = BookRecord.objects.get(
                    user=request.user,
                    book=book
                )
                record.delete()
            except ObjectDoesNotExist:
                pass
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


def user_page(_, username):
    try:
        user = User.objects.get(username=username)
    except Exception:
        raise Http404(f'Cannot find user {username}')
    records = user.bookrecord_set.all()
    template = get_template('list_page.html')
    variables = {
        'ratings': [2, 4, 6, 8, 10],
        'user': user,
        'records': records,
        'list_title': 'Books edited by ' + username
    }
    output = template.render(variables)
    return HttpResponse(output)
