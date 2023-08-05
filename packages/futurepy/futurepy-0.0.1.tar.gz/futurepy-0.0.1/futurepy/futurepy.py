"""futurepy – A cli version for FutureMe

Usage:
    futurepy [options]

Options:
    -s --subject <subject>  Your message subject.
    -b --body <body>        Your message body.
    -d --date <date>        The future date to which to send your message to.
                            Format: YYYYMMDD
    -e --email <email>      Your email.
    -p --public             Post publicly
                            Default: False
    -c --confirm            Display a preview of the message before sending
                            Default: False
    -h --help               Display this message.

"""

import requests
from docopt import docopt
from logging import warnings
import time
import re
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
about = dict()
with open(os.path.join(here, '__version__.py'), 'r') as f:
    exec(f.read(), about)

def warn(x):
    #warnings.warn(x)
    sys.stderr.write(x+'\n')
    sys.exit(1)

def run(args):
    subject = args.get('--subject')
    if(subject == None):
        warn('-s --subject required.')
    body = args.get('--body')
    if(body == None):
        warn('-b --body required.')
    date = args.get('--date')
    if(date == None):
        warn('-d --date required.')
    else:
        try:
            t = time.strptime(date, '%Y%m%d')
            if(time.gmtime()[0] > t[0]):
                warn('You can\'t send messages to the past.')
        except ValueError:
            warn('Invalid date.')
    m = str(int(str(date[4:6])))
    d = str(int(str(date[6:])))
    y = str(int(str(date[:4])))

    email = args.get('--email')
    if(email == None):
        warn('-e --email required.')
    else:
        match = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I)
        if not(match):
            warn('Invalid email.')
    public = args.get('--public')
    confirm = args.get('--confirm')

    url = 'https://api.futureme.org/letters'
    data = {
        'letter[subject]': subject,
        'letter[body]': body,
        'letter[send_date(2i)]': m,
        'letter[send_date(3i)]': d,
        'letter[send_date(1i)]': y,
        'letter[pick_date]': '1',
        'letter[public]': str(public).lower(),
        'letter[comments]': '',
        'letter[email]': email
    }

    if(confirm):
        print(subject)
        print()
        print(body)
        print()
        print('Delivery: {}/{}/{}\n'.format(y, m, d))
        conf = input('Confirm? [Y/n] ')
        if(conf in 'Yy '):
            print('A confirmation link was sent to ' + email + '. See you in the future!')
            res = requests.post(url, data=data)
        else:
            print('Exiting.')
    else:
        print('A confirmation link was sent to ' + email + '. See you in the future!')
        res = requests.post(url, data=data)

def main():
    args = docopt(__doc__, version=about['__version__'])
    try:
        run(args)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
