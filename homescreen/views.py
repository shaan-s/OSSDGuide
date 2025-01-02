from django.template import loader
from django.http import HttpResponse
from .models import Courses, Reviews
from statistics import mean
from .forms import ReviewForm
from time import time
from django.http import HttpResponseRedirect
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def percentformat(value, arg):
    return (float(value) - float(arg))*100

@register.filter
def s(value):
    if value > 1:
        return "s"
    else: return ""

@register.filter
def format(str):
    return str.title().replace("_"," ")

@register.filter
def get_ratings(course):
    return Reviews.objects.filter(course_code = course.course_code).count()

@register.filter
def get_score(course):
    course_reviews_query = Reviews.objects.filter(course_code = course)
    if course_reviews_query.count() > 0:
        return "{:.1f}".format(mean(list(course_reviews_query.values_list('overall_rating',flat=True))))
    else: return None


def explore(request):
    courseslist = Courses.objects.all()

    category_filter = request.GET.getlist('category')
    grade_filter = request.GET.getlist('grade')
    level_filter = request.GET.getlist('level')
    search = request.GET.get('search')
    sort_by = request.GET.get('sortby')
    rev = request.GET.get('rev')

    grade_checked_list = [0,0,0,0]
    grade_checked_all = False

    level_checked_list = {"De-streamed":0,"Applied":0,"Academic":0,"University":0,"University/College":0,"College":0,"Workplace":0,"Open":0}
    level_to_char = {"De-streamed":"W","Applied":"P","Academic":"D","University":"U","University/College":"M","College":"C","Workplace":"E","Open":"O"}
    level_checked_all = False

    if category_filter:
        category_filter = category_filter[0]

        if category_filter != "(Any)":
            courseslist = courseslist.filter(category__in=category_filter.split(","))

    if grade_filter:
        grade_filter = "".join(grade_filter) #list to str
        courseslist = courseslist.filter(course_code__regex=r'^...[' + grade_filter  + ']+[A-Za-z]$')

        for grade in range(1,5):
            if str(grade) in grade_filter:
                grade_checked_list[grade-1] = 1

    if level_filter:
        level_filter = "".join(level_filter) #list to str

        courseslist = courseslist.filter(course_code__regex=r'^....[' + "".join(level_filter) + ']+$')
        for level in level_checked_list:
            if level_to_char[level] in level_filter:
                level_checked_list[level] = 1
    if search:
        search = "".join([substr for substr in search if (substr.isalnum() or substr in " ()'’:,")]) #keep only alphanum+space+punc
        courseslist = courseslist.filter(course_name__icontains=search) | courseslist.filter(course_code__icontains=search)
    if search == None:
        search = "";

    if (grade_checked_list == [1,1,1,1]) or (grade_checked_list == [0,0,0,0]):
        grade_checked_list = [0,0,0,0]
        grade_checked_all = True

    level_values = list(level_checked_list.values())
    if level_values.count(level_values[0]) == len(level_values): #if all values equal; ie all are checked
        level_checked_list = {"De-streamed":0,"Applied":0,"Academic":0,"University":0,"University/College":0,"College":0,"Workplace":0,"Open":0}
        level_checked_all = True

    if sort_by in ["course_code","course_name"]:
        courseslist = list(courseslist.order_by(sort_by))
    elif not sort_by:
        courseslist = list(courseslist.order_by("course_code"))
        sort_by = "course_code"

    if sort_by == "ratings":
        courseslist = list(courseslist)
        courseslist.sort(key=get_ratings,reverse=True)

    if rev == "1":
        courseslist.reverse()

    #create list of unique categories
    categories = [category[0] for category in set(Courses.objects.values_list("category"))]
    categories.sort()
    categories.insert(0, "(Any)")

    template = loader.get_template('explore.html')
    context = {
    'courseslist': courseslist,
    'gradelist': grade_checked_list,
    'grade_checked_all': grade_checked_all,
    'level_checked_list':level_checked_list,
    'level_checked_all':level_checked_all,
    'level_to_char':level_to_char,
    'categories':categories,
    'category_filter':category_filter,
    'search':search,
    'rev':rev,
    'sortby':sort_by,
    'params':["course_code","course_name","ratings"],
    }


    return HttpResponse(template.render(context, request))

def course_page(request, code):
    curr_course = Courses.objects.filter(course_code = code).first()
    prereq_list = curr_course.prereq.split(",")

    leads_to = Courses.objects.filter(prereq__contains = code)
    leads_to_codes = [course.course_code for course in leads_to]

    course_reviews_query = Reviews.objects.filter(course_code = code)
    course_reviews_query = course_reviews_query.filter(moderated = True)

    course_reviews = list(course_reviews_query)
    for review in course_reviews:
        review.user_school_board = review.get_user_school_board_display()

    num_ratings = len(course_reviews)
    mean_dict = {}
    if num_ratings > 0:
        mean_dict["overall_mean"] = "{:.1f}".format(mean(list(course_reviews_query.values_list('overall_rating',flat=True))))
        mean_dict["interesting_mean"] = "{:.1f}".format(mean(list(course_reviews_query.values_list('interesting_rating',flat=True))))
        mean_dict["easy_mean"] = "{:.1f}".format(mean(list(course_reviews_query.values_list('easy_rating',flat=True))))

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                get_user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
                if get_user_ip:
                    get_user_ip = ip_address.split(',')[0]
                else:
                    get_user_ip = request.META.get('REMOTE_ADDR')
            except:
                get_user_ip = "<IP Query Failed!>"

            Reviews.objects.create(
            course_code = curr_course.course_code,
            online = form.cleaned_data["online"],
            review_text = form.cleaned_data["review_text"],
            interesting_rating = form.cleaned_data["interesting_rating"],
            easy_rating = form.cleaned_data["easy_rating"],
            overall_rating = form.cleaned_data["overall_rating"],
            user_school_board = form.cleaned_data["user_school_board"],
            review_date = time(),
            moderated = False, ##CHANGE TO FALSE IF AUTO-MOD OFF
            user_ip = get_user_ip,
            )
            return HttpResponseRedirect(request.path_info)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewForm()

    template = loader.get_template('course_page.html')

    context = {
    'curr_course': curr_course,
    'grade_val': curr_course.grade(),
    'url_grade_val': curr_course.grade()-8,
    'level_val': curr_course.level(),
    'url_level_val': curr_course.course_code[4],
    'prereq_list': prereq_list,
    'last_prereq': prereq_list[-1],
    'len_first_prereq': len(prereq_list[0]),
    'leads_to' : leads_to_codes,

    'course_reviews': course_reviews,
    'num_ratings' : num_ratings,

    'form': form,
    }

    if leads_to:
        context['last_leads_to'] =  leads_to_codes[-1]

    context.update(mean_dict)

    return HttpResponse(template.render(context, request))

def contact(request):

    context = {}
    template = loader.get_template('contact.html')
    return HttpResponse(template.render(context, request))

def home(request):
    context = {
    'course_len' : len(Courses.objects.all()),
    'ratings_len' : len(Reviews.objects.all()),
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))
