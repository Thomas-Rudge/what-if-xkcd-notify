#! python3
#-------------------------------------------------------------------------------
# Name:        what-if
# Purpose:     Send a notification via PushBullet when a new
#              What-If XKCD comic is available.
# Author:      Thomas Edward Rudge
#
# Created:     03-12-2015
# Copyright:   (c) Thomas Edward Rudge 2015
# Licence:     MIT
#-------------------------------------------------------------------------------
import bs4, os, re, requests, sys, time
from pushbullet import Pushbullet


def push_new_comic(title, link, token):
    '''
    Sends a link notification via push bullet.
    '''
    try:
        pb = Pushbullet(token)
        pb = pb.push_link('New What-If XKCD: %s' % title, link)
    except InvalidKeyError:
        pass

def get_previous_no(newno):
    '''
    Get the last comic number and update the tracker with the new one.
    '''

    try:
        newno = int(newno)
    except ValueError:
        raise Exception('Bad value for comic no %s. Expecting integer.' % newno)

    cwd = os.getcwd()

    ## Check if the tracking file is present.
    if os.path.isfile(cwd + '/tracker.txt'):
        ## Read the files contents.
        with open(cwd + '/tracker.txt', 'r') as file:
            prvno = file.read()

        if not prvno:
            prvno = newno - 1
    else:
        ## Set the previous number.
        prvno = newno - 1

    with open(cwd+'/tracker.txt', 'w') as file:
        file.write(str(newno))

    ## Make sure the value taken from file is a number.
    try:
        int(prvno)
    except ValueError:
        raise Exception('Bad value in tracker file %s. Expecting integer.' % prvno)

    return(prvno)


def main(
        csspath_comic = '#entry-wrapper > article > a',
        access_token = None
        ):
    '''
    Fetch the latest xkcd what-if comic number. If it is a new comic
    number, send a pushbullet notification.
    '''
    if access_token is None:
        sys.exit()

    ## Get the main what-if page.
    page= None

    for attempt in range(1,4):
        page = requests.get('http://www.what-if.xkcd.com/')
        try:
            page.raise_for_status()
            break
        except requests.RequestException:
            ## Wait and try again. Wait time increases with each attempt 10, 20, 30.
            time.sleep(attempt*10)

    if page is None:
        ## Failed to get page.
        sys.exit()

    ## Get the html that details the comic number
    xkcd_soup = bs4.BeautifulSoup(page.text, 'lxml')
    comic_no = xkcd_soup.select(csspath_comic)

    if not comic_no:
        ## The css path is not valid.
        sys.exit()

    comic_title = comic_no[0].text
    regx = re.compile('/\d+/')
    regx = regx.findall(str(comic_no[0]))

    if not regx:
        ## Couldn't find the comic number.
        sys.exit()
    else:
        regx = regx[0][1:-1]

    ## Get the previous comic number.
    previous_comic = get_previous_no(regx)

    ## If the new comic number is greater, send a notification.
    if int(previous_comic) < int(regx):
        push_new_comic(
                        comic_title,
                        'http://what-if.xkcd.com/' + regx + '/',
                        access_token
                        )

if __name__ == '__main__':
    var_ = sys.argv

    if not var_:
        sys.exit()

    ## Expect var_ to be a list [script location, PushBullet Token]
    ## when script is called from batch file.
    main(access_token = var_[1])
