import json
import os
from django.http import JsonResponse
from django.conf import settings
from groq import Groq

# Initialize the Groq client
# This looks for 'GROQ_API_KEY' in your settings.py
client = Groq(api_key=settings.GROQ_API_KEY)

def ask_ai(request):
    """
    Handles the POST request from the frontend, sends the question to Groq,
    and returns the AI's response as JSON.
    """
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_question = data.get("question", "")
            user_lang = data.get("lang", "en-IN")

            if not user_question:
                return JsonResponse({"answer": "Please ask a question!"}, status=400)

            # Send the request to Groq Cloud (Llama 3 model)
            completion = client.chat.completions.create(
                model="llama3-8b-8192",  # High-speed model perfect for hackathons
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are 'Bolo Seekho', a supportive AI mentor. Provide clear and helpful answers in {user_lang}."
                    },
                    {
                        "role": "user", 
                        "content": user_question
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
            )

            # Extract the text answer
            answer = completion.choices[0].message.content

            return JsonResponse({"answer": answer})

        except Exception as e:
            # If something goes wrong (like a bad API key or no internet)
            print(f"Error: {str(e)}")
            return JsonResponse({"answer": f"⚠️ Mentor Error: {str(e)}"}, status=500)

    # If someone tries to visit the URL via browser (GET request)
    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)