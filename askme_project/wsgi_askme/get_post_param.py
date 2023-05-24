from cgi import parse


def application(env, start_response):
    print(env)

    try:
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    body = b'GET PARAMETERS: '
    qs = env.get('QUERY_STRING')
    print(qs)
    body += qs.encode()

    body += b'\nPOST PARAMETERS: '

    request_body = env['wsgi.input'].read(request_body_size)

    body += request_body
    body += '\n'.encode()

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [body]
