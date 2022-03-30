# NFT-Creator

``` shell
$ git clone git@github.com:Enfyshsu/NFT-Creator.git
$ cd NFT-Creator
$ mkdir media
```

``` shell
$ vim data.json
```

In data.json:
``` json=
{
    "SERVER_IP": <Your server IP>,
    "SECRET_KEY": <Your django secret key>
}
```

Run:
``` shell
$ python3 manage.py runserver <Your server IP>:8000
```

For example: 
``` shell
$ python3 manage.py runserver localhost:8000
```