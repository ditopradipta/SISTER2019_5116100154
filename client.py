import Pyro4
import subprocess


def get_server():
    uri = "PYRONAME:greetserver@localhost:7777"
    gserver = Pyro4.Proxy(uri)
    return gserver



if __name__=='__main__':
    server = get_server()
    
    if server == None:
        exit()
    test = True
    while test:


        text = input ("> ").lower()
        text_split = text.split()
        if text_split[0] == 'list':
            print(server.get_list_dir(text))
        elif text_split[0] == 'create':
            print(server.create_handler(text))
        elif text_split[0] == 'delete':
            print(server.delete_handler(text))
        elif text_split[0] == 'read':
            print(server.read_handler(text))
        elif text_split[0] == 'update':
            print(server.update_handler(text))
        elif text_split[0] == 'exit':
            print(server.bye())
            test = False
        else:
            print(server.command_not_found())
