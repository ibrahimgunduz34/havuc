# Havuç Nedir ?
Havuç, ürün bazında fiyat karşılaştırmanızı sağlayan bir web uygulamasıdır.

# Nasıl Çalışır ?
Havuç, ürün katoloğunda tanımladığnız her bir ürün için, ürünün bulunduğu web sitelere periyodik olarak bağlanarak fiyat ve resim bilgilerini toplar, arşivler. İlgili ürünün en düşük fiyatla nerede bulunduğu bilgisini saklar.

# Kurulum:

Uygulamayı geliştirme ortamında çalıştırmak için;

. Sanal ortam kurulumunu gerceklestirn.

```shell
$ virtualenv havuc-env
$ cd havuc-env
```

. Uygulamayı git reposundan geliştirme ortamınıza kopyalayın.

```shell
$ git clone git@github.com:ibrahimgunduz34/havuc.git
```

. Sanal ortamı aktif duruma getirin ve uygulama için gerekli paketlerin kurulumunu gerceklestirin.

```shell
$ source bin/activate
$ pip install -r requirements.pip
```

. Redis kurulumunu gerçekleştirin. (yoksa)

```shell
$ sudo apt-get install redis-server
```

. SQLite veritabanın yaratılması için syncdb komutunu çalıştırın.

```shell
$ python manage.py syncdb
```


# Çalıştırılması:
Havuc, fiyat edinme işlemini arkaplanda asenkron olarak gerçekleştirdiği için geliştirme ortamında celery kuyruklarını işleyecek django komutları çalıştırılmalıdır.

```shell
$ python manage.py celeryd -B
...
$ python managege.py celeryd -Q scheduled_tasks,crawler
```

. Development web sunucusunu çalıştırın.

```shell
$ python manage.py runserver
```

# Ekran Görüntüleri:

Ürün Listesi:
![Ürün Listesi](/docs/screenshots/screencapture-localhost-8000-admin-catalog-product.png)

Ürün Detayı:
![Ürün Detayı](/docs/screenshots/screencapture-localhost-8000-admin-catalog-product-2.png)