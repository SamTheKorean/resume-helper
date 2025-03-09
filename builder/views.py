from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Resume
from .forms import InputForm
import openai
from django.conf import settings

from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)
def home(request):
    suggested_sentence = ''
    input_sentence = '' 

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input_sentence = form.cleaned_data['input_sentence']  
    else:
        form = InputForm()

    if input_sentence:  # Ensure it's not empty before calling OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Transform the following sentence into a format suitable for an ATS (Applicant Tracking System), emphasizing quantifiable achievements and starting with an active verb. The sentence to convert is: {input_sentence}. Ensure that it is only one sentence."}
            ],
            temperature=0.8
        )

        suggested_sentence = f" You can put: {response.choices[0].message.content} for your resume "

    return render(request, 'home.html', {'form': form, 'suggested_sentence': suggested_sentence})

    try:
        # Check if the user has entered a message
        if request.method == 'POST':
            user_message = request.POST.get('message', '')

            # Make sure there is an actual input
            if user_message:
                # Call OpenAI API to generate a response
                completion = openai.chat.completions.create(
                    model="gpt-3.5-turbo",  # You can change this to gpt-4 for better results
                    messages=[
                        {"role": "user",  "content": f"GivenProvide me with some warm, encouraging advice for: {user_message}"}
                    ]
                )
                
                # Extract the message from the response
                response_content = completion['choices'][0]['message']['content'].strip()

                # Render the positive, warm response in a Django template
                return render(request, 'builder/generate_resume.html', {'response_content': response_content})
            else:
                return render(request, 'builder/generate_resume.html', {'error': "Please enter a message."})
        else:
            return render(request, 'builder/generate_resume.html')

    except Exception as e:
        # If there's an error, show the error message in the template
        return render(request, 'builder/generate_resume.html', {'error': f"Error: {str(e)}"})