from urllib.parse import parse_qs

def handler(event, context):
  # Ensure the request method is POST
  if event['httpMethod'] != 'POST':
    return {
      'statusCode': 405,
      'body': 'Method Not Allowed',
    }

  # Parse the form data
  body = parse_qs(event['body'])
  
  for k, v in body.items():
      print(f'{k}: {v}')

  # Do something with the form data

  # Return a success response
  return {
    'statusCode': 200,
    'body': 'Success',
  }
