import os
import re
from django.shortcuts import render
from groq import Groq
from decouple import config

GROQ_API_KEY = config("GROQ_API_KEY")



def ai_consultant_view(request):
    ai_response = None
    
    if request.method == "POST":
        try:
            # Initialize Client using the API Key from your environment
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

            # Capture form data from the user
            car = request.POST.get('car_model')
            budget = request.POST.get('budget')

            # Request formal response from Llama 3
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a professional automotive consultant for CarbonCraft Studio. "
                            "Format your response formally and professionally. "
                            "Use clear, capitalized headings. Use bullet points for specific modifications. "
                            "Provide a 'Final Summary' at the end. Do not use bold markdown symbols like **. "
                            "Focus strictly on prices in PKR and part availability in the Lahore market."
                        )
                    },
                    {
                        "role": "user", 
                        "content": f"Provide a formal modification protocol for: {car}. Allocated Budget: {budget} PKR."
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            # Extract and format the content in a classy HUD style
            raw_content = chat_completion.choices[0].message.content
            # Convert **Heading** to HUD Header with accent bar
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<div class="mt-8 mb-4 flex items-center gap-3 border-b border-blue-500/10 pb-2"><div class="w-1 h-4 bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div><strong class="text-white text-[11px] font-black uppercase tracking-[0.3em] font-sans">\1</strong></div>', raw_content)
            # Convert bullets to technical markers and handle line breaks
            ai_response = formatted.replace('* ', '<span class="text-blue-500 mr-2">▶</span> ').replace('\n', '<br>')

        except Exception as e:
            # Capture errors like missing API keys or connection issues
            ai_response = f"System Error: {str(e)}"

    return render(request, 'ai_consultant.html', {'result': ai_response})


def ai_consultant_view2(request):
    ai_response = None
    
    if request.method == "POST":
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            
            # Capture New Inputs
            budget = request.POST.get('budget')
            use_type = request.POST.get('use_type')

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a Pakistani Car Market Expert. Format your response formally. "
                            "Provide two distinct sections: 1) NEW CAR OPTIONS (Zero Meter) "
                            "and 2) USED CAR OPTIONS (Market Favorites). "
                            "Consider resale value, maintenance costs in Lahore/Karachi, and fuel average. "
                            "Do not use bold symbols (**). Use clear headings."
                        )
                    },
                    {
                        "role": "user", 
                        "content": f"I have a budget of {budget} PKR. I need a car for {use_type}. "
                                   f"Suggest the best new and used options currently available in Pakistan."
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            raw_content = chat_completion.choices[0].message.content
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<div class="mt-8 mb-4 flex items-center gap-3 border-b border-blue-500/10 pb-2"><div class="w-1 h-4 bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div><strong class="text-white text-[11px] font-black uppercase tracking-[0.3em] font-sans">\1</strong></div>', raw_content)
            ai_response = formatted.replace('* ', '<span class="text-blue-500 mr-2">▶</span> ').replace('\n', '<br>')

        except Exception as e:
            ai_response = f"System Error: {str(e)}"

    return render(request, 'ai_consultant2.html', {'result': ai_response})


def car_specs_view(request):
    specs_result = None
    
    if request.method == "POST":
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            car_name = request.POST.get('car_name')

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a technical automotive data specialist for the Pakistani market. "
                            "Analyze the user's input. If the user asks for a specific technical detail "
                            "(e.g., 'fuel average', 'engine CC', 'torque'), provide that specific information prominently. "
                            "If the user only provides a car name, return a formal technical specification sheet. "
                            "Always include the relevant Pakistani market variant details. "
                            "Use clear headers for sections. Do not use bold markdown symbols (**)."
                        )
                    },
                    {
                        "role": "user", 
                        "content": f"Technical Data Request: {car_name}. Provide the most accurate and specific details available for Pakistan."
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            raw_content = chat_completion.choices[0].message.content
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<div class="mt-8 mb-4 flex items-center gap-3 border-b border-blue-500/10 pb-2"><div class="w-1 h-4 bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div><strong class="text-white text-[11px] font-black uppercase tracking-[0.3em] font-sans">\1</strong></div>', raw_content)
            specs_result = formatted.replace('* ', '<span class="text-blue-500 mr-2">▶</span> ').replace('\n', '<br>')
        except Exception as e:
            specs_result = f"Error fetching specs: {str(e)}"

def car_comparison_view(request):
    ai_response = None
    if request.method == "POST":
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            car1 = request.POST.get('car1')
            car2 = request.POST.get('car2')

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a professional automotive comparison expert for CarbonCraft Studio. "
                            "Compare the two provided vehicles specifically for the Pakistani market. "
                            "Return the comparison in a clean, professional HTML table. "
                            "Table Columns: Metric, " + car1 + ", " + car2 + ". "
                            "Metrics to include: Engine/CC, Horsepower, Fuel Average, Resale Value, Parts Availability. "
                            "Do not use any asterisks (*) or bold symbols (**) in the entire response. "
                            "After the table, provide a short 'VERDICT' section in a separate paragraph."
                        )
                    },
                    {
                        "role": "user", 
                        "content": f"Compare these two vehicles in Pakistan: {car1} vs {car2}."
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            raw_content = chat_completion.choices[0].message.content
            
            # Clean styling for the table to match HUD theme
            styled_table = raw_content.replace('<table>', '<table class="w-full border-collapse border border-blue-500/20 text-xs my-6">')
            styled_table = styled_table.replace('<th>', '<th class="border border-blue-500/20 p-3 bg-blue-500/10 text-blue-400 uppercase tracking-widest text-left">')
            styled_table = styled_table.replace('<td>', '<td class="border border-blue-500/20 p-3 text-gray-300">')
            
            # Remove any stray asterisks and strip whitespace
            ai_response = styled_table.replace('*', '').strip()

        except Exception as e:
            ai_response = f"System Error: {str(e)}"

    return render(request, 'ai_compare.html', {'result': ai_response})


def Ai_agents(request):
    return render(request, 'AI_AGENTS.html')




# Load variables from .env


def diagnose(request):
    if request.method == "POST":
        car_model = request.POST.get('car_model')
        problem = request.POST.get('problem')
        
        # Pull key from .env
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        system_msg = (
            "You are the Carbon Craft AI Diagnostic Sentinel. Provide a professional mechanical analysis. "
            "Format your response with clear headings using **bold symbols**. "
            "Use bullet points for lists. Provide a professional summary."
        )
        
        user_msg = f"Vehicle: {car_model}. Reported Symptoms: {problem}."

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.5, # Lower temperature for more factual diagnostics
            )
            
            raw_content = completion.choices[0].message.content
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<div class="mt-8 mb-4 flex items-center gap-3 border-b border-blue-500/10 pb-2"><div class="w-1 h-4 bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div><strong class="text-white text-[11px] font-black uppercase tracking-[0.3em] font-sans">\1</strong></div>', raw_content)
            result = formatted.replace('* ', '<span class="text-blue-500 mr-2">▶</span> ').replace('\n', '<br>')
            
            return render(request, 'ai_dignose.html', {
                'diagnosis': result,
                'car_model': car_model
            })
            
        except Exception as e:
            return render(request, 'ai_dignose.html', {
                'error': "Neural link interrupted. Verify API credentials."
            })

    return render(request, 'ai_dignose.html')