# exams/views.py
from django.shortcuts import render, redirect
from .models import Exam
from .forms import ExamForm

def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = ExamForm()
    
    return render(request, 'exams/create_exam.html', {'form': form})


# exams/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question
from .forms import AnswerForm
from .utils import calculate_exam_score

def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Question.objects.filter(exam=exam)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, questions=questions)
        if form.is_valid():
            # Calculate the score based on user's answers
            score = calculate_exam_score(exam, form.cleaned_data)
            
            # Create or update the exam result for the user
            exam_result, created = ExamResult.objects.get_or_create(
                user=request.user,
                exam=exam,
            )
            exam_result.score = score
            exam_result.save()
            
            return redirect('exam_results')
    else:
        form = AnswerForm(questions=questions)
    
    return render(request, 'exams/exam_detail.html', {'exam': exam, 'form': form})

# exams/views.py
from django.shortcuts import render
from .models import Exam, ExamResult

def exam_results(request):
    # Fetch all exam results for the logged-in user
    exam_results = ExamResult.objects.filter(user=request.user)
    
    return render(request, 'exams/exam_results.html', {'exam_results': exam_results})

# exams/views.py
from django.shortcuts import render
from .models import Exam, ExamResult

def exam_results(request):
    # Fetch all exam results for the logged-in user
    exam_results = ExamResult.objects.filter(user=request.user)
    
    return render(request, 'exams/exam_results.html', {'exam_results': exam_results})
