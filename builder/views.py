from django.shortcuts import render
from .forms import InputForm
from django.conf import settings

from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def home(request):
    suggested_sentence = ''
    input_sentence = '' 
    error_message = None

    
    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            input_sentence = form.cleaned_data['input_sentence']
            
            # Use AI to validate if the input is related to experience
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
                    # Proceed with processing the valid input
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": f"Convert the following sentence into an ATS-optimized bullet point, ensuring it starts with an active verb and highlights quantifiable achievements. If multiple sentences are given, rewrite them concisely, avoiding redundancy while maintaining clarity. The output should be in a single sentence per idea. Example: Optimized the Django backend and Flutter frontend, leading to a 50% decrease in server response time and a 30% enhancement in overall application performance. Sentence to convert: {input_sentence}"}
                        ],
                        temperature=0.8
                    )

                    suggested_sentence = f"{response.choices[0].message.content}"

                else:
                    print("Invalid input: Not related to experience.")
                    error_message = "Please provide a sentence related to your professional experience."

            except Exception as e:
                print("Error during processing:", str(e))
                error_message = f"Error processing input: {str(e)}"

    else:
        form = InputForm()

    print("Rendering response with form:", form)
    return render(request, 'home.html', {
        'form': form,
        'suggested_sentence': suggested_sentence,
        'error_message': error_message
    })
