import re
import openai

openai.api_key = "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"

def message_prob(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True
    user_words = re.split(r'\s+|[,;:?!.-]\s*', user_message.lower())
    for word in user_words:
        if word in recognised_words:
            message_certainty += 1
    
    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0
    

def check_all_messages(message):
    highest_prob_list = {}
    
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_prob(message, list_of_words, single_response, required_words)
    
    # Responses
    response('Hello!', ['hello', 'heyy', 'sup', 'hii'], single_response=True)
    response("I'm doing fine and you?", ['how', 'are', 'you'], required_words=['how'])
    response('Thank you', ['bye', 'quit', 'exit'], required_words=['quit', 'bye', 'exit'], single_response=True)

        
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return best_match

def get_response(user_input):
    answer = None
    try:
        if answer is None:
            prompt = f"User: {user_input}\nBot:"
            model = "text-davinci-002"
            completions = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
                timeout=5  # Set the timeout value (in seconds)
            )
            answer = completions.choices[0].text.strip()
    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return answer
    

while True:
    user_input = input('You: ')
    bot_response = get_response(user_input)
    print('Bot:', bot_response)
    if bot_response == 'quit':
        break

