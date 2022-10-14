# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import sqlite3
from re import split, search
from sqlite3 import Error
from typing import Text, Dict, Any, List

from rasa_sdk import FormValidationAction, Tracker, Action
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
class ValidateReservationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reservation_form"

    def validate_seats(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        seats = slot_value;
        if int(seats) <= 0:
            message = "Shouldn't your order number be made of actual order number?"
            dispatcher.utter_message(message)
            return {"seats": None}
            # message = 'Thank you ' + names + ' for making your reservation at ' + cardinal_Val + ' ' + time_slot + ' in our ' + section + ' section. If you want to restart the conversation please feel free to tell the bot.'
            # dataUpdate(names, contact, cardinal_Val, section)
        return {"seats": seats}

    def validate_CARDINAL(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        cardinal_Val = slot_value
        if len(cardinal_Val) <= 2:
            hour = int(cardinal_Val)
            if hour >= 7 and hour < 10:
                # message = 'Thank you ' + names + ' for making your reservation at ' + cardinal_Val + ' ' + time_slot + ' in our ' + section + ' section. If you want to restart the conversation please feel free to tell the bot.'
                # dataUpdate(names,contact,cardinal_Val,section)
                return {"CARDINAL": cardinal_Val}
            else:
                message = 'Sorry! we are not open at that time😅. Open time is 7 pm to 10 pm'
                dispatcher.utter_message(message)
                return {"CARDINAL": None}
        if len(cardinal_Val) > 2:
            split_time = split(":", cardinal_Val, maxsplit=1)
            hour = int(split_time[0])
            minutes = int(split_time[1])
            if hour >= 7 and hour < 10:
                # message = 'Thank you ' + names + ' for making your reservation at ' + cardinal_Val + ' ' + time_slot + ' in our ' + section + ' section. If you want to restart the conversation please feel free to tell the bot.'
                # dataUpdate(names, contact, cardinal_Val, section)
                return {"CARDINAL": cardinal_Val}
            else:
                message = 'Sorry! we are not open at that time. Please choose another time.'
                dispatcher.utter_message(message)
                return {"CARDINAL": None}

    def validate_name(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        name = slot_value
        if len(name) <= 0:
            dispatcher.utter_message(text="Please input your name, so we can make a reservation for you 😀")
            return {"name": None}
            # message = 'Thank you ' + names + ' for making your reservation at ' + cardinal_Val + ' ' + time_slot + ' in our ' + section + ' section. If you want to restart the conversation please feel free to tell the bot.'
            # dataUpdate(names, contact, cardinal_Val, section)
        return {"name": name}

    def validate_phone(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        phone = slot_value
        if len(phone) <= 9:
            dispatcher.utter_message(text="Please input your actual phone, so we can make a reservation for you 😀")
            return {"phone": None}
        elif bool(search('[a-zA-Z]', phone)):
            dispatcher.utter_message(text="Please input your actual phone, so we can make a reservation for you 😀")
            return {"phone": None}
        # message = 'Thank you ' + names + ' for making your reservation at ' + cardinal_Val + ' ' + time_slot + ' in our ' + section + ' section. If you want to restart the conversation please feel free to tell the bot.'
        # dataUpdate(names, contact, cardinal_Val, section)
        return {"phone": phone}


class UpdateReservationDetails(Action):

    def name(self) -> Text:
        return "submit_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Runs a query using only the order ID column, outputs an utterance
        to the user w/ the relevent
        information for one of the returned rows.
        """
        conn = DbQueryingMethods.create_connection(db_file="rasa_db/freshfeast.db")
        seats = tracker.get_slot("seats")
        cardinal = tracker.get_slot("CARDINAL")
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone")
        # slot_value = tracker.get_slot("order_number")
        DbQueryingMethods.update_slots(conn=conn, seats=seats, cardinal=cardinal, name=name, phone=phone)
        dispatcher.utter_message(template="utter_submit")
        return []

class UpdatefeedbackDetails(Action):
    def name(self) -> Text:
        return "submit_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Runs a query using only the order ID column, outputs an utterance
        to the user w/ the relevent
        information for one of the returned rows.
        """
        conn = DbQueryingMethods.create_connection(db_file="rasa_db/freshfeast.db")
        taste = tracker.get_slot("taste")
        environment = tracker.get_slot("environment")
        service = tracker.get_slot("service")
        # slot_value = tracker.get_slot("order_number")
        DbQueryingMethods.update_feedback(conn=conn, taste=taste, environment=environment, service=service)
        dispatcher.utter_message(template="utter_feedback")
        return []

class DbQueryingMethods:
    def create_connection(db_file):
        """
        create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    def update_slots(conn, seats, cardinal, name, phone):

        cur = conn.cursor()
        sql = 'INSERT INTO  reservation(seats,cardinal,name,phone) VALUES("{0}","{1}","{2}","{3}");'.format(
            seats, cardinal, name, phone)
        cur.execute(sql)
        conn.commit()
        return []

    def update_feedback(conn, taste, service, environment):
        cur = conn.cursor()
        sql = 'INSERT INTO  feedback(taste,environment,service) VALUES("{0}","{1}","{2}");'.format(
            taste, environment, service)
        cur.execute(sql)
        conn.commit()
        return []


