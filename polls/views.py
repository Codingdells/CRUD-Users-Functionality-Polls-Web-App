from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from . models import Question, Choice
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView,ListView
from . forms import *
from django.forms import formset_factory
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction

# @login_required
# def index(request):
#     latest_question_list = Question.objects.all().order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


class PollsListView(ListView, LoginRequiredMixin):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "question"
    ordering = ['-pub_date']
    paginate_by = 5



# class UserPollsListView(ListView, LoginRequiredMixin):
#     model = Question
#     template_name = "polls/index.html"
#     context_object_name = "question"
#     ordering = ['-pub_date']
#     paginate_by = 5
    
#     def get_queryset(self):
#         user = get_object_or_404(User, pk=self.kwargs.get("id"))
#         return Question.objects.filter(author=user).order_by("-pub_date")
    
    
def user_detail(request, id):
    user = get_object_or_404(User, pk=id)
    question = Question.objects.filter(author=user).order_by("-pub_date")[:5]
    context = {"question": question}
    return render(request, "polls/index.html", context) 


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'polls/question_create.html'
    form_class = QuestionForm
    success_url = None
    
    def get_context_data(self, **kwargs):
        data = super(QuestionCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['choices'] = ChoiceFormSet(self.request.POST)
        else:
            data['choices'] = ChoiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['choices']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if choices.is_valid():
                choices.instance = self.object
                choices.save()
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('list')


class QuestionUpdateView(UpdateView,  LoginRequiredMixin, UserPassesTestMixin):
    model = Question
    template_name = 'polls/question_create.html'
    form_class = QuestionForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(QuestionUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['choices'] = ChoiceFormSetUpdate(
                self.request.POST, instance=self.object)
        else:
            data['choices'] = ChoiceFormSetUpdate(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['choices']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if choices.is_valid():
                choices.instance = self.object
                choices.save()
        return super(QuestionUpdateView, self).form_valid(form)
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False
        
    def get_success_url(self):
        return reverse('list')


class QuestionDeleteView(DeleteView, UserPassesTestMixin, LoginRequiredMixin):
    model = Question
    success_url = "/"
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False


def QuestionDetailView(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        formset = Choice.objects.filter(question_id=question_id)
        print(formset)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/question_detail.html', { 'question': question, "formset": formset})


# class QuestionDetailView(DetailView):
#     model = Question
    
#     def get_context_data(self, **kwargs):
#         data = super(QuestionDetailView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['choices'] = ChoiceFormSetUpdate(
#                 self.request.POST, instance=self.object)
#         else:
#             data['choices'] = ChoiceFormSetUpdate(instance=self.object)
#         return data



def vote(request, id):
    print(request.POST['choice'])
    question = Question.objects.get(pk=id)
    try:
        choice_set = Choice.objects.filter(question_id=id)
        selected_choice = choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        
        # Redisplay the question voting form.
        return render(request, 'polls/question_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('list'))
