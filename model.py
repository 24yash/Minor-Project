import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

# print(api_key)

client = OpenAI(api_key=api_key)

assistant = client.beta.assistants.create(
  name="Chat Bot with Memory",
      instructions= """
    You are Course Compass, an AI assistant designed to recommend courses to users. Follow these guidelines:

  1. Identity and Purpose:
     - You are named Course Compass.
     - Your primary function is to recommend courses from Coursera, Udemy, MIT, and NPTEL.

  2. Interaction Process:
     - Engage in conversation with users to understand their preferences.
     - Based on the conversation, formulate relevant keywords for course recommendations.
     - Use these keywords as input for the course recommendation function.

  3. Recommendation Function:
     - You have access to a function that accepts a 'user query' parameter.
     - This query should consist of keywords relevant to the user's interests and needs.
     - The function will return course recommendations based on these keywords.

  4. Conversation Style:
     - Be polite, helpful, and concise in your interactions.
     - Avoid excessive cross-questioning. Gather necessary information efficiently.
     - Focus on understanding the user's needs and providing valuable recommendations.

  5. Keyword Formulation:
     - Provide relevant keywords as arguments to the recommendation function.
     - Ensure these keywords accurately reflect the user's expressed interests and requirements. These keywords should not be anything else like their background.

  Remember, your goal is to assist users in finding courses that best match their educational needs and interests.""" ,
  tools= [
    {
      "type": "function",
      "function": {
        "name": "get_courses",
        "description": "Provides Course Recommendations.",
        "parameters": {
          "type": "object",
          "properties": {
            "user_query": {
              "type": "string",
              "description": "The user preferences what they want to learn."
            }
          },
          "required": [
            "text"
          ]
        }
      }
    }
  ]
,
  model="gpt-4o-mini",
)

from d import get_relevant_courses_from_cluster_nptel, get_relevant_courses_from_cluster_mit, get_relevant_courses_from_cluster_udemy, get_relevant_courses_from_cluster_coursera

def get_courses(user_query):
    relevant_courses_nptel = get_relevant_courses_from_cluster_nptel(user_query, top_n=1)
    relevant_courses_mit = get_relevant_courses_from_cluster_mit(user_query, top_n=1)
    relevant_courses_udemy = get_relevant_courses_from_cluster_udemy(user_query, top_n = 2)
    relevant_courses_coursera = get_relevant_courses_from_cluster_coursera(user_query, top_n = 1)
    data =  {
        "NPTEL": relevant_courses_nptel,
        "MIT": relevant_courses_mit,
        "Udemy": relevant_courses_udemy,
        "Coursera": relevant_courses_coursera
    }
    # return data
    print('data: ')
    print(data)

    final_completion = client.chat.completions.create(
          model="gpt-4o",
          messages=[
              {"role": "system", "content": f"""Here are the top courses related to '{user_query}' from different platforms. Extract the most relevant courses and return the important information to the user. Follow these guidelines strictly:

  1. Provide the EXACT and COMPLETE links as given in the input data. Do not modify, shorten, or simplify the links in any way. THIS IS IMPORTANT!
  2. Include all relevant information for each course: title, platform, instructor (if available), and the exact link. You may also tell why this course will be beneficial to what they want which is: "{user_query}".
  3. If relevant courses are not available for a platform, mention that there are no relevant courses available for that platform.

  The courses are: {data}

  Respond with a well-formatted list of the most relevant courses, ensuring all links are preserved exactly as provided."""},
              {"role": "user", "content": user_query}
          ]
      )
    
    final_response = final_completion.choices[0].message.content
    # print("response: ")
    # print(final_response)
    return final_response



thread = client.beta.threads.create()

import time
def wait_on_run(run):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        
        time.sleep(0.5)
    return run

def get_response(prompt):
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    )
    import json
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        # print(messages)
        if messages.data:  # Check if there are any messages
                last_message = messages.data[0]  # Get the last message
                if last_message.content:  # Check if the message has content
                    text_content_block = last_message.content[0]  # Get the first TextContentBlock
                    message_text = text_content_block.text.value  # Extract the text value
                    # print(message_text)
                    return message_text
                else:
                    print("The last message has no content.")
                    print(messages)
        else:
            print(run.status)
    elif run.status == "requires_action":
        tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
        name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # print("Waiting for custom Function:", name)
        # print("Function arguments:")
        # print(arguments)
        function_response = get_courses(**arguments)

        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": tool_call.id,
                    "output": "done. function response:" + str(function_response),
                }
            ],
        )
        run = wait_on_run(run)
        return function_response
    else:
        print(run.status)
        print(run)
        return "Some Error occured in the LLM run. Sorry for the inconvenience."