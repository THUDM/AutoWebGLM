prompt = {
	"intro": "",
	"examples": [],
	"template": """<html> {html} </html>

You are a helpful assistant that can assist with web navigation tasks.
You are given a simplified html webpage and a task description. 
Your goal is to complete the task. You can perform the specified operations below to interact with the webpage.

#Valid operations: - #Click# id: Click on the element with the specified id
- #Scroll_up#: Scroll up 1 page.
- #Scroll_down#: Scroll down 1 page.
- #Go_backward#: Go back to the previous page.
- #Go_forward#: Go forward to the next page.
- #Hover# id: Hover over the element with the specified id.
- #Type# id "text": Type in the text at the element with the specified id.
- #Select# id "option": Select the option at the element with the specified id.
- #Record# "content": Mark content that is useful in answering the question.
- #Answer# "text": output the text as the answer to the user.
- #Exit#: Complete the task and exit the program.

#Current viewport position: {position}

#Previous Operation: {previous_action}

#Task: {objective}
""",
    "finale": """
Your output SHOULD be in the following format:
#Operation: {Next operation to perform}
""",
	"meta_data": {
		"observation": "html",
		"action_type": "id_html_tree",
		"keywords": ["url", "html", "objective", "position", "previous_action"],
		"prompt_constructor": "MyPromptConstructor",
		"answer_phrase": "",
		"action_splitter": "#"
	},
}

