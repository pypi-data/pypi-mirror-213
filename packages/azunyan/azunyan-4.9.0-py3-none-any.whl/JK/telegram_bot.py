from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext


def chat_action(action: str):
    """
    Decorator that sends `action` while processing func command.

    e.g.,

    ```python
    @chat_action(ChatAction.TYPING)
    async def func...

    @chat_action(ChatAction.UPLOAD_VIDEO)
    async def func...
    ```

    - `action` str\n
        - `ChatAction.TYPING`. See `telegram.constants.ChatAction` for more.
    """

    def decorator(func):
        @wraps(func)
        async def command_func(*args, **kwargs):
            # collect update and context
            FLAG_UPDATE = False
            FLAG_CONTEXT = False
            for arg in args:
                if (not FLAG_UPDATE) and isinstance(arg, Update):
                    update = arg
                    FLAG_UPDATE = True
                elif (not FLAG_CONTEXT) and isinstance(arg, CallbackContext):
                    context = arg
                    FLAG_CONTEXT = True
                if FLAG_UPDATE and FLAG_CONTEXT:
                    break
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(*args, **kwargs)
        return command_func

    return decorator
