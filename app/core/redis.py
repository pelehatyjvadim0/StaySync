from redis import asyncio as aioredis 
from app.core.config import settings

from functools import wraps
import hashlib

import json
from typing import Any
from datetime import date, datetime

redis_pool = aioredis.ConnectionPool.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', decode_response = True)
client = aioredis.Redis(connection_pool=redis_pool)


# Генератор ключей для кеширования в Redis
def cache_key_generator(func_name: str, *args, **kwargs) -> str:
    # Создаём префикс удобного формата, постоянное cache будет указателем на то, что это кешированные данные с постгреса
    # Такое именование затем позволит нам в Redis сортировать ключи и понимать для чего этот ключ вообще нужен. Что-то типо класса)
    # второй указатель здесь - имя функции, с которой будет вызвана попытка записи или попытка чтения.
    # имя функции позволит сортировать запросы в Redis на нужную нам. Например очистить кеш только get_all_users, очень удобно.
    prefix = f'cache:{func_name}'
    
    # Фильтруем поступающие арги и кварги, защищаясь от иных типов переданных данных.
    # Наша третья часть ключа - хешированные арги и кварги, если среди аргов и кваргов будут нестабильные данные, например объекты в памяти,
    # хеши всегда будут разные и у нас будет миллион ключей, такой ключ затем не найти! 
    # каждый иной аргумент = другой ключ. 
    filtered_args = [a for a in args if isinstance(a, (str, bool, float, int, str, dict, list, type(None)))]
    filtered_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, (str, float, bool, int, str, dict, list, type(None)))}
    
    # приводим отфильтрованные арги и кварги к строке и объединяем. 
    # обязательно сортируем кварги, чтобы ключ не зависел от расположения переданных кваргов в функцию!
    args_data = str(filtered_args) + str(sorted(filtered_kwargs.items()))
    
    # хешируем кварги с помощью встроенного hashlib, методом md5. 
    # md5 ожидает на вход байты, переводим нашу строку аргов и кваргов в байты с помощью .encode()
    # hexdigest запарсит полученный от md5 хеш и превратит его удобный для прочтения человеку. md5 также гарантирует, что хеш будет не более 32 символов.
    hashed_args = hashlib.md5(args_data.encode()).hexdigest()
    
    # объединяем наш префикс и полученный хеш из строки аргов и кваргов.
    # ключ готов, возвращаем 
    return f'{prefix}:{hashed_args}'


# Функция для парсинга непонятных json'у данных в iso формат. Пригодится нам ниже, в основной функции обёртке для работы с кешем Redis
# пройдитесь ниже и вернитесь, когда ознакомитесь с cache_response!

# снова привет, если в json_dumps(srlzble_data) наш json увидит объект даты, он не выкинет ошибку, а посмотрит в свой аргумент default
# json_dumps(srlzble_data, default = json_serial)
# без паники вызовет json_serial и закинет в качестве аргумента неизвестный ему объект, нашу дату!
# в json_serial мы парсим дату в iso формат, с которым json отлично работает и отправляем ему обратно, ошибок нет, данные в json успешно сериализованы
def json_serial(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    # на случай, если json видит не дату, а другой объект, с которым он не умеет работать, вызовет наш except на SET метод и мы получим в логи эту строку, приложение не упадёт!
    raise TypeError(f'Type {type(obj)} not serializable.')


# Основной декоратор для работы с кешем Redis!
# expire - время жизни ключа в базе redis, указывается в секундах, по умолчанию 60 секунд.
# model - модель pydantic-схемы, обязательна для безопасности работы приложения и защиты от ошибок, обязательно указывайте pydantic схему ответа
# при установке докератора на эндпоинт в роутере
def cache_response(expire: int = 60, model: Any): #type: ignore
    def decorator(func):
        # wraps обязательно используем для сохранения сигнатуры главной функции роутера
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # вытаскиваем наш ключ из генератора
            cache_key = cache_key_generator(func_name=func.__name__, *args, **kwargs)
            
            # отправляем запрос через клиента в redis на получение данных с ключа
            cache_json = await client.get(cache_key)
            
            # обязательно оборачиваем в try except, чтобы приложение не упало, если произойдёт ошибка чтения/записи кеша
            # лучше пользователь получит данные чуть медленнее, если попытка работы с кешем ляжет, чем всё приложение упадёт
            try:
                # проверяем на наличие данных под нужным нам ключом. Если есть, с джейсона парсим в объект python.
                if cache_json is not None:
                    cache_data = json.loads(cache_json)
                    
                    # модель всегда обязательна, но тут я указал себе для явности, может потом и уберу обязательное заполнение модели.
                    # проверяем на соответствие типов, если получили список словарей, проходимся по словарям циклом, валидируя в pydantic схему переданную в model
                    # если получули одиночный словарь, валидируем его сразу в pydantic схему
                    if model:
                        if isinstance(cache_data, list):
                            result = [model.model_validate(item) for item in cache_data]
                        elif isinstance(cache_data, dict):
                            result = model.model_validate(cache_data)
                            
                        # возвращаем результат из обёртки 
                        return result
                    
                    # если получили строку с Redis, возвращаем её без валидаций
                    return cache_data
            except Exception as e:
                # ловим ошибку, обязательно логгируем в консоль для себя
                print(f'Redus Error during GET!: {e}')
                
            # если cache_json = None, данных в кеше нет, идём в постгрес и вытаскиваем от туда
            data = await func(*args, **kwargs)
            
            # также оборачиваем в try except, для ловли ошибки записи, не роняя всё приложение целиком по той же логике ловли ошибки при чтении
            # мы параноики, проверям на != None
            try:
                if data is not None:
                    srlzble_data = data
                    
                    # окей мы не получили None,
                    # проверяем есть ли у полученных с постгреса данных метод model_dump
                    # если есть, значит получили одиночную модель, дампим в словарь
                    # теперь наша srtlzble_data это словарь, сможем легко запарсить в json и откинуть в Redis на запись
                    if hasattr(srlzble_data, 'model_dump'):
                        srlzble_data = srlzble_data.model_dump()
                    
                    # если первое условие не прошло, проверяем полученный объект на наличие атрибута __iter__, итерируемый ли он? 
                    # строки и словари тоже итерируемые, но они нам не нужны, поэтому через and ставим условие что полученные данные не являются строкой или словарём
                    elif hasattr(srlzble_data, '__iter__') and not isinstance(srlzble_data, (str, dict)):
                        # проходимся циклом по моделям в нашем объекте и наш srzble_data и дампим их в словари, теперь srzble_data это список словарей, его легко запарсить в json и откинуть в Redis на запись
                        srlzble_data = [
                            item.model_dump() if hasattr(item, 'model_dump') else item
                            for item in srlzble_data
                        ]
                    
                    # записываем полученные данные в redis, ОБЯЗАТЕЛЬНО указываем expire.
                    # если вы забудете указать expire, ваш ключ будет жить в redis вечно и никогда не 'протухнет' и не удалится автоматически
                    # сервер упадёт, когда огромная база редиса состоящая из таких бессмертных ключей забьёт всю оперативу сервера.
                    # обязательно указываем ex 
                    # но у нас в expire стоит дефолтное 60, если забудем указать в роутере, то применится 60.
                    # дефолт в expire у нас, это защита от bloat нашего редиса от потенциальных ошибок разработчика.
                    await client.set(
                        cache_key,
                        json.dumps(srlzble_data, default=json_serial),
                        ex = expire
                    )
            # если получили ошибку, ловим её, выводим в консоль, и даём возможность приложению работать дальше       
            except Exception as e:
                print(f'Redis during SET!: {e}')
            
            # возвращаем всё
            return data
        return wrapper
    return decorator
            
            