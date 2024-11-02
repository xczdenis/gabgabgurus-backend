<a href="https://www.djangoproject.com" target="_blank">
    <img src="https://img.shields.io/static/v1?label=Django&message=5%2B&color=brightgreen&style=flat&logo=django" alt="Django">
</a>

<a href="https://www.django-rest-framework.org/" target="_blank">
    <img src="https://img.shields.io/static/v1?label=DRF&message=3%2B&style=flat&logo=django" alt="Django">
</a>

<a href="https://ru.wikipedia.org/wiki/OAuth" target="_blank">
    <img src="https://img.shields.io/static/v1?label=OAuth&message=2.0&color=%23EB5424&style=flat&logo=auth0" alt="OAuth2.0">
</a>

<a href="https://github.com/django/channels" target="_blank">
    <img src="https://img.shields.io/static/v1?label=ASGI(channels)&message=4%2B&color=%2343B1B0&style=flat&logo=redis" alt="Redis">
</a>

<a href="https://swagger.io/" target="_blank">
    <img src="https://img.shields.io/static/v1?label=Swagger&message=3&color=%2385EA2D&style=flat&logo=swagger" alt="Django">
</a>

<a href="https://www.postgresql.org/" target="_blank">
    <img src="https://img.shields.io/static/v1?label=Postgre&message=16%2B&color=%234169E1&style=flat&logo=postgresql" alt="PostgreSQL">
</a>

<a href="https://redis.io/" target="_blank">
    <img src="https://img.shields.io/static/v1?label=Redis&message=7%2B&color=%23D82C20&style=flat&logo=redis" alt="Redis">
</a>
<a href="https://www.docker.com/" target="_blank">
    <img src="https://img.shields.io/static/v1?label=Docker&message=23&color=%232496ED&style=flat&logo=docker" alt="Docker">
</a>
<a href="#">
    <img src="https://img.shields.io/static/v1?label=python&message=3.12^&color=%233674a8&style=flat&logo=python" alt="Supported Python versions">
</a>
<a href="https://black.readthedocs.io/en/stable/">
    <img src="https://img.shields.io/static/v1?label=style&message=black&color=black&style=flat&logo=python" alt="Supported Python versions">
</a>

# GabGabGurus (backend)

<ul>
    <li>
        <a target="_blank" href="https://gabgabgurus.ru/" >GabGabGurus.ru</a> - веб сайт
    </li>
    <li>
        <a href="https://gabgabgurus.ru/api/openapi/swagger/?version=v1" target="_blank">OpnAPI Swagger</a> - API в интерфейсе swagger
    </li>
    <li>
        <a href="https://gabgabgurus.ru/api/openapi/redoc/?version=v1" target="_blank">OpnAPI Redoc</a> - API в интерфейсе redoc
    </li>
    <li>
        <a href="https://github.com/xczdenis/gabgabgurus-frontend" target="_blank">GabGabGurus (frontend)</a> - фронтенд на NextJS (React)
    </li>
    <li>
        <a href="https://github.com/xczdenis/gabgabgurus-backend" target="_blank">GabGabGurus (backend)</a> - backend на Django+DRF
    </li>
</ul>

[GabGabGurus.ru](https://gabgabgurus.ru/) - это сервис для поиска собеседников для практики иностранных языков. Здесь можно найти носителя языка по общим увлечениям и практиковаться в свободной речи или переписке. Проект создан с использованием таких технологий, как Django, Django Rest Framework (DRF), ASGI (channels), OpenAPI (swagger), PostgreSQL, Redis и Docker, что обеспечивает высокую производительность, надежность и масштабируемость.

Полностью в докере с удобными sh скриптами для инициализации, линтинга, форматинга, а также набор коротких и часто используемых команд в Makefile.

## 📖 Содержание

- [✨ Особенности](#-Особенности-)
- [✅ Функционал сервиса](#-Функционал-сервиса-)
    - [🌐 REST API](#-REST-API-)
    - [🔐 Авторизация OAuth2](#-Авторизация-OAuth2-)
    - [💬 WebSocket API](#-WebSocket-API-)
- [🚀 Быстрый старт](#-Быстрый-старт-)
    - [⚙️ Настройка переменных окружения](#%EF%B8%8F-настройка-переменных-окружения-)
    - [🏁 Запуск](#-Запуск-)
- [💻 Режим разработки](#-Режим-разработки-)
    - [📋 Pre requirements](#-pre-requirements-)
    - [🌐 Создание среды разработки](#-Создание-среды-разработки-)
    - [📚 Установить Poetry](#-Установить-Poetry-)
    - [🐳 Подробнее про Docker](#-Подробнее-про-Docker-)
    - [🔄 Окружения dev и prod](#-Окружения-dev-и-prod-)
    - [📜 Один Dockerfile для двух окружений](#-Один-Dockerfile-для-двух-окружений-)
- [🚀 Запуск проекта](#-Запуск-проекта-)
    - [👨‍💼 Запуск приложения App в докере](#-Запуск-приложения-App-в-докере-)
    - [🔧 Полезные команды](#-Полезные-команды-)
- [📝 Особенности разработки](#-Особенности-разработки-)
    - [🔗 Управление зависимостями](#-Управление-зависимостями-)
    - [📝 Conventional Commits](#-conventional-commits-)
    - [🖥️ Настройки IDE](#%EF%B8%8F-настройки-ide-)
    - [🖊️ Форматер и линтер](#%EF%B8%8F-форматер-и-линтер-)

## ✨ Особенности [🔝](#-содержание)

* **Python 3.12+**;
* **RESTFull API**:
    * Django 5;
    * Django Rest Framework;
    * ASGI: Django channels + Websockets + Daphne;
    * Самодокументируемое API: Swagger и Redoc;
    * Удобные настройки с [django-split-settings](https://github.com/wemake-services/django-split-settings);
* Полная **Docker** интеграция:
    * тонкие образы - **multi-stage сборка**;
    * **docker-compose** для локальной разработки;
* **OAuth2** + **JWT** авторизация;
* **CI/CD** - workflow для GitHub Actions от линтинга до деплоя на удаленном сервере;
* **SOLID** код;
* [src-шаблон](https://blog.ionelmc.ro/2014/05/25/python-packaging/) - отдельный пакет для сервиса;
* Удобные **sh** скрипты:
    * [init.sh](src%2Fscripts%2Finit.sh) (`make init`) - инициализация проекта;
    * [lint.sh](src%2Fscripts%2Flint.sh) (`make lint`) - линтинг (`black`, `flake8`, `isort`, `autoflake`);
    * [format.sh](src%2Fscripts%2Fformat.sh) (`make format`) - форматирование;
* [Pre-commit](https://pre-commit.com/) хуки, чтобы код всегда был в отличном состоянии;
* [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) - строгое соблюдение правил написания коммитов;
* **Makefile** для удобного запуска команд;

## ✅ Функционал сервиса [🔝](#-содержание)

### 🌐 REST API [🔝](#-Функционал-сервиса-)

Gabgabgurus (backend) предоставляет API в архитектуре REST для управления данными. Сервис использует версионированное, самодокументируемое API.

Схема в формате Swagger доступна здесь: [https://gabgabgurus.ru/api/openapi/swagger/?version=v1](https://gabgabgurus.ru/api/openapi/swagger/?version=v1)
![swagger.png](docs%2Fassets%2Fimg%2Fservice%2Fswagger.png)

Схема в формате Redoc доступна здесь: [https://gabgabgurus.ru/api/openapi/redoc/?version=v1](https://gabgabgurus.ru/api/openapi/redoc/?version=v1)
![redoc.png](docs%2Fassets%2Fimg%2Fservice%2Fredoc.png)

### 🔐 Авторизация OAuth2 [🔝](#-Функционал-сервиса-)

Сервис предоставляет возможность авторизации пользователей с помощью социальных сетей по протоколу OAuth2.

#### Как работает OAuth2 [🔝](#-Авторизация-OAuth2-)

Последовательность действий при регистрации пользователя с помощью социальной сети следующая:

1. **Получить авторизационный URL**
   Сначала нужно получить авторизационный URL - это адрес провайдера социальной сети, на который необходимо перенаправить пользователя. Пользователю будет открыто окно провайдера с запросом на предоставление доступа к своим учетным данным. Если пользователь еще не залогинен у провайдера, то ему будет предложено ввести логин и пароль. Чтобы получить авторизационный URL, нужно отправить GET запрос на адрес
   `api/v1/oauth/<provider-name>/`. Запрос возвращает строку - авторизационный URL провайдера;
2. **Перенаправить пользователя на авторизационный URL**
   Далее клиенту нужно перенаправить пользователя на полученный авторизационный URL. Пользователь должен подтвердить доступ к его аккаунту. Доступ предоставляется на чтение имени и email. Как только пользователь подтверждает доступ, провайдер сгенерирует для него авторизационный код, который нужно будет обменять на токены авторизации, а затем перенаправляет на `redirect_url`;
3. **Обменять авторизационный код на токены**
   Клиентское приложение должно принять запрос от провайдера, поступивший на `redirect_url`. Этот запрос будет содержать в параметрах авторизационный код и дополнительную информацию, такую как `state`. Клиентское приложение должно получить из запроса все параметры, включая код авторизации и отправить POST запрос на адрес `api/v1/oauth/signin/`;
4. **Бэкенд формирует токены авторизации**
   Бэкенд проверяет входящие данные и в случае успешной проверки формирует свои собственные `access`
   и `refresh` токены авторизации для сервиса gabgabgurus. Затем бэкенд возвращает эти токены клиенту в заголовках `set-cookie` с параметрами `http-only` и `secure`. Клиенту не требуется заботиться о хранении токенов поскольку они автоматически будет отправляться с каждым следующим запросом на бэкенд. Также эти токены нельзя будет получить, используя JS поскольку они имеют параметр `http-only` и не будут доступны на клиенте.

#### Схема работы OAuth2 [🔝](#-Авторизация-OAuth2-)

``` mermaid
sequenceDiagram
  participant W as Web-app
  participant B as Backend
  participant G as GitHub
  autonumber
  Note left of W: Войти с GitHub
  W->>B: GET /authorize-url
  B->>W: `authorize_url`
  W->>G: Направить пользователя на `authorize_url`
  Note right of G: Подтверждение доступа
  G->>B: code
  B->>W: code
  W->>B: POST /sign-in
  B->>W: access_token
```

### 💬 WebSocket API [🔝](#-Функционал-сервиса-)

#### Общее описание [🔝](#-WebSocket-API-)

GabGabGurus предоставляет асинхронное API для возможности обмена мгновенными сообщениями, используя протокол WebSocket.

Сервис предоставляет 2 websocket канала:

1. **chat**: канал для обмена сообщениями в чате;
2. **notifications**: канал для мгновенных уведомлений;

Для подключения к websocket используется адрес `wss://gabgabgurus.ru/ws/api/v1`.

#### Особенности реализации (SOLID) [🔝](#-WebSocket-API-)

Каждое websocket сообщение имеет свой тип. Рассмотрим типы сообщений для канала `chat`:

```python
class ChatMessageTypes(str, Enum):
    MESSAGE = "message"
    MARK_AS_READ_MESSAGE = "mark_as_read"
    USER_JOINED = "user_joined"
    USER_BLOCKING = "user_blocking"
```

Для каждого типа сообщения, может потребоваться своя, особенная логика обработки. Рассмотрим как это реализовано.

Есть базовый класс `ChatConsumerMessageHandler`, который содержит обязательную для реализации функцию `handle_message`:

```python
# src/gabgabgurus/api/v1/chats/handlers.py

class ChatConsumerMessageHandler(AsyncSerializerMixin):
    def __init__(self, consumer):
        self.consumer = consumer

    async def handle_message(self, content):
        raise NotImplementedError("Method must be implemented by subclass")
```

Для каждого типа сообщения, есть свой собственный обработчик, который наследуется от класса `ChatConsumerMessageHandler`:

```python
# src/gabgabgurus/api/v1/chats/handlers.py

class CreateMessageHandler(ChatConsumerMessageHandler):
    serializer_class = MessageRequest
    output_serializer_class = MessageResponse

    async def handle_message(self, content):
        self.very_comlicated_algorithm()


class UserBlockingHandler(ChatConsumerMessageHandler):
    serializer_class = MarkMessagesAsReadRequest

    async def handle_message(self, content):
        self.do_smth()


class MarkAsRedMessageHandler(ChatConsumerMessageHandler):
    async def handle_message(self, content):
        self.very_simple_algorithm()
```

Фабрика `ChatMessageHandlerFactory` формирует нужный обработчик в зависимости от типа сообщения:

```python
# src/gabgabgurus/api/v1/chats/factories.py

@dataclass(slots=True, frozen=True)
class ChatMessageHandlerFactory:
    handlers = {
        ChatMessageTypes.MESSAGE: CreateMessageHandler,
        ChatMessageTypes.USER_BLOCKING: UserBlockingHandler,
        ChatMessageTypes.MARK_AS_READ_MESSAGE: MarkAsRedMessageHandler,
    }

    @classmethod
    def get_handler(cls, consumer, message_type):
        handler_class = cls.handlers.get(message_type)
        if handler_class:
            return handler_class(consumer=consumer)

        return None
```

Потребитель (consumer) использует фабрику для получения обработчика по типу сообщения и выполняет функцию `handle_message`:

```python
# src/gabgabgurus/api/v1/chats/consumers.py

from gabgabgurus.api.v1.chats.factories import ChatMessageHandlerFactory


@async_exception_handling()
class ChatConsumer(GroupWebsocketConsumerMixin, AsyncJsonWebsocketConsumer):
    async def receive_json(self, content, **kwargs):
        handler = await self.get_message_handler(content)
        if handler:
            await handler.handle_message(content)

    async def get_message_handler(self, content):
        client_message_type = await self.get_client_message_type(content)
        return ChatMessageHandlerFactory.get_handler(self, client_message_type)
```

## 🚀 Быстрый старт [🔝](#-содержание)

Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта, если иное не указано в описании конкретной команды.

### ⚙️ Настройка переменных окружения [🔝](#-Быстрый-старт-)

Перед стартом, нужно создать файл `.env` в корне проекта. Это можно сделать, выполнив команду:

```bash
make env
```

Можно просто скопировать файл `env.example`.

### 🏁 Запуск [🔝](#-Быстрый-старт-)

🚨 Убедись, что у тебя свободны все порты, указанные в настройках, оканчивающихся на `PORT` в файле `.env`.

🚨 Укажи свою платформу для docker образов в настройке `DOCKER_IMG_PLATFORM` в файле `.env`. Например, для Mac на M1 вот так:

```bash
DOCKER_IMG_PLATFORM=linux/arm64
```

Для Linux вот так:

```bash
DOCKER_IMG_PLATFORM=linux/amd64
```

Запустить проект в докере:

```bash
make run
```

Будут доступны следующие URL:

* приложение: [http://127.0.0.1:8000](http://127.0.0.1:8000);
* админка: [http://127.0.0.1:8000/api/admin](http://127.0.0.1:8000/api/admin). Суперюзер создается автоматически при старте приложения в докере, учетные данные см. в настройках `SUPERUSER_EMAIL`
  и `SUPERUSER_PASSWORD` в файле `.env`.;
* swagger: [http://127.0.0.1:8000/api/openapi/swagger/?version=v1](http://127.0.0. 1:
  8000/api/openapi/swagger/?version=v1);
*

redoc: [http://127.0.0.1:8000/api/openapi/redoc/?version=v1](http://127.0.0.1:8000/api/openapi/redoc/?version=v1)

Остановить и удалить все запущенные контейнеры:

```bash
make down
```

## 💻 Режим разработки [🔝](#-содержание)

### 📚 Pre requirements [🔝](#-Режим-разработки-)

Для успешного развертывания среды разработки понадобится:

1. Python ^3.12;
2. `postgresql` на локальной машине;
3. Менеджер пакетов [Poetry](https://python-poetry.org/docs/#installation);
4. Docker (version ^23.0.5). Если у тебя его еще нет, следуй [инструкциям по установке](https://docs.docker.com/get-docker/);
5. Docker compose (version ^2.17.3). Обратись к официальной документации [для установки](https://docs.docker.com/compose/install/);
6. [Pre-commit](https://pre-commit.com/#install).

### 🌐 Создание среды разработки [🔝](#-Режим-разработки-)

#### Важно: подготовка

Перед выполнением команд из этого раздела, убедись, что у тебя установлены все компоненты [Pre requirements](#Pre-requirements-), в противном случае, смотри инструкции по установке в подразделах ниже.

**ВАЖНО:
** проект включает зависимость `psycopg2-binary`. Эта библиотека может быть установлена только в том случае, если на хост машине установлена `postgresql` и прописан путь к `pg_config`.

Если `postgresql` не установлена или путь к `pg_config` не прописан, то установка зависимостей через
`poetry install` завершится подобной ошибкой:

```
❯ poetry add psycopg2-binary
Using version ^2.9.9 for psycopg2-binary

Updating dependencies
Resolving dependencies... (0.3s)

Package operations: 1 install, 0 updates, 0 removals

  • Installing psycopg2-binary (2.9.9): Failed

  ChefBuildError

  Backend subprocess exited when trying to invoke get_requires_for_build_wheel

  running egg_info
  writing psycopg2_binary.egg-info/PKG-INFO
  writing dependency_links to psycopg2_binary.egg-info/dependency_links.txt
  writing top-level names to psycopg2_binary.egg-info/top_level.txt

  Error: pg_config executable not found.

  pg_config is required to build psycopg2 from source.  Please add the directory
  containing pg_config to the $PATH or specify the full executable path with the
  option:

      python setup.py build_ext --pg-config /path/to/pg_config build ...

  or with the pg_config option in 'setup.cfg'.

  If you prefer to avoid building psycopg2 from source, please install the PyPI
  'psycopg2-binary' package instead.

  For further information please check the 'doc/src/install.rst' file (also at
  <https://www.psycopg.org/docs/install.html>).



  at ~/Library/Application Support/pypoetry/venv/lib/python3.10/site-packages/poetry/installation/chef.py:166 in _prepare
      162│
      163│                 error = ChefBuildError("\n\n".join(message_parts))
      164│
      165│             if error is not None:
    → 166│                 raise error from None
      167│
      168│             return path
      169│
      170│     def _prepare_sdist(self, archive: Path, destination: Path | None = None) -> Path:

Note: This error originates from the build backend, and is likely not a problem with poetry but with psycopg2-binary (2.9.9) not supporting PEP 517 builds. You can verify this by running 'pip wheel --no-cache-dir --use-pep517 "psycopg2-binary (==2.9.9)"'.
```

Убедиться что `postgresql` установлена:

```bash
postgres --version
```

Результат выполнения команды должен показать версию `postgresql`:

```
postgres (PostgreSQL) 14.10 (Homebrew)
```

Если `postgresql` не установлена, то нужно установить:

```bash
brew install postgresql
```

Если `postgresql` установлена, то нужно убедиться, что `pg_config` находится в вашем `PATH`:

```bash
which pg_config
```

Если команда не возвращает путь, вам нужно добавить директорию, содержащую `pg_config`, в ваш `PATH`. Это обычно `/usr/local/bin` или `/usr/bin`.

После этого библиотека `psycopg2-binary` установится без ошибок.

#### Инициализация проекта

Для создания среды разработки, выполни следующие команды одну за другой, из корневой директории проекта:

```bash
make env
poetry shell
make init
```

Те же команды без `Makefile`:

```bash
cp .env.template .env
poetry shell
poetry install
pre-commit install
pre-commit install --hook-type commit-msg
```

### 📖 Установить Poetry [🔝](#-Режим-разработки-)

Подробнее про установку Poetry [здесь](https://python-poetry.org/docs/#installation).

**Linux, macOS, Windows (WSL)**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Важно:
** после установки, необходимо добавить путь к Poetry в свой `PATH`. Как правило, это делается автоматически. Подробнее смотри в разделе [Add Poetry to your PATH](https://python-poetry.org/docs/#installation).

Проверить, что Poetry установлен корректно:

```bash
poetry --version

# Poetry (version 1.5.0)
```

### 🐳 Подробнее про Docker [🔝](#-Режим-разработки-)

Проект полностью интегрирован в `docker`. Для оркестрации используется `docker-compose`. Проект содержит следующие файлы docker-compose:

* **docker-compose.yml** - главный файл;
* **docker-compose.dev.yml** - содержит
  ***только изменения*** относительно главного файла, необходимые для режима разработки;
* **docker-compose.prod.yml** - содержит
  ***только изменения*** относительно главного файла, необходимые для режима `production`;

#### Файл docker-compose.yml [🔝](#-Подробнее-про-Docker-)

Файл `docker-compose.yml` - это главный compose-файл. Любая команда `docker-compose` должна использовать этот файл в качестве первого аргумента.

Файл содержит все сервисы проекта и основные метаданные для каждого сервиса, такие как `build`, `env_file`,
`depends_on` и т.п.

Файл `docker-compose.yml` **не должен** содержать портов, смотрящих наружу для сервисов баз данных.

#### Профили [🔝](#-Подробнее-про-Docker-)

Все сервисы в файле `docker-compose.yml` сгруппированы по профилям. Профили необходимы для возможности запуска только определенной группы сервисов.

Главный профиль - `default`, все сервисы должны иметь этот профиль.

Существуют следующие профили:

* `default`
* `db`

Например, к профилю `db` относятся только `postgres` и `redis` и больше ничего. Это нужно для возможности локального запуска приложения. Запустить исключительно сервисы профайла `db` можно так:

```bash
make run-db
```

#### Файл docker-compose.dev.yml [🔝](#-Подробнее-про-Docker-)

Файл `docker-compose.dev.yml` используется для запуска проекта в режиме разработки. Здесь добавляются изменения относительно `docker-compose.yml`. Например, здесь можно примонтировать тома для папок приложения и указать порты, смотрящие наружу, чтобы облегчить отладку.

### 🔄 Окружения dev и prod [🔝](#-Режим-разработки-)

Основной тип запуска проекта - через docker-compose. Запуск проекта может быть выполнен в одном из двух окружений: `development` или `production`. Окружение управляется настройкой `ENVIRONMENT` в файле [.env](.env):

```bash
ENVIRONMENT=development
```

Если настройка `ENVIRONMENT` имеет значение `production`, то при запуске используется файл
[docker-compose.yml](docker-compose.yml). Если настройка `ENVIRONMENT` имеет значение `development`, то при запуске используется дополнительный файл [docker-compose.dev.yml](docker-compose.dev.yml).

При запуске в режиме `development` папка приложения [src](src) монтируется как том, а каждый сервис имеет `expose` порты:

```dockerfile
    postgres:
        <<: *base-dev-service
        ports:
            - ${POSTGRES_PORT}:5432

    redis:
        <<: *base-dev-service
        ports:
            - ${REDIS_PORT}:6379
```

### 📜 Один Dockerfile для двух окружений [🔝](#-Режим-разработки-)

Стоит обратить внимание на [Dockerfile](deploy%2Fapp%2FDockerfile) для самого приложения `App`. Помимо `multistage` сборки, данный файл использует слои `development` и `production` в соответствии с настройкой `ENVIRONMENT`:

```dockerfile
# ./deploy/app/Dockerfile
ARG env=production
...

FROM final as development


FROM final as production

COPY ./src/${pck_name} ./src/${pck_name}


FROM ${env}

ENTRYPOINT ["./scripts/entrypoint.sh"]
```

Данная конфигурация позволяет использовать разные итоговые образы в зависимости от режима запуска. При запуске в режиме `development` папка приложения [src](src) монтируется как том в файле [docker-compose.dev.yml](docker-compose.dev.yml), поэтому слой `development` в `Dockerfile` пустой:

```dockerfile
# ./deploy/app/Dockerfile
...

FROM final as development

...
```

При запуске в окружении `production` папка приложения [src](src) копируется с помощью инструкции `COPY`:

```dockerfile
# ./deploy/app/Dockerfile
...

FROM final as production

COPY ./src/${pck_name} ./src/${pck_name}
```

В конце файла, выбирается образ из переменной `env`:

```dockerfile
# ./docker/python/Dockerfile
ARG env=production
...

FROM ${env}
```

Переменная `env` в свою очередь передается как аргумент сборки при этом монтируется том `src`:

```dockerfile
# ./docker-compose.dev.yml
services:
    app:
        <<: *base-dev-service
        build:
            context: .
            dockerfile: deploy/app/Dockerfile
            args:
                env: ${ENVIRONMENT}
                img: ${PYTHON_IMG}
        volumes:
            - ./src/gabgabgurus:/app/src/gabgabgurus
```

Итоговый образ будет использовать самый последний слой. Таким образом, если настройка `ENVIRONMENT` имеет значение `development`, то будет использован образ `development`, а если `production`, то `production`.

## 🚀 Запуск проекта [🔝](#-содержание)

### 👨‍💼 Запуск приложения App в докере [🔝](#-Запуск-проекта-)

Запустить все сервисы проекта:

```bash
make run
```

Будут доступны следующие URL:

* приложение: [http://127.0.0.1:8000](http://127.0.0.1:8000);
* админка: [http://127.0.0.1:8000/api/admin](http://127.0.0.1:8000/api/admin). Суперюзер создается автоматически при старте приложения в докере, учетные данные см. в настройках `SUPERUSER_EMAIL` и `SUPERUSER_PASSWORD` в файле `.env`.;
* swagger: [http://127.0.0.1:8000/api/openapi/swagger/?version=v1](http://127.0.0.1:8000/api/openapi/swagger/?version=v1);

redoc: [http://127.0.0.1:8000/api/openapi/redoc/?version=v1](http://127.0.0.1:8000/api/openapi/redoc/?version=v1)

Команда `make run` автоматически определяет режим запуска из настройки `ENVIRONMENT`.

Посмотреть все, что касается docker - запущенные сервисы, тома, образы, сети:

```bash
make di
```

Нативная команда для запуска в окружении `development`:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile default up -d --build
```

Нативная команда для запуска в окружении `production`:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml --profile default up -d --build
```

При запуске в докере, автоматически запускаются миграции базы данных, база заполняется предопределенными
данными из каталога [init_data](src%2Fgabgabgurus%2Finit_data), а также создается суперюзер по настройкам из файла [.env](.env):

```bash
SUPERUSER_LOGIN=admin
SUPERUSER_EMAIL=admin@admin.com
SUPERUSER_PASSWORD=123qwe
```

Для локального запуска нужно сначала запустить сервисы профиля `db`:

```bash
make run-db
```

Создать миграции:

```bash
make makemigrations
```

Применить миграции:

```bash
make migrate
```

Одна общая команда для создания и применения миграций:

```bash
make db-update
```

Нативные команды можно посмотреть в [Makefile](Makefile). Например, нативная команда для создания миграций:

```bash
python src/gabgabgurus/manage.py makemigrations
```

Создать суперюзера:

```bash
make su
```

Запустить сервис локально:

```bash
make serve
```

### 🔧 Полезные команды [🔝](#-Запуск-проекта-)

Запустить несколько определенных сервисов:

```bash
make run s="postgres redis"
```

Зайти внутрь контейнера:

```bash
make bash s=app
```

Также есть команда sh:

```bash
make sh s=app
```

Чтобы выйти, нужно выполнить команду `exit`.

Вывести логи сервиса:

```bash
make logs s=redis
```

Остановить все сервисы и удалить контейнеры:

```bash
make down
```

Посмотреть текущий конфиг `docker-compose`:

```bash
make config
```

Удалить все неиспользуемые образы, контейнеры и тома:

```bash
make remove
```

## 📝 Особенности разработки [🔝](#-содержание)

При разработке необходимо придерживаться установленных правил оформления кода. В этом разделе ты найдешь описание настроек редактора кода, линтеры и форматеры, используемые в проекте, а также другие особенности, которые необходимо учитывать при разработке.

### 🔗 Управление зависимостями [🔝](#-Особенности-разработки-)

В качестве пакетного менеджера используется [Poetry](https://python-poetry.org/docs/#installation). Для управления зависимостями используются группы (см. файл `pyproject.toml`).

🚨 Важно: каждая зависимость должна принадлежать **только одной
** группе. Нельзя добавлять одну и ту же зависимость в разные группы.

Если одна зависимость используется для различных сервисов, то она добавляется в дефолтную группу
`tool.poetry.dependencies`.

Все основные зависимости располагаются в дефолтной группе `tool.poetry.dependencies`:

```
[tool.poetry.dependencies]
python = "^3.12"
pydantic = "^1.10.2"
backoff = "^2.2.1"
```

Добавление основной зависимости:

```bash
poetry add pendulum
```

Остальные зависимости делятся на группы. Например, группа `dev` - зависимости, которые используются только при разработке, а в проде они не нужны:

```toml
[tool.poetry.group.dev.dependencies]
isort = "^5.12.0"
pre-commit = "^3.3.3"
black = "^23.9.1"
```

Добавление общей зависимости:

```bash
poetry add django
```

Добавление зависимости в конкретную группу (используй флаг `--group` и название группы):

```bash
poetry add pytest --group=test
```

Разделение зависимостей на группы позволяет уменьшить размер докер образов, так как в образы устанавливаются только необходимые зависимости. Например, в итоговый образ приложения будут установлены только зависимости главной группы:

```dockerfile
# ./deploy/app/Dockerfile
...

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main
```

### 📝 Conventional Commits [🔝](#-Особенности-разработки-)

Твои комментарии к коммитам должны соответствовать [Conventional Commits](https://www.conventionalcommits.org/). Pre-commit хук `conventional-pre-commit` выполнит проверку комментария перед коммитом.

Если твой комментарий не соответствует конвенции, то в терминале ты увидишь подобное сообщение:

```bash
commitizen check.........................................................Failed
- hook id: commitizen
- exit code: 14
commit validation: failed!
please enter a commit message in the commitizen format.
```

Для более удобного написания комментариев к коммитам, ты можешь воспользоваться плагином Conventional Commit для PyCharm.

### 🖥️ Настройки IDE [🔝](#-Особенности-разработки-)

Проект содержит файл `.editorconfig` - ознакомься с ним, чтобы узнать какие настройки должны быть в твоем редакторе.

Основное:

* максимальная длина строки: 110;
* отступы: пробелы;
* количество отступов: 4.

### 🖊️ Форматер и линтер [🔝](#-Особенности-разработки-)

В качестве форматера мы используем [black](https://github.com/psf/black). Конфиг black см. в файле `pyproject.toml` в секции `[tool.black]`.

Линтер - flake8, конфиг находится в файле `setup.cfg`.

Если ты используешь PyCharm, то можешь настроить форматирование файла с помощью black через External Tools.
