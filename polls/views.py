from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# from django.django.http.response import HttpResponseRedirect
from .models import Question, Choice, Report
from django import forms


# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
class ReportView(generic.DetailView):
    model = Question
    template_name = "polls/report.html"

class SubmitView(generic.DetailView):
    model = Question
    template_name = "polls/submitted.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs['pk']
        context['report_list'] = Report.objects.filter(question_id=question_id)
        return context

    def get_queryset(self):
        return Report.objects.all()
def submitReport(request, question_id):
    #template_name = "polls/report.html"
    #return HttpResponseRedirect(reverse("polls:submitted", args=(question_id,)))

    questionId = request.POST.get("question_id")

    #Get values from Post data
    question = get_object_or_404(Question, pk=question_id)
    name = request.POST.get("name")
    input = request.POST.get("input")
    if not name or not input:
        return render(request, "polls/report.html", {"question": question, "error_message": "Please fill out all fields"})
        #return HttpResponseRedirect(reverse("polls:submitted", args=(question_id,title)))

    else:
        report = Report.objects.create(question=question, name=name, input=input)
        report.save()
        return HttpResponseRedirect(reverse("polls:submitted", args=(question_id,)))



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question": question,
                                                     "error_message": "You didn't select a choice.",
                                                     },
                      )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
