from groq import Groq
from config import GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

def generate_summary(diff):
    # fetch context from text file to pass onto the model
    with open('./ai/content.txt', 'r') as file:
        context = file.read() 
        
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": diff
            }
        ]
    )
    summary = completion.choices[0].message.content

    return summary