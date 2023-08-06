import os
import os.path as path
import subprocess as sp
import multiprocessing as processor

# from time import sleep
from colorama import init, Fore, Style
from configparser import ConfigParser

def main():
    DEFAULT_CONFIG = ConfigParser()

    DEFAULT_CONFIG['MAIN'] = {
        'http_server_status' : False,
        'tor_service_status' : False,
    }

    DEFAULT_CONFIG['WEB'] = {
        'file_dir': '/var/www/html',
        'hidden_service_dir': '/var/lib/tor/hidden_service',
        'is_active': False,
        'is_online': False,
        'domain': 'None',
    }

    HTTP_SERVER = 'http_server'
    TOR_SERVICE = 'tor_service'
    ONION_START_MARKER = "#-- START OF ONION SERVICES --#"
    ONION_STOP_MARKER = "#-- END OF ONION SERVICES --#"


    USERNAME = sp.getoutput('whoami')
    SYSTEM_HOSTNAME = sp.getoutput('hostname')
    HOSTNAME = 'onion'

    BOX_INFO = 'SERVER'

    TASK_LIST = {}


    def change_hostname(new_hostname):
        sp.getoutput(f'hostname {new_hostname}')

    class Settings:
        def __init__(self, filename):
            self.config = ConfigParser()
            self.filename = filename
            self.config_dict = dict()


        def scan(self):
            self.config.read(self.filename)

            for section in self.config.sections():
                self.config_dict[section] = dict(self.config.items(section))


        def get(self, name):
            self.scan()
            section = self.config_dict[name]

            self.make_python(section)        
            
            return section
        
        def add(self):
            return self.config

        
        def update(self):
            for KEY in self.config_dict:
                VALUE = self.config_dict[KEY]
                self.make_config(VALUE)

                self.config[KEY] = VALUE

                with open(self.filename, 'w') as file:
                    self.config.write(file)

        def make_python(self, section):
            for KEY in section:
                VALUE = section[KEY]
                if VALUE == 'True':
                    section[KEY] = True
                elif VALUE == 'False':
                    section[KEY] = False
                elif VALUE == 'None':
                    section[KEY] = None

        def make_config(self, section):
            for KEY in section:
                VALUE = section[KEY]
                if VALUE == None:
                    section[KEY] = 'None'
            




    def kill_task(_type: str = HTTP_SERVER):
        server = 'python3 -m http.server --bind 127.0.0.1 8080'
        pid = []

        def kill(task):
            processes = sp.getoutput(f'ps aux | grep "{task}"').split('\n')

            for item in processes:
                item = item.split()
                if '"' in item:
                    item.remove('"')
                
                if len(item) > 2:
                    pid.append(item[1])
            else:
                for id in pid:
                    sp.getoutput(f'kill {id}')

        if _type == HTTP_SERVER:
            kill(server)
        elif _type == TOR_SERVICE:
            pid = sp.getoutput('pidof tor')
            sp.getoutput(f'kill {pid}')


    def make_services_active():
        CONFIG = settings.get('MAIN')
        CONFIG['http_server_status'] = True
        CONFIG['tor_service_status'] = True
        settings.update()


    def http_server():
        KEY = 'http_server_status'
        CONFIG = settings.get('MAIN')

        kill_task(HTTP_SERVER)
        server = sp.getoutput('python3 -m http.server --bind 127.0.0.1 8080')
        CONFIG[KEY] = False
        settings.update()



    def tor_service():
        KEY = 'tor_service_status'
        CONFIG = settings.get('MAIN')

        kill_task(HTTP_SERVER)
        service = sp.getoutput('tor')
        CONFIG[KEY] = False
        settings.update()


    def start(process, name: str = None):
        HANDLER = processor.Process(target=process, name=name)
        HANDLER.start()

        TASK_LIST[HANDLER.name] = HANDLER
        return HANDLER


    def stop(name):
        process = TASK_LIST[name]
        KEY =  name + '_status'
        CONFIG = settings.get('MAIN')

        try:
            CONFIG[KEY] = False
            settings.update()
        except:
            ...

        kill_task(name)

        process.terminate()



    def init_torrc():
        with open('/etc/tor/torrc', 'r') as file:
            file = file.readlines()
            SECTION_MARKER = "## This section is just for relays ##"

            #Check in /etc/tor/torrc has already been configured.
            for lines in file:
                if ONION_START_MARKER in lines:
                    return
                

            for line in range(len(file)):
                line_index = line - 1
                
                if SECTION_MARKER in file[line_index]:
                    onion_torrc = [
                        '\n',
                        f'{ONION_STOP_MARKER}\n',
                        'HiddenServicePort 80 127.0.0.1:8080\n',
                        'HiddenServiceDir /var/lib/tor/hidden_service/\n',
                        f'{ONION_START_MARKER}\n'
                    ]
                    
                    for conf in onion_torrc:
                        file.insert(line_index, conf)
                    else:
                        with open('/etc/tor/torrc', 'w') as torrc:
                            torrc.writelines(file)

                    break       
                                    


    def get_domain(_path: str | None = None):
        if _path != None and path.isfile(_path):
            with open(_path, 'r') as hostname:
                return hostname.read()



    # SYSTEM UPDATE FUNCTIONS
    def update_online_status(session):
        service = 'HiddenServicePort 80 127.0.0.1:8080\n'
        with open('/etc/tor/torrc') as file:
            file = file.readlines()
            for line in file:
                if service in line and '#' in line:
                    session['is_online'] = False
                elif service in line and '#' not in line:
                    session['is_online'] = True

    def update_web_service():
        session = settings.get('WEB')
        
        service_dir = session['hidden_service_dir']
        if path.isdir(service_dir):
            domain = get_domain(f'{service_dir}/hostname')
            session['domain'] = domain
            session['is_active'] = True
        else:
            session['is_active'] = False
            session['domain'] = None

        update_online_status(session)
        settings.update()

    def update_server():
        update_web_service() #Update tor web hosting services

    def server_cmd(cmd):
        server = cmd.split('.')
        action = server[1]

        if action == 'start':
            GET = settings.get('MAIN')
            if GET['http_server_status'] != True and GET['tor_service_status'] != True:
                start(make_services_active, 'ACTIVATE')
                start(tor_service, TOR_SERVICE)
                start(http_server, HTTP_SERVER)
            else:
                print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  server already running...')
        elif action == 'stop':
            processes = [TOR_SERVICE, HTTP_SERVER]
            for i in range(2):
                try:
                    stop(processes[i-1])
                except:
                    ...
            
        elif action == 'scan':
            update_server()


    def handle_cmd(cmd):
        if cmd == 'exit':
            processes = [TOR_SERVICE, HTTP_SERVER]
            for i in range(2):
                try:
                    stop(processes[i-1])
                except:
                    ...
            
            change_hostname(SYSTEM_HOSTNAME)
            exit()
        elif 'tor' in cmd:
            command = cmd.split('.')
            action = command[1]
            GET = settings.get('MAIN')

            if action == 'start':
                if GET['tor_service_status'] != True:
                    GET['tor_service_status'] = True
                    settings.update()
                    start(tor_service, TOR_SERVICE)
                else:
                    print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  tor already running...')
            elif action == 'stop':
                if GET['tor_service_status'] != False:
                    stop(TOR_SERVICE)
                else:
                    print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  tor already stopped!')
                    
        elif 'http' in cmd:
            command = cmd.split('.')
            action = command[1]
            GET = settings.get('MAIN')

            if action == 'start':
                if GET['http_server_status'] != True:
                    GET['http_server_status'] = True
                    settings.update()
                    start(http_server, HTTP_SERVER)
                else:
                    print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  http already running...')
            elif action == 'stop':
                if GET['http_server_status'] != False:
                    stop(HTTP_SERVER)
                else:
                    print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  http already stopped!')
                    
        elif cmd == 'clear':
            sp.run('clear', shell=True)
        elif 'server' in cmd:
            server_cmd(cmd)    
        elif cmd == 'status':
            CONFIG = settings.get('MAIN')
            http = CONFIG['http_server_status']
            tor = CONFIG['tor_service_status']

            print()
            if tor == True:
                print(f'  [{Fore.GREEN + Style.BRIGHT} * {Style.RESET_ALL}] {Fore.BLUE} tor{Style.RESET_ALL}')
            else:
                print(f'  [{Fore.RED + Style.BRIGHT} * {Style.RESET_ALL}] {Fore.BLUE} tor{Style.RESET_ALL}')
            
            if http == True:
                print(f'  [{Fore.GREEN + Style.BRIGHT} * {Style.RESET_ALL}] {Fore.BLUE} http{Style.RESET_ALL}')
            else:
                print(f'  [{Fore.RED + Style.BRIGHT} * {Style.RESET_ALL}] {Fore.BLUE} http{Style.RESET_ALL}')

        elif cmd == 'scan':
            update_server() #update all running services on server
        elif 'web' in cmd:
            web = cmd.split('.')
            action = web[1].split()

            if action[0] == 'dir':
                try:
                    if path.isdir(action[1]):
                        settings.get('WEB')['file_dir'] = action[1]
                        settings.update()
                        sp.getoutput(f"rm -r {settings.get('WEB')['hidden_service_dir']}")
                except:
                    ...

            elif action[0] == 'info':
                update_web_service() #update web services only

                session = settings.get('WEB')


                if session['is_active'] == True:
                    active_status = f'{Fore.GREEN + Style.BRIGHT}ACTIVE{Style.RESET_ALL}'
                else:
                    active_status = f'{Fore.RED + Style.BRIGHT}INACTIVE{Style.RESET_ALL}'

                if session['is_online'] == True:
                    online_status = f'{Fore.GREEN + Style.BRIGHT}ONLINE{Style.RESET_ALL}'
                else:
                    online_status = f'{Fore.RED + Style.BRIGHT}OFFLINE{Style.RESET_ALL}'

                print(f'''
    [ {online_status} ] [ {active_status} ]

    [ {Fore.YELLOW + Style.BRIGHT}File Dir{Style.RESET_ALL} ] {session['file_dir']}
    [  {Fore.YELLOW + Style.BRIGHT}Domain{Style.RESET_ALL}  ] {session['domain']}''')
            else:
                new_command = action[0]
                
                if new_command == 'set' and len(action) == 2:
                    argument = action[1]

                    set = settings.get('WEB')
                    # service_dir = set['hidden_service_dir']
                    set_status = set['is_online']
                    service_line = f'HiddenServicePort 80 127.0.0.1:8080\n'

                    def switch_status(state):
                        with open('/etc/tor/torrc', 'r') as torrc:
                            torrc = torrc.readlines()
                            start_section = torrc.index(f'{ONION_START_MARKER}\n')
                            stop_section = torrc.index(f'{ONION_STOP_MARKER}\n')
                            onion_torrc = torrc[start_section:stop_section]

                            for item in range(len(onion_torrc)):
                                if service_line in onion_torrc[item]:
                                    if state == 'online':
                                        onion_torrc[item] = onion_torrc[item].removeprefix('#')
                                    elif state == 'offline':
                                        onion_torrc[item] = f'#{onion_torrc[item]}'
    
                                    torrc[start_section:stop_section] = onion_torrc
                            else:
                                with open('/etc/tor/torrc', 'w') as write_torrc:
                                    write_torrc.writelines(torrc)
    
                    if argument == 'online':
                        if set_status != True:
                            set['is_online'] = True
                            switch_status('online')
                        else:
                            #error message web service is already offline
                            print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  Web service is already online.')

                    elif argument == 'offline':
                        if set_status != False:
                            set['is_online'] = False
                            switch_status('offline')
                        else:
                            #error message web service is already offline
                            print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  Web service is already offline.')

                    settings.update()
        else:
            output = sp.getoutput(cmd)
            print(output)



    #### Color the Input Place holder text and bolden certain texts Kali Linux Style
    uname_section = f'{Fore.WHITE}┌──({Fore.RED + Style.BRIGHT + USERNAME}'
    host_section = f'㉿{HOSTNAME + Fore.WHITE + Style.NORMAL})-['
    input_section = f'{Fore.WHITE}└─{Fore.RED + Style.BRIGHT}${Style.RESET_ALL}'

    # __main__ code
    DIR_NAME = f'{path.dirname(__file__)}'

    if path.isfile(f'{DIR_NAME}/config.ini') == False:
        with open(f'{DIR_NAME}/config.ini', 'w') as config_file:
            DEFAULT_CONFIG.write(config_file)
            
    settings = Settings(f'{DIR_NAME}/config.ini')
    init_torrc()

    if USERNAME != 'root':
        print(f'\n  [{Fore.YELLOW + Style.BRIGHT} MESSAGE {Style.RESET_ALL}]  {Fore.RED + Style.BRIGHT}Run as Root!{Style.RESET_ALL}')
    else:
        change_hostname('onion')
        try:
            while True:
                FILE_DIR = settings.get('WEB')['file_dir']
                os.chdir(FILE_DIR)

                if FILE_DIR == '/':
                    BOX_INFO = '~'
                else:
                    BOX_INFO = FILE_DIR.removesuffix("/")

                info_section = f'{Fore.LIGHTBLUE_EX + Style.BRIGHT + BOX_INFO + Fore.WHITE + Style.NORMAL}]\n'

                print(f'''\n{uname_section + host_section + info_section + input_section} ''', end="")
                handle_cmd(input())
        except KeyboardInterrupt:
            change_hostname(SYSTEM_HOSTNAME)


if __name__ == '__main__':
    main()