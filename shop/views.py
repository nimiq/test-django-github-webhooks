import json
import hmac
import hashlib

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return HttpResponse('<html>My Icecream Shop</html>')

GITHUB_WEBHOOK_PASSWORD = 'mypassword'
GITHUB_WEBHOOK_EVENTS = {
    'push': True,
    'release': True,
}
GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH = 'develop'

@csrf_exempt
def github_webhook(request):
    # Read the signature sent by GitHub.
    github_signature = request.META.get('HTTP_X_HUB_SIGNATURE', '')
    # Compute the signature based on the password.
    signature = 'sha1=' + hmac.new(GITHUB_WEBHOOK_PASSWORD, request.body, hashlib.sha1).hexdigest()

    # Compare the signatures.
    #if not hmac.compare_digest(signature, github_signature):  # Works only for Python >= 2.7.7|3.3
    if not signature == github_signature:
        raise Http404

    # The signature is valid, parse the content.
    payload = json.loads(request.body)
    print(payload)

    event = request.META.get('HTTP_X_GITHUB_EVENT', '')  # 'push', 'release', ...
    print('EVENT={}'.format(event))

    handler = {'push': handle_push,
               'release': handle_release}.get(event, None)
    if handler:
        handler(payload)

    return HttpResponse('OK')


def handle_push(payload):
    if not GITHUB_WEBHOOK_EVENTS.get('push', False):
        return

    if not 'refs/heads/{}'.format(GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH) in payload['ref']:
        print('You did NOT push to the monitored branch: {}'.format(payload.get('ref', '')))
        return

    print('You did push to the monitored branch: {}'.format(GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH))


def handle_release(payload):
    if not GITHUB_WEBHOOK_EVENTS.get('release', False):
        return

    tag_name = payload['release']['tag_name']
    draft = payload['release']['draft']

    if draft:
        print('TAG_NAME={}\nDRAFT={}\nJust a draft'.format(tag_name, draft))
        return

    print('TAG_NAME={}\nDRAFT={}'.format(tag_name, draft))
