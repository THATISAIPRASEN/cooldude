import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.views import generic
from django.http.response import HttpResponse
# Create your views here.



def decode(message):
    outmessage = message
    outmessage = ''
    outarr = ''
    jokes = ''
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', message).lower().split()
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo Mama joke!"
    return outmessage


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAU16JlAvmABAOelhAicq6kxSOKPTYEFY2JgB3q68dkQHTALhzOD1UZCMwGNqXWB2uLnfibA35R8iPj7UZBbawGlb36lQA7WsN1ZCCPtUjSvZAPUejTPX3keHu9A1BaMf70wPL3gx4VGKzNlG4K7LWhqDA3YDpXRvDZBdZBhWXjgZDZD'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class CoolDudeView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '210798':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
