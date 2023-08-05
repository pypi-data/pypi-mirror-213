# netbox-plugin-unacceptable-events-users-computers


```bash
pip3 install netbox-unacceptable-events-users-computers
```



Добавить в файле netbox/netbox/configuration.py

```
PLUGINS = [
    'ptuevents'
]
```

В командной строке
```
./manage.py migrate
```

Перезапустить сервер netbox.