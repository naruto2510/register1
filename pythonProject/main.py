import asyncio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

# Словарь для хранения чатов: {название_чата: {messages: [], users: {}}}
chats = {
    "Основной": {
        "messages": [],
        "users": {},
        "avatar": "💬"  # Эмодзи для чата
    }
}
current_chat = "Основной"  # Текущий выбранный чат
MAX_MESSAGES_COUNT = 100

# Стикеры и GIF-изображения
STICKERS = {
    "Радость": ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😊", "😋"],
    "Любовь": ["😍", "🥰", "😘", "😗", "😙", "😚", "😻", "💋", "❤️", "🧡"],
    "Животные": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯"],
    "Еда": ["🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈"],
    "Праздники": ["🎄", "🎅", "🤶", "🎁", "🎀", "🎊", "🎉", "🎈", "🧨", "✨"]
}

GIFS = {
    "Реакции": [
        {"url": "", "name": "крутится кот"},
        {"url": "https://media.giphy.com/media/l0HU20BZ6LbSEITza/giphy.gif", "name": "Джон Траволта в замешательстве"},
        {"url": "https://media.giphy.com/media/l0HU3q4F4lUDH4uWI/giphy.gif", "name": "Пожатие плечами"},
        {"url": "https://media.giphy.com/media/l0HU8JgS5hHzl8eWA/giphy.gif", "name": "Подмигивание"},
        {"url": "https://media.giphy.com/media/l0HlHFRbmaZtBRhXG/giphy.gif", "name": "Лицо ладошкой"},
        {"url": "https://media.giphy.com/media/l0HU3sZ4xQMWatm2A/giphy.gif", "name": "Качание головой"},
        {"url": "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", "name": "Овации"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Сюрприз"},
        {"url": "https://media.giphy.com/media/l0HU7JI1nz6ZyxQh2/giphy.gif", "name": "Одобрение"},
        {"url": "https://media.giphy.com/media/26n6WywJyh39n1pBu/giphy.gif", "name": "Смеющийся ребенок"}
    ],
    "Животные": [
        {"url": "https://steamuserimages-a.akamaihd.net/ugc/2259182745984152155/2F5A9F49F850C7AB253349B25379472AA94B2070/?imw=630&imh=574&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true", "name": "кот лизун"},
        {"url": "https://steamuserimages-a.akamaihd.net/ugc/2017092157679577267/05608485BC865DF2804E337389228AF816BB8A38/", "name": "крутится кот"},
        {"url": "https://static.wikia.nocookie.net/553fa922-0495-468b-9702-d8eca3252cf0/scale-to-width/755", "name": "Прыгающий пёс"},
        {"url": "https://steamuserimages-a.akamaihd.net/ugc/773972553887350897/907EBE3A7DD84ED1957DD2551F14EFEE357CC4E4/?imw=512&amp;imh=384&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true", "name": "танец лягушки"},
        {"url": "https://media.giphy.com/media/jpbnoe3UIa8TU8LM13/giphy.gif", "name": "Кот в очках"},
        {"url": "https://media.giphy.com/media/3o7TKUM3IgJBX2as9O/giphy.gif", "name": "Морская выдра плавает"},
        {"url": "https://media.giphy.com/media/3o7TKSha51ATTx9KzC/giphy.gif", "name": "Панда катается"},
        {"url": "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif", "name": "Хамелеон меняет цвет"},
        {"url": "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif", "name": "Сова вращает головой"},
        {"url": "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif", "name": "Енот моет еду"}
    ],
    "мемы": [
        {"url": "https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/80079b14e7d5a22469ec2e9e54e4894442cfc11a62d03976ae36d1f95c7b5468.gif", "name": "бухаем"},
        {"url": "https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/e0175a03105b229842238291fb1848b4e77514cbe40ea22026d774617ca2fe8f.webp", "name": "бесконечный патрик"},
        {"url": "https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif", "name": "Успешный парень из мема"},
        {"url": "https://lastfm.freetls.fastly.net/i/u/ar0/551709f573794970c9ad3b8affe6aa23.gif", "name": "троль за компом"},
        {"url": "https://i.postimg.cc/T3Ztpw1b/37606475-21c5bcbd92f5a64cbd793ba5be8da67e-800.gif", "name": "ну что?"},
        {"url": "https://static.wikia.nocookie.net/f71b838b-d5c8-4a27-8f46-4a18f46a231a/scale-to-width/755", "name": "что?"},
        {"url": "https://media1.tenor.com/m/6rTPusi4YJcAAAAd/sigma-sigma-male.gif", "name": "сигма"},
        {"url": "https://i.yapx.cc/VakAN.gif", "name": "тап-тап"},
        {"url": "https://i.pinimg.com/originals/bf/fa/02/bffa02575da14a5784e9dd2bcba62fc8.gif", "name": "конь в пальто"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Фродо (Властелин колец)"}
    ],
    "Спорт": [
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Футбольный гол"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Баскетбольное попадание"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Теннисная подача"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Боксерский нокаут"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Пловец"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Гимнастическое сальто"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Спринтер бежит"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Велоспорт"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Лыжник"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Сноубордист"}
    ],
    "Еда": [
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Вращающаяся пицца"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Готовящийся бургер"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Суши шеф-повара"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Тающее мороженое"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Льющийся шоколад"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Наливаемый кофе"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Завариваемый чай"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Пончик с посыпкой"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Разрезаемый торт"},
        {"url": "https://media.giphy.com/media/3o7TKsQ8XJnwjXoVHi/giphy.gif", "name": "Свежие фрукты"}
    ]
}


# Увеличенный список доступных аватарок (эмодзи)
AVATARS = [
    "👨", "👩", "👦", "👧", "👶", "👨‍⚕️", "👩‍⚕️", "👨‍🎓", "👩‍🎓",
    "👨‍🏫", "👩‍🏫", "👨‍⚖️", "👩‍⚖️", "👨‍🌾", "👩‍🌾", "👨‍🍳", "👩‍🍳",
    "👨‍🔧", "👩‍🔧", "👨‍🏭", "👩‍🏭", "👨‍💼", "👩‍💼", "👨‍🔬", "👩‍🔬",
    "👨‍💻", "👩‍💻", "👨‍🎤", "👩‍🎤", "👨‍🎨", "👩‍🎨", "👨‍✈️", "👩‍✈️",
    "👨‍🚀", "👩‍🚀", "👨‍🚒", "👩‍🚒", "👮", "👮‍♂️", "👮‍♀️", "🕵️", "🕵️‍♂️", "🕵️‍♀️",
    "🧙", "🧙‍♂️", "🧙‍♀️", "🧚", "🧚‍♂️", "🧚‍♀️", "🧛", "🧛‍♂️", "🧛‍♀️",
    "🧜", "🧜‍♂️", "🧜‍♀️", "🧝", "🧝‍♂️", "🧝‍♀️", "🧞", "🧞‍♂️", "🧞‍♀️",
    "🧟", "🧟‍♂️", "🧟‍♀️", "👹", "👺", "🤡", "👻", "👽", "🤖",
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯",
    "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🦆",
    "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋",
    "🐌", "🐞", "🐜", "🦟", "🦗", "🕷️", "🦂", "🐢", "🐍", "🦎",
    "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟",
    "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧",
    "🎃", "🎄", "🎆", "🎇", "🧨", "✨", "🎈", "🎉", "🎊", "🎋",
    "🎍", "🎎", "🎏", "🎐", "🎑", "🧧", "🎀", "🎁", "🎗️", "🎟️",
    "🎫", "🎖️", "🏆", "🏅", "🥇", "🥈", "🥉", "⚽", "⚾", "🥎",
    "🏀", "🏐", "🏈", "🏉", "🎾", "🥏", "🎳", "🏏", "🏑", "🏒",
    "🥍", "🏓", "🏸", "🥊", "🥋", "🥅", "⛳", "🎣", "🎽", "🎯",
    "🪀", "🪁", "🎱", "🔮", "🧿", "🪄", "🎮", "🕹️", "🎲", "♟️",
    "🎭", "🖼️", "🎨", "🧵", "🪡", "🧶", "🪢", "👓", "🕶️", "🥽",
    "🥼", "🦺", "👔", "👕", "👖", "🧣", "🧤", "🧥", "🧦", "👗",
    "👘", "🥻", "🩱", "🩲", "🩳", "👙", "👚", "👛", "👜", "👝",
    "🛍️", "🎒", "👞", "👟", "🥾", "🥿", "👠", "👡", "🩰", "👢",
    "👑", "👒", "🎩", "🎓", "🧢", "🪖", "⛑️", "💄", "💍", "💼"
]


async def main():
    global current_chat, chats

    put_markdown("## 🧊 Добро пожаловать в онлайн чат с несколькими комнатами!(недоделаная версия)")

    # Создаем layout
    put_grid([
        [put_scope("chats-list"), put_scope("chat-content")],
        [None, put_scope("input-area")]
    ])

    try:
        # Отображаем список чатов
        await update_chats_list()

        # Ввод ника и выбор аватарки
        user_data = await input_group("Войти в чат", [
            input("Ваше имя", name="nickname", required=True, placeholder="Никнейм",
                  validate=lambda n: "Такой ник уже используется!" if any(
                      n in chats[chat].get('users', {}) for chat in chats) or n == '📢' else None),
            select("Выберите аватар", options=AVATARS, name="avatar", search=True),
            select("Выберите чат для входа", options=list(chats.keys()), name="chat")
        ])

        nickname = user_data['nickname']
        avatar = user_data['avatar']
        current_chat = user_data['chat']

        # Проверяем, существует ли еще выбранный чат
        if current_chat not in chats:
            current_chat = "Основной"
            toast("Выбранный чат больше не существует, переключено на Основной")

        # Добавляем пользователя
        chats[current_chat].setdefault('users', {})[nickname] = avatar
        chats[current_chat].setdefault('messages', []).append(
            ('📢', '📢', f'{avatar} `{nickname}` присоединился к чату!'))

        # Инициализация интерфейса чата
        with use_scope("chat-content", clear=True):
            put_scrollable(put_scope("msg-box"), height=300, keep_bottom=True)

        await update_messages(nickname)

        # Запускаем обновление сообщений
        refresh_task = run_async(refresh_msg(nickname))

        # Основной цикл чата
        while True:
            try:
                with use_scope("input-area", clear=True):
                    data = await input_group("💭 Новое сообщение", [
                        actions(name="action", buttons=[
                            {'label': "Отправить", 'value': 'send'},
                            {'label': "Стикер", 'value': 'sticker'},
                            {'label': "GIF", 'value': 'gif'},
                            {'label': "Создать чат", 'value': 'create'},
                            {'label': "Удалить чат", 'value': 'delete'},
                            {'label': "Сменить чат", 'value': 'switch'},
                            {'label': "Удалить сообщение", 'value': 'delete_msg'},
                            {'label': "Выйти", 'type': 'cancel'}
                        ]),
                        input(placeholder="Текст сообщения...", name="msg", value="")
                    ])

                if data is None:
                    break

                if data['action'] == 'send' and data['msg']:
                    if current_chat not in chats:
                        current_chat = "Основной"
                        toast("Чат был удален, переключено на Основной")
                        continue

                    chats[current_chat]['messages'].append((nickname, avatar, data['msg']))
                    await update_messages(nickname)

                elif data['action'] == 'sticker':
                    await send_sticker(nickname, avatar)

                elif data['action'] == 'gif':
                    await send_gif(nickname, avatar)

                elif data['action'] == 'create':
                    await create_chat(nickname)

                elif data['action'] == 'delete':
                    await delete_chat(nickname)

                elif data['action'] == 'switch':
                    await switch_chat(nickname)

                elif data['action'] == 'delete_msg':
                    await delete_message(nickname)

            except Exception as e:
                print(f"Ошибка в основном цикле: {e}")
                toast("Произошла ошибка, попробуйте еще раз")
                continue

    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        toast("Произошла ошибка при входе в чат")
        put_button(['Перезагрузить'], onclick=lambda btn: run_js('window.location.reload()'))
        return

    finally:
        # Выход из чата
        if 'refresh_task' in locals():
            refresh_task.close()

        if current_chat in chats and nickname in chats[current_chat].get('users', {}):
            chats[current_chat]['users'].pop(nickname)
            chats[current_chat]['messages'].append(
                ('📢', '📢', f'Пользователь {avatar} `{nickname}` покинул чат!'))
            await update_messages(nickname)

        toast("Вы вышли из чата!")
        put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))


async def send_sticker(nickname, avatar):
    """Отправка стикера"""
    global current_chat, chats

    try:
        if current_chat not in chats:
            toast("Текущий чат не существует!")
            return

        # Выбор категории стикера
        category = await select(
            "Выберите категорию стикера",
            options=list(STICKERS.keys())
        )

        if not category:
            return

        # Выбор конкретного стикера
        sticker = await select(
            "Выберите стикер",
            options=STICKERS[category]
        )

        if sticker:
            chats[current_chat]['messages'].append((nickname, avatar, f"[СТИКЕР] {sticker}"))
            await update_messages(nickname)

    except Exception as e:
        toast(f"Ошибка при отправке стикера: {str(e)}")


async def send_gif(nickname, avatar):
    """Отправка GIF-изображения"""
    global current_chat, chats

    try:
        if current_chat not in chats:
            toast("Текущий чат не существует!")
            return

        # Выбор категории GIF
        category = await select(
            "Выберите категорию GIF",
            options=list(GIFS.keys())
        )

        if not category:
            return

        # Создаем список для отображения с названиями
        gif_options = [f"{gif['name']}" for gif in GIFS[category]]

        # Выбор конкретного GIF
        selected = await select(
            "Выберите GIF",
            options=gif_options
        )

        if selected:
            # Находим выбранный GIF
            selected_gif = next(gif for gif in GIFS[category] if gif['name'] == selected)
            gif_url = selected_gif['url']
            chats[current_chat]['messages'].append((nickname, avatar, f"[GIF] {gif_url} | {selected_gif['name']}"))
            await update_messages(nickname)

    except Exception as e:
        toast(f"Ошибка при отправке GIF: {str(e)}")


async def create_chat(nickname):
    """Создание нового чата"""
    global current_chat, chats

    try:
        chat_data = await input_group("Создать новый чат", [
            input("Название чата", name="name", required=True,
                  validate=lambda n: "Чат с таким названием уже существует!" if n in chats else None),
            select("Выберите иконку для чата", options=AVATARS, name="avatar")
        ])

        chat_name = chat_data['name']
        chats[chat_name] = {
            "messages": [('📢', '📢', f'Чат "{chat_name}" создан!')],
            "users": {},
            "avatar": chat_data['avatar']
        }

        current_chat = chat_name
        await update_chats_list()
        with use_scope("chat-content", clear=True):
            put_scrollable(put_scope("msg-box"), height=300, keep_bottom=True)
        await update_messages(nickname)

    except Exception as e:
        toast(f"Ошибка при создании чата: {str(e)}")


async def delete_chat(nickname):
    """Удаление чата"""
    global current_chat, chats

    try:
        if len(chats) <= 1:
            toast("Нельзя удалить последний чат!")
            return

        available_chats = [chat for chat in chats if chat != current_chat]
        if not available_chats:
            toast("Нет чатов для удаления")
            return

        chat_to_delete = await select("Выберите чат для удаления",
                                      options=available_chats)

        if not chat_to_delete:
            return

        # Перемещаем пользователей
        for user, user_avatar in list(chats[chat_to_delete].get('users', {}).items()):
            chats["Основной"]['users'][user] = user_avatar
            chats["Основной"]['messages'].append(
                ('📢', '📢', f'Пользователь {user_avatar} `{user}` перемещен в основной чат'))

        del chats[chat_to_delete]

        if current_chat == chat_to_delete:
            current_chat = "Основной"
            with use_scope("chat-content", clear=True):
                put_scrollable(put_scope("msg-box"), height=300, keep_bottom=True)

        await update_chats_list()
        await update_messages(nickname)

    except Exception as e:
        toast(f"Ошибка при удалении чата: {str(e)}")


async def delete_message(nickname):
    """Удаление сообщения"""
    global current_chat, chats

    try:
        if current_chat not in chats:
            toast("Текущий чат не существует!")
            return

        messages = chats[current_chat]['messages']
        if not messages:
            toast("Нет сообщений для удаления")
            return

        # Создаем список сообщений для выбора (только обычные сообщения, не системные)
        message_options = []
        message_indices = []

        for i, msg in enumerate(messages):
            if msg[0] != '📢':  # Исключаем системные сообщения
                message_text = f"{msg[1]} {msg[0]}: {msg[2]}"
                message_options.append(message_text)
                message_indices.append(i)

        if not message_options:
            toast("Нет сообщений для удаления")
            return

        # Добавляем возможность удалить последнее сообщение пользователя
        for i in reversed(range(len(messages))):
            msg = messages[i]
            if msg[0] == nickname:
                message_text = f"(Ваше последнее) {msg[1]} {msg[0]}: {msg[2]}"
                message_options.insert(0, message_text)
                message_indices.insert(0, i)
                break

        selected_index = await select(
            "Выберите сообщение для удаления",
            options=message_options
        )

        if selected_index is None:
            return

        selected_msg_index = message_indices[message_options.index(selected_index)]
        deleted_msg = messages[selected_msg_index]

        # Проверяем, может ли пользователь удалить это сообщение
        if deleted_msg[0] != nickname and nickname not in chats[current_chat].get('users', {}):
            toast("Вы можете удалять только свои сообщения!")
            return

        # Удаляем сообщение
        del messages[selected_msg_index]
        toast("Сообщение удалено")
        await update_messages(nickname)

    except Exception as e:
        toast(f"Ошибка при удалении сообщения: {str(e)}")


async def switch_chat(nickname):
    """Смена текущего чата"""
    global current_chat

    try:
        available_chats = list(chats.keys())
        if not available_chats:
            toast("Нет доступных чатов")
            return

        new_chat = await select("Выберите чат", options=available_chats)

        if new_chat and new_chat != current_chat:
            current_chat = new_chat
            with use_scope("chat-content", clear=True):
                put_scrollable(put_scope("msg-box"), height=300, keep_bottom=True)
            await update_messages(nickname)

    except Exception as e:
        toast(f"Ошибка при смене чата: {str(e)}")


async def update_chats_list():
    """Обновление списка чатов"""
    try:
        with use_scope("chats-list", clear=True):
            put_markdown("### 📌 Доступные чаты")
            for chat in list(chats.keys()):  # Используем list для безопасности
                user_count = len(chats[chat].get('users', {}))
                put_text(f"{chats[chat].get('avatar', '💬')} {chat} ({user_count} пользователей)").onclick(
                    lambda c=chat: run_async(switch_chat_click(c)))

            put_markdown("---")
            put_button("➕ Создать чат", onclick=lambda: run_async(create_chat(None)))

    except Exception as e:
        print(f"Ошибка обновления списка чатов: {e}")


async def switch_chat_click(chat_name):
    """Обработчик клика по чату"""
    global current_chat
    if chat_name in chats:
        current_chat = chat_name
        with use_scope("chat-content", clear=True):
            put_scrollable(put_scope("msg-box"), height=300, keep_bottom=True)
        await update_messages(None)


async def update_messages(nickname):
    """Обновление сообщений"""
    try:
        if current_chat not in chats:
            return

        with use_scope("msg-box", clear=True):
            for m in chats[current_chat].get('messages', []):
                if m[0] == '📢':
                    put_markdown(f"{m[1]} {m[2]}")
                else:
                    if m[2].startswith("[СТИКЕР] "):
                        sticker = m[2][9:]  # Убираем префикс [СТИКЕР]
                        put_text(f"{m[1]} `{m[0]}`: ").style('display: inline-block; vertical-align: middle;')
                        put_text(sticker).style('font-size: 24px; display: inline-block; vertical-align: middle;')
                    elif m[2].startswith("[GIF] "):
                        # Разбираем строку на URL и название
                        parts = m[2][6:].split(" | ")
                        gif_url = parts[0]
                        gif_name = parts[1] if len(parts) > 1 else "GIF"
                        put_text(f"{m[1]} `{m[0]}`: {gif_name}").style('display: block;')
                        put_image(gif_url).style('max-width: 200px; max-height: 200px;')
                    else:
                        put_markdown(f"{m[1]} `{m[0]}`: {m[2]}")

    except Exception as e:
        print(f"Ошибка обновления сообщений: {e}")


async def refresh_msg(nickname):
    """Обновление сообщений в реальном времени"""
    last_counts = {chat: len(chats[chat].get('messages', [])) for chat in chats}

    while True:
        try:
            await asyncio.sleep(1)

            # Проверяем существование текущего чата
            if current_chat not in chats:
                current_chat = "Основной"
                last_counts = {chat: len(chats[chat].get('messages', [])) for chat in chats}
                continue

            # Проверяем новые сообщения
            current_msg_count = len(chats[current_chat].get('messages', []))
            if current_chat in last_counts and current_msg_count > last_counts[current_chat]:
                new_msgs = chats[current_chat]['messages'][last_counts[current_chat]:]
                with use_scope("msg-box"):
                    for m in new_msgs:
                        if m[0] != nickname:
                            if m[0] == '📢':
                                put_markdown(f"{m[1]} {m[2]}")
                            else:
                                if m[2].startswith("[СТИКЕР] "):
                                    sticker = m[2][9:]
                                    put_text(f"{m[1]} `{m[0]}`: ").style(
                                        'display: inline-block; vertical-align: middle;')
                                    put_text(sticker).style(
                                        'font-size: 24px; display: inline-block; vertical-align: middle;')
                                elif m[2].startswith("[GIF] "):
                                    parts = m[2][6:].split(" | ")
                                    gif_url = parts[0]
                                    gif_name = parts[1] if len(parts) > 1 else "GIF"
                                    put_text(f"{m[1]} `{m[0]}`: {gif_name}").style('display: block;')
                                    put_image(gif_url).style('max-width: 200px; max-height: 200px;')
                                else:
                                    put_markdown(f"{m[1]} `{m[0]}`: {m[2]}")
                last_counts[current_chat] = current_msg_count

            # Очистка старых сообщений
            for chat in list(chats.keys()):
                if len(chats[chat].get('messages', [])) > MAX_MESSAGES_COUNT:
                    chats[chat]['messages'] = chats[chat]['messages'][len(chats[chat]['messages']) // 2:]
                    last_counts[chat] = len(chats[chat]['messages'])

        except Exception as e:
            print(f"Ошибка в refresh_msg: {e}")
            await asyncio.sleep(3)  # Задержка перед повторной попыткой


if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)