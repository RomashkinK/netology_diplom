
## **Получить исходный код**

    git config --global user.name "YOUR_USERNAME"
    
    git config --global user.email "your_email_address@example.com"
    
    mkdir ~/my_diplom
    
    cd my_diplom
    
    git clone git@github.com:RomashkinK/netology_diplom.git
    
    cd netology_diplom
    
    sudo pip3 install  --upgrade pip
    
    sudo pip3 install -r requirements.txt
    
    python3 manage.py makemigrations
     
    python3 manage.py migrate
    
    python3 manage.py createsuperuser    
    
 
## **Проверить работу модулей**
    
    
    python3 manage.py runserver 


## **Для Silk**
    
    python3 manage.py collectstatic 

## **Настройка Auth VK**

Для настройки авторизации через VKOAuth2 с использованием Django Social Auth, сначала необходимо создать новое приложение VK. Для этого необходимо зайти на сайт https://vk.com/apps и зарегистрировать новое standalone-приложение.

При создании приложения вам понадобится указать следующие параметры:
1. Название приложения
2. Описание приложения
3. Категория приложения
4. Платформы, для которых разрабатывается приложение (Web)
5. Адрес сайта, на котором будет использоваться авторизация VKOAuth2 (URL вашего Django проекта)
6. В разделе настройки приложения нужно указать Redirect URI для авторизации (URL вида http://localhost:8000/complete/vkontakte/)

После создания приложения в VK, необходимо установить Django Social Auth и настроить его на использование VKOAuth2. В settings.py вашего Django проекта добавьте необходимые настройки для использования VKOAuth2:

```python
SOCIAL_AUTH_VK_OAUTH2_KEY = 'Ваш API ID приложения VK'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'Секретный ключ приложения VK'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_VK_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'v': '5.131'}
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['email']
```

Затем добавьте URL для авторизации через VKOAuth2 в urls.py вашего Django проекта:

```python
path('oauth/', include('social_django.urls', namespace='social')),
```

Теперь вы можете использовать авторизацию через VKOAuth2 в вашем Django проекте. При переходе по URL, указанному в Redirect URI при создании приложения VK, пользователи будут авторизовываться через VK и получать доступ к их профилю VK.

Более подробную информацию о настройке Django Social Auth  можно найти в официальной документации: https://python-social-auth.readthedocs.io