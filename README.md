# Online dict
                        
## Network Protocol
Request|Protocol|parameter
:------|:------:|:-------
register|R|username,password
log in |L|username,password
search|R|username,word
history|H|username

## Network transmission
socket--->TCP

## IO Multiplexing
 To handing multi-user requests

Reason:
- Large number of quests
- Short processing time 



## Client:
    page one:
        register-->username,password
        log in --->username,password
        exit------>sys.exit()
    page two:
        search word-->username,word
        look history
        cancellation--->back to page one 

## Server:
    handle mysql:
        register-->insert to users
        log in---->select-->insert to history
        search word-->select from word
        query history--->select from history where username is satisfied
    
## Optimization
MVC:
- model: class DictSql
- view : client-->page one --->page two
- controller:server-->class DictServer-->db=DictSql()
    