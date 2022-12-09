def handler(event, context):
  # Ensure the request method is POST
  if event['httpMethod'] != 'POST':
    return {
      'statusCode': 405,
      'body': 'Method Not Allowed',
    }

  # Ensure the request content-type is "application/x-www-form-urlencoded"
  if event['headers']['content-type'] != 'application/x-www-form-urlencoded':
    return {
      'statusCode': 400,
      'body': 'Bad Request',
    }

  # Parse the form data
  body = parse_qs(event['body'])
  
  for k, v in body.items():
      print(f'{key}: {value}')

  # Do something with the form data

  # Return a success response
  return {
    'statusCode': 200,
    'body': 'Success',
  }
