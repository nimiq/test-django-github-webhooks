import json
import hmac
import hashlib
import os
import subprocess
import logging

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


log = logging.getLogger('github_webhooks')
log.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)


def home(request):
    return HttpResponse('<html>My Icecream Shop</html>')


# Settings (to be moved to the settings file).
GITHUB_WEBHOOK_PASSWORD = 'mypassword'
GITHUB_WEBHOOK_EVENTS = {
    'push': True,
    'release': True,
}
GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH = 'develop'
GITHUB_WEBHOOK_SCRIPT_TO_TRIGGER = os.path.abspath(os.path.join(settings.BASE_DIR,
                                                                'auto_deployment_script.sh'))
GITHUB_WEBHOOK_SCRIPT_LOG_FILE = os.path.abspath(os.path.join(settings.BASE_DIR,
                                                              'auto_deployment_script.log'))


@csrf_exempt
def github_webhook(request):
    # Only POST requests are served.
    if not request.method.upper() == 'POST':
        raise Http404

    # Read the signature sent by GitHub.
    github_signature = request.META.get('HTTP_X_HUB_SIGNATURE', None)
    if not github_signature:
        raise Http404

    # Compute the signature based on the password.
    signature = 'sha1=' + hmac.new(GITHUB_WEBHOOK_PASSWORD, request.body, hashlib.sha1).hexdigest()

    # Compare the signatures.
    #if not hmac.compare_digest(signature, github_signature):  # Works only for Python >= 2.7.7|3.3
    if not signature == github_signature:
        raise Http404

    # The signature is valid, parse the content.
    payload = json.loads(request.body)
    log.debug(payload)

    event = request.META.get('HTTP_X_GITHUB_EVENT', '')  # 'push', 'release', ...
    log.info('Received a GitHub Webhook with event={}'.format(event))

    handler = {'push': handle_push,
               'release': handle_release}.get(event, None)
    if handler:
        try:
            handler(payload)
            run_script()
        except EventNotMonitored as ex:
            log.info('A GitHub Webhook was received but the given event is not '
                     'monitored. {}'.format(ex))

    return HttpResponse('OK')


def handle_push(payload):
    if not GITHUB_WEBHOOK_EVENTS.get('push', False):
        raise EventNotMonitored('The monitoring of the push event is disabled in the settings.')

    pushed_branch = payload['ref']
    if not 'refs/heads/{}'.format(GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH) in pushed_branch:
        raise EventNotMonitored('Push webhooks received on the branch {}. '
                                'This branch is not being monitored. '
                                'The monitored branch is {}.'.format(
                                    pushed_branch, GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH))

    log.info('Push webhooks received on the monitored branch {}.'.format(
        GITHUB_WEBHOOK_PUSH_MONITORED_BRANCH))


def handle_release(payload):
    if not GITHUB_WEBHOOK_EVENTS.get('release', False):
        raise EventNotMonitored('The monitoring of the release event is disabled in the settings.')

    tag_name = payload['release']['tag_name']
    draft = payload['release']['draft']

    if draft:
        raise EventNotMonitored('Release webhooks received, but it is a draft release. '
                                'Draft releases are not monitored. '
                                'Tag_name={} and draft={}.'.format(tag_name, draft))

    log.info('Release webhooks received with tag_name={}.'.format(tag_name))


def run_script():
    log.info('Triggering the script: {}'.format(GITHUB_WEBHOOK_SCRIPT_TO_TRIGGER))
    subprocess.Popen('{} >>{} 2>&1'.format(
        GITHUB_WEBHOOK_SCRIPT_TO_TRIGGER, GITHUB_WEBHOOK_SCRIPT_LOG_FILE), shell=True)


class EventNotMonitored(Exception):
    pass