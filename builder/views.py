from django.shortcuts import render
from django.http import JsonResponse
from .forms import InputForm
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def home(request):
    suggested_sentence = ''
    error_message = None

    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            input_sentence = form.cleaned_data['input_sentence']

            try:
                validation_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", 
                         "content": f"Is this sentence related to experience? {input_sentence} Please answer 'Yes' or 'No'."}
                    ],
                    temperature=0.7
                )

                validation_answer = validation_response.choices[0].message.content.strip().lower()

                if validation_answer == 'yes':
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": f"Convert the following sentence into an ATS-optimized bullet point, ensuring it starts with an active verb and highlights quantifiable achievements. Sentence to convert: {input_sentence}"}
                        ],
                        temperature=0.8
                    )

                    suggested_sentence = response.choices[0].message.content

                    # ✅ Handle AJAX request (return JSON response)
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse({"suggested_sentence": suggested_sentence})

                else:
                    error_message = "Please provide a sentence related to your professional experience."

            except Exception as e:
                error_message = f"Error processing input: {str(e)}"

    else:
        form = InputForm()

    return render(request, 'home.html', {
        'form': form,
        'suggested_sentence': suggested_sentence,
        'error_message': error_message
    })
