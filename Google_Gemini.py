import google.generativeai as genai
import os

API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY')

print(API_KEY)

genai.configure(api_key='')

model = genai.GenerativeModel('gemini-1.5-flash')

# response = model.generate_content("""
        
#         import google.generativeai as genai
#         import os

#         API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY')

#         print(API_KEY)

#         genai.configure(api_key='')

#         model = genai.GenerativeModel('gemini-1.5-flash')

#         response = model.generate_content("Please tell me what more I can do with you and what my options are beyond model.generate_content")
#         chat = model.start_chat()


#         print(response.text)
#         model.start_chat()
#         print(chat)

    
#     """)


response = model.generate_content("give me the python code to start a chat with you")
# chat = model.start_chat()


print(response.text)
# model.start_chat()
# print(chat)
