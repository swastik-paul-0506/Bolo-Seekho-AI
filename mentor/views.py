from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_question = data.get('question')
            user_lang_code = data.get('lang', 'en-IN')

            # Language Mapping
            lang_map = {
                "hi-IN": "Hindi",
                "bn-IN": "Bengali",
                "ta-IN": "Tamil",
                "te-IN": "Telugu",
                "mr-IN": "Marathi",
                "gu-IN": "Gujarati",
                "kn-IN": "Kannada",
                "ml-IN": "Malayalam",
                "pa-IN": "Punjabi",
                "en-IN": "English"
            }
            
            target_lang = lang_map.get(user_lang_code, "English")

            # Force the AI to use the correct language
            system_prompt = f"You are a helpful mentor. The user is asking in {target_lang}. You MUST reply ONLY in {target_lang} script. Do not use English."

            # Sending to Ollama
            response = requests.post('http://localhost:11434/api/generate', 
                json={
                    "model": "llama3.2", 
                    "prompt": f"{system_prompt}\n\nUser Question: {user_question}",
                    "stream": False
                }
            )
            
            result = response.json()
            ai_response = result.get('response', 'Sorry, I could not process that.')

            return JsonResponse({'answer': ai_response})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=400)