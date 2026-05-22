import os
import re
from django.shortcuts import render
from groq import Groq



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
                            "Focus strictly on prices in PKR and part availability in the Lahore market. "
                            "CRITICAL RULE: If the user's input contains unusual symbols, gibberish, or is not related to cars/automotive topics, you MUST reject the prompt and reply exactly with: 'Error: I am a CarbonCraft intelligence. Please ask me about cars.' Do not provide any other information in this case."
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
            
            # Capture Inputs
            budget = request.POST.get('budget')
            use_type = request.POST.get('use_type')

            # Updated system prompt using Markdown requirements for layout uniformity
            system_msg = (
                "You are CarbonCraft's elite Pakistani Car Market Expert and Navigator. "
                "Given a budget (in PKR) and a primary use case, provide a highly strategic car purchase consultation.\n\n"
                
                "CRITICAL STRUCTURAL & FORMATTING RULES:\n"
                "1. Use markdown headers (###) for main sections and specific vehicle models. Never output raw HTML tags.\n"
                "2. Provide exactly two distinct sections using these exact markdown headers:\n"
                "   ### NEW CAR OPTIONS (Zero Meter)\n"
                "   ### USED CAR OPTIONS (Market Favorites)\n"
                "3. Under each vehicle recommendation, use clean bullet points (-) to detail: Trim/Variant, Estimated On-Road Price, Fuel Average (KM/L) for local city traffic, and Market Resale/Maintenance Reality.\n"
                "4. Keep the rationale focused on practical factors specific to the Pakistani market (e.g., Lahore/Karachi parts availability, dealership networks, and suspension durability for local roads).\n\n"
                
                "CRITICAL SAFETY RULE: If the user's input contains unusual symbols, gibberish, or is not related to cars/automotive topics, "
                "you MUST reject the prompt and reply exactly with: 'Error: I am a CarbonCraft intelligence. Please ask me about cars.' "
                "Do not provide any other information in this case."
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {
                        "role": "user", 
                        "content": f"I have a budget of {budget} PKR. I need a car for {use_type}. Suggest the best new and used options currently available in Pakistan."
                    }
                ],
                model="llama-3.1-8b-instant",
            )
            
            raw_content = chat_completion.choices[0].message.content
            
            # Guard rail logic match
            if "Error: I am a CarbonCraft intelligence" in raw_content:
                ai_response = f'<div class="text-red-400 border border-red-500/20 bg-red-500/5 rounded-lg p-4 font-mono text-xs">{raw_content}</div>'
            else:
                # 1. Convert Markdown Headings (###) into glowing blue/white premium headers
                formatted = re.sub(
                    r'###\s*(.*?)\n', 
                    r'<div class="mt-8 mb-4 flex items-center gap-3 border-b border-blue-500/10 pb-2">'
                    r'<div class="w-1.5 h-4 bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.6)]"></div>'
                    r'<strong class="text-blue-400 text-xs font-black uppercase tracking-[0.25em] font-sans">\1</strong>'
                    r'</div>', 
                    raw_content
                )
                
                # 2. Format Bullet lines into uniform structural flex rows with a cyan/blue arrow
                formatted = re.sub(
                    r'^-\s*(.*?)$', 
                    r'<div class="flex items-start gap-2 my-2 font-sans text-sm text-gray-300">'
                    r'<span class="text-blue-500 select-none font-bold">▶</span>'
                    r'<span>\1</span>'
                    r'</div>', 
                    formatted, 
                    flags=re.MULTILINE
                )
                
                # 3. Apply line breaks seamlessly
                ai_response = formatted.replace('\n', '<br>')

        except Exception as e:
            ai_response = f'<div class="text-red-500 p-4 border border-red-500/30 rounded font-mono text-xs">System Failure: {str(e)}</div>'

    return render(request, 'ai_consultant2.html', {'result': ai_response})

def car_specs_view(request):
    specs_result = None
    
    if request.method == "POST":
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            car_name = request.POST.get('car_name', '').strip()

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
                            "\n\n"
                            "CRITICAL FORMATTING RULES:\n"
                            "1. Use '###' for MAJOR section headings only (e.g., ### Engine & Performance, ### Fuel Economy & Transmission).\n"
                            "2. Use standard bold markdown '**' only for minor inline keys, inline labels, or values (e.g., **Displacement:** 1498cc).\n"
                            "\n\n"
                            "CRITICAL RULE 2: If the user's input contains unusual symbols, gibberish, or is not related to cars/automotive topics, you MUST reject the prompt and reply exactly with: 'Error: I am a CarbonCraft intelligence. Please ask me about cars.' Do not provide any other information in this case."
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
            
            # STEP 1: Turn Major Sections (###) into Unique, Bold Blue layout blocks
            formatted = re.sub(
                r'###\s*(.*?)\n', 
                r'<div class="mt-8 mb-4 flex items-center gap-3 border-b border-stone-800 pb-2">'
                r'<div class="w-1.5 h-4 bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.6)]"></div>'
                r'<h3 class="text-blue-500 text-sm font-bold uppercase tracking-wider font-sans">\1</h3>'
                r'</div>\n', 
                raw_content
            )
            
            # STEP 2: Turn minor bold items (**) into clean, subtle off-white tags (not blue)
            formatted = re.sub(
                r'\*\*(.*?)\*\*', 
                r'<strong class="text-stone-200 font-semibold">\1</strong>', 
                formatted
            )
            
            # STEP 3: Replace bullet markers with clean custom structural indicators
            specs_result = formatted.replace('* ', '<span class="text-blue-500/80 mr-2 text-[10px]">▶</span> ').replace('\n', '<br>')
            
        except Exception as e:
            specs_result = f'<div class="text-xs text-red-400 p-4 bg-red-950/20 border border-red-900/30 font-mono">Error fetching specs: {str(e)}</div>'
            
    return render(request, 'car_specs.html', {'specs': specs_result})
    
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
                            "After the table, provide a short 'VERDICT' section in a separate paragraph. "
                            "CRITICAL RULE: If the user's input contains unusual symbols, gibberish, or is not related to cars/automotive topics, you MUST reject the prompt and reply exactly with: 'Error: I am a CarbonCraft intelligence. Please ask me about cars.' Do not provide any other information in this case."
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


def engine_recommendation_view(request):
    ai_response = None
    
    if request.method == "POST":
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            car_model = request.POST.get('car_model')
            budget = request.POST.get('budget')
            
            # The system message now instructs the LLM to use markdown markdown blocks so Python can inject custom components safely.
            system_msg = (
                "You are CarbonCraft's elite automotive expert specializing in engine swaps, performance modifications, "
                "and engine selection for the Pakistani car community, with deep knowledge of local markets like Bilal Gunj in Lahore. "
                "Given a car model and a budget (in PKR), provide a structured list of realistic engine options available in Pakistan.\n\n"
                
                "CRITICAL ENGINE FORMATTING RULES:\n"
                "1. Use markdown headers (###) for main sections and engine names. Never output raw HTML tags.\n"
                "2. Each recommendation MUST include the official Engine Code/Name, Make, and Model of origin (e.g., '### Toyota 1.5L 1NZ-FE (from Toyota Corolla/Vitz)').\n"
                "3. Under each engine, use bullet points (-) to detail: Horsepower/Torque, estimated fuel efficiency (KM/L) in Lahore city traffic conditions, a realistic PKR price estimate for the engine assembly alone in the local market, and a brief compatibility rationale.\n"
                "4. Separate the recommendations into distinct sections: Engine Options, Recommended Bolt-ons, and Necessary Alterations using Markdown titles.\n\n"
                
                "CRITICAL SAFETY RULE: If the input contains unusual symbols, gibberish, or is completely unrelated to cars, "
                "reply exactly with: 'Error: I am a CarbonCraft intelligence. Please ask me about cars.'"
            )
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": f"Car Model: {car_model}. Budget: {budget} PKR. Suggest locally viable engines, bolt-ons, and alterations."}
                ],
                model="llama-3.3-70b-versatile",
            )
            
            raw_content = chat_completion.choices[0].message.content
            
            # Check for safety error override before applying layout designs
            if "Error: I am a CarbonCraft intelligence" in raw_content:
                ai_response = f'<div class="text-red-400 border border-red-500/20 bg-red-500/5 rounded-lg p-4 font-mono text-xs">{raw_content}</div>'
            else:
                # 1. Convert Markdown Headings (###) into glowing blue/white premium headers
                formatted = re.sub(
                    r'###\s*(.*?)\n', 
                    r'<div class="mt-8 mb-4 flex items-center gap-3 border-b border-blue-500/10 pb-2">'
                    r'<div class="w-1.5 h-4 bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.6)]"></div>'
                    r'<strong class="text-blue-400 text-xs font-black uppercase tracking-[0.25em] font-sans">\1</strong>'
                    r'</div>', 
                    raw_content
                )
                
                # 2. Format Bullet lines to look uniform with your customized cyan/blue indicator arrow
                formatted = re.sub(
                    r'^-\s*(.*?)$', 
                    r'<div class="flex items-start gap-2 my-2 font-sans text-sm text-gray-300">'
                    r'<span class="text-blue-500 select-none font-bold">▶</span>'
                    r'<span>\1</span>'
                    r'</div>', 
                    formatted, 
                    flags=re.MULTILINE
                )
                
                # 3. Clean up loose ends and maintain baseline linebreaks safely
                ai_response = formatted.replace('\n', '<br>')
            
        except Exception as e:
            ai_response = f'<div class="text-red-500 p-4 border border-red-500/30 rounded font-mono text-xs">System Failure: {str(e)}</div>'
            
    return render(request, 'engine_recommend.html', {'result': ai_response})


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
            "Use bullet points for lists. Provide a professional summary. "
            "CRITICAL RULE: If the user's input contains unusual symbols, gibberish, or is not related to cars/automotive topics, you MUST reject the prompt and reply exactly with: 'Error: I am a CarbonCraft intelligence. Please ask me about cars.' Do not provide any other information in this case."
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