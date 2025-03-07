from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Resume
from .forms import ResumeForm
import openai
from django.conf import settings

from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)
def home(request):
    return HttpResponse("hi yuri")

def resume_input(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save()
            return redirect('generate_resume', pk=resume.pk)
    else:
        form = ResumeForm()
    return render(request, 'builder/resume_input.html', {'form': form})


def generate_resume(request):
    try:
        # Example user input message
        user_message = "How do I output all files in a directory using Python?"
        
        # Call OpenAI's chat model (gpt-3.5-turbo or gpt-4)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-",  # You can replace with gpt-3.5-turbo or gpt-4o as needed
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        # Get the response content from the API
        response_content = completion['choices'][0]['message']['content'].strip()

        # Render the response content in a Django template
        return render(request, 'builder/generate_resume.html', {'response_content': response_content})

    except Exception as e:
        # Handle any potential errors from the OpenAI API
        return render(request, 'builder/generate_resume.html', {'error': f"Error: {str(e)}"})
   