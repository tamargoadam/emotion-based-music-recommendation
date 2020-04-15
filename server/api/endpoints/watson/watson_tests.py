import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Authentication Method
with open("../credentials/watson_credentials.json", "r") as file:
        creds = json.load(file)
        authenticator = IAMAuthenticator(creds['API_KEY'])
        tone_analyzer = ToneAnalyzerV3(
                version=creds['VERSION'],
                authenticator=authenticator)
        tone_analyzer.set_service_url(creds['URL'])

# Start of Tests -- Try not to waste all of our API calls!
# Uncomment if you wish to run the test functions!
print('Uncomment the tests in the code, then run again. This is to prevent excess API calls.')
"""
print("\ntone_chat() example 1:\n")
utterances = [{
    'text': 'I am very happy.',
    'user': 'glenn'
}, {
    'text': 'It is a good day.',
    'user': 'glenn'
}]
tone_chat = tone_analyzer.tone_chat(utterances).get_result()
print(json.dumps(tone_chat, indent=2))

print("\ntone() example 1:\n")
print(
    json.dumps(
        tone_analyzer.tone(
            tone_input='I am very happy. It is a good day.',
            content_type="text/plain").get_result(),
        indent=2))


with os.scandir('resources/') as entries:
    for entry in entries:
        print(entry.name)

print("\ntone() example 2:\n")
with open(join(os.getcwd(),
               'resources/tone-example.json')) as tone_json:
    tone = tone_analyzer.tone(json.load(tone_json)['text'], content_type="text/plain").get_result()
print(json.dumps(tone, indent=2))


print("\ntone() example 3:\n")
with open(join(os.getcwd(),
               'resources/tone-example.json')) as tone_json:
    tone = tone_analyzer.tone(
        tone_input=json.load(tone_json)['text'],
        content_type='text/plain',
        sentences=True).get_result()
print(json.dumps(tone, indent=2))
print("\ntone() example 4:\n")
with open(join(os.getcwd(),
               'resources/tone-example.json')) as tone_json:
    tone = tone_analyzer.tone(
        tone_input=json.load(tone_json),
        content_type='application/json').get_result()
print(json.dumps(tone, indent=2))
print("\ntone() example 5:\n")
with open(join(os.getcwd(),
               'resources/tone-example-html.json')) as tone_html:
    tone = tone_analyzer.tone(
        json.load(tone_html)['text'],
        content_type='text/html').get_result()
print(json.dumps(tone, indent=2))

print("\ntone() example 6 with GDPR support:\n")
with open(join(os.getcwd(),
               'resources/tone-example-html.json')) as tone_html:
    tone = tone_analyzer.tone(
        json.load(tone_html)['text'],
        content_type='text/html',
        headers={
            'Custom-Header': 'custom_value'
        })

print(tone)
print(tone.get_headers())
print(tone.get_result())
print(tone.get_status_code())

print("\ntone() example 7:\n")
tone_input = ToneInput('I am very happy. It is a good day.')
tone = tone_analyzer.tone(tone_input=tone_input, content_type="application/json").get_result()
print(json.dumps(tone, indent=2))
"""