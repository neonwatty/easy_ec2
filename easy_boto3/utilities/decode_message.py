import subprocess
import json

def decode_authorization_failure_message(message):
    if not message or message == '-h' or message == '--help':
        print("""Usage: decode-authorization-failure-message <message>
Use this when Amazon gives you an "Encoded authorization failure message" and
you need to turn it into something readable.""")
        return 1

    cmd = ['aws', 'sts', 'decode-authorization-message', '--encoded-message', message]
    output = subprocess.check_output(cmd).decode('utf-8')
    decoded_message = json.loads(output)["DecodedMessage"]
    decoded_message = decoded_message.replace('\\"', '"').strip('"')
    return json.loads(decoded_message)

# Example usage
message = "<encoded-message>"
result = decode_authorization_failure_message(message)
print(result)
