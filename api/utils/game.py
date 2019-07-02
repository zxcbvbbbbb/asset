
import sys,re
from subprocess import call

def exec_cmd(cmd):
    call(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)

game_list = ['ChessPoker','fish','fruit','game_FG']

def sync_game():
    for game in game_list:
        cmd = 'rsync -vzrtopg --delete --port=37873 rsync@218.17.239.26::game_fg/{0}/ /data/www/php/fg/gamelist/public/global/game/{0}/ --password-file=/etc/rsync.pass'.format(
            game)

# if __name__ == '__main__':
#         print(cmd)
