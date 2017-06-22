from app import create_app

import socket

if __name__ == '__main__':
    app = create_app('dev')
    if socket.gethostname() not in ['Boer-PC', 'boer-PC']:
        app = create_app('prod')
    
    app.run(host='0.0.0.0')
