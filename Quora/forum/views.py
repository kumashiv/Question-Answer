from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse, JsonResponse
from .models import Question, Comment, Like, UserProfile

from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse, reverse_lazy
from .forms import QuestionForm

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView
import json

from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


# Search functionality
class QuestionListView(ListView):
    model = Question
    # template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs_json"] = json.dumps(list(Question.objects.values()),cls=DjangoJSONEncoder)

        return context


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs ):
        profile = UserProfile.objects.get(pk=pk)
        p_user = profile.user

        followers = profile.followers.all()
        print(followers)

        num_of_followers = len(followers)

        if num_of_followers == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        myQuestions = Question.objects.filter(owner = p_user)
        myComments = Comment.objects.filter(owner = p_user)

        context = {'p_user': p_user, 'profile': profile , 'myQuestions' : myQuestions, 'myComments': myComments, 'num_of_followers' : num_of_followers, 'is_following' : is_following, 'followers': followers}

        return render(request, 'forum/profile.html', context)


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        print(profile.pk)

        return redirect(reverse('forum:profile', kwargs={'pk':profile.pk}))


class RemoveFollower(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        print(profile.pk)

        return redirect(reverse('forum:profile', kwargs={'pk':profile.pk}))




def index(request):
    all_questions = Question.objects.all().order_by('-pub_date')

    # data_json = json.dumps(list(Question.objects.values()),cls=DjangoJSONEncoder)
    # context = {'all_questions' : all_questions, 'data_json' : data_json}

    context = {'all_questions' : all_questions}

    return render(request, 'forum/index.html', context)

def account(request):
    all_questions = Question.objects.all()

    user = request.user
    myQuestions = Question.objects.filter(owner = user)
    # data_json = json.dumps(list(Question.objects.values()),cls=DjangoJSONEncoder)

    myComments = Comment.objects.filter(owner = user)

    context = {'all_questions' : all_questions, 'myQuestions' : myQuestions, 'myComments' : myComments}
    return render(request, 'forum/myaccount.html', context)


def QuestionDetail(request, question_id):
    q = Question.objects.get(pk=question_id)
    # Comment related
    c = Comment.objects.filter(question = q)

    user = request.user
    like = Like.objects.filter(question = q, owner = user).count()

    print(like);

    context = {
        'question' : q,
        'comment': c,
        'like': like
    }

    return render(request, 'forum/question_detail.html', context)


# def save_comment(request):
#
#     if request.method == 'POST':
#         comment = request.POST['comment']
#
#         questionid = request.POST['questionid']
#         question = Question.objects.get(pk=questionid)
#
#         user = request.user
#
#         Comment.objects.create(
#             comment_text = comment,
#             owner = user,
#             question = question
#         )
#         return JsonResponse({'bool':True})


def save_comment(request, question_id):
    if request.method == 'POST':
        comment = request.POST['comment']


        question = Question.objects.get(pk=question_id)
        user = request.user

        Comment.objects.create(
            comment_text = comment,
            owner = user,
            question = question
        )
        return JsonResponse({'bool':True})

def save_like(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(pk=question_id)
        user = request.user

        check = Like.objects.filter(question = question, owner = user).count()
        # print(check)

        check2 = Like.objects.filter(question = question, owner = user)
        # print(check2)


        if check > 0:
            check2.delete()
            return JsonResponse({'bool':False})

        else:
            Like.objects.create(
                owner = user,
                question = question
            )
            return JsonResponse({'bool':True})


class QuestionCreate(CreateView, LoginRequiredMixin):
    model = Question
    fields = ['question_text']
    success_url = reverse_lazy('forum:index')

    def form_valid(self, form):
        # object = form.save(commit=False)
        # object.owner = self.request.user
        # object.save()

        form.instance.owner = self.request.user

        # return super(QuestionCreate, self).form_valid(form)
        return super().form_valid(form)


class QuestionUpdate(LoginRequiredMixin, View):
    model = Question

    # fields = ['question_text']
    template = 'forum/question_form.html'
    success_url = reverse_lazy('forum:index')

    # def get_queryset(self, request, question_id):
    #     print("In query")
    #     return Question.objects.filter(owner=self.request.user)

    def get(self, request, question_id):
        print("In Get")
        q = get_object_or_404(self.model, pk=question_id)

        if q.owner == self.request.user:
            form = QuestionForm(instance=q)
            ctx = {'form': form}
            return render(request, self.template, ctx)
        else:
            # raise PermissionDenied
            return redirect(reverse_lazy('users:login'))


    def post(self, request, question_id):
        q = get_object_or_404(self.model, pk=question_id)
        form = QuestionForm(request.POST, instance=q)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)


class QuestionDelete(LoginRequiredMixin, View):
    model = Question

    # fields = ['question_text']
    template = 'forum/question_confirm_delete.html'
    success_url = reverse_lazy('forum:index')

    def get(self, request, question_id):
        q = get_object_or_404(self.model, pk=question_id)
        print(q)
        # form = QuestionForm(instance=q)
        # ctx = {'form': form}
        if q.owner == self.request.user:
            form = QuestionForm(instance=q)
            ctx = {'q': q}
            return render(request, self.template, ctx)
        else:
            # raise PermissionDenied
            return redirect(reverse_lazy('users:login'))

    def post(self, request, question_id):
        q = get_object_or_404(self.model, pk=question_id)
        q.delete()
        return redirect(self.success_url)
