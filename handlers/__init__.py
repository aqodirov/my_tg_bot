from aiogram import Router
from .commands_handler import router as commands_handler
from .text_handlers import router as text_handlers
from .callbacks_handler import router as callbacks_handler

router = Router()
router.include_routers(commands_handler, text_handlers, callbacks_handler)