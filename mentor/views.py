import json
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"  # Fast & free-tier friendly


@csrf_exempt
def ask_ai(request):
    if request.method == 'POST':
        try:
            # --- Validate API Key ---
            api_key = os.environ.get("GROQ_API_KEY", "")
            if not api_key:
                return JsonResponse(
                    {'answer': "⚠️ GROQ_API_KEY is not configured on the server."},
                    status=500,
                )

            data = json.loads(request.body)
            user_question = data.get('question', '')
            selected_lang = data.get('lang', 'en-IN')

            # STRICT PROMPT: Forces AI to match the user's selected language
            system_prompt = (
                f"You are a professional mentor. The user is speaking in {selected_lang}. "
                f"Instructions: Answer the question ONLY in {selected_lang}. Do not use any other language. "
                f"Keep your answer under 40 words."
            )

            # --- Call Groq Cloud API (OpenAI-compatible) ---
            response = requests.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150,
                },
                timeout=30,
            )

            if response.status_code == 200:
                ai_answer = (
                    response.json()
                    .get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "No response from AI.")
                )
                return JsonResponse({'answer': ai_answer})
            else:
                error_detail = response.json().get("error", {}).get("message", "Unknown error")
                return JsonResponse(
                    {'answer': f"⚠️ AI service error: {error_detail}"},
                    status=500,
                )

        except requests.exceptions.Timeout:
            return JsonResponse(
                {'answer': "⚠️ AI service timed out. Please try again."},
                status=504,
            )
        except Exception as e:
            return JsonResponse(
                {'answer': f"⚠️ Server error: {str(e)}"},
                status=500,
            )

    return JsonResponse({'error': 'Invalid Method'}, status=405)