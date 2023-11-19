from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from bs4 import BeautifulSoup

    
class ActionCallFlaskAPI(Action):
    def name(self):
        return "action_call_flask_api"

    def run(self, dispatcher, tracker, domain):
        # Get the user's message
        user_message = tracker.latest_message.get('text')

        # Send a POST request to your Flask app
        import requests
        response = requests.post('http://localhost:5000/webhook', json={'message': user_message})

        # Extract the response from your Flask app
        bot_response = response.json().get ('text', 'Sorry, I didn\'t understand.')

        # Send the bot's response to the user
        dispatcher.utter_message(bot_response)

        return []

class ActionGetTermMeaning(Action):
    def name(self) -> Text:
        return "action_get_term_meaning"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entity = tracker.latest_message["entities"]
        term = entity[0]['value']

        meaning = self.get_term_meaning(term)
        dispatcher.utter_message(f" '{term}' means {meaning}")
        return []

    def get_term_meaning(self, term):
        url = f'https://www.merriam-webster.com/dictionary/{term}'
        #url = f"https://dictionary.cambridge.org/dictionary/english/{term}"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find the element that contains the definition
            meaning = soup.find("span", class_="dtText")
            if meaning:
                return meaning.text
            else:
                return f"Meaning for '{term}' not found."
        else:
            return f"Unable to retrieve data for '{term}'."