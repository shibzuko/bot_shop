from aiogram import Dispatcher
from .is_admin import IsAdmin
from .is_user import IsUser

# Регистрируем классы IsAdmin и IsUser с помощью фабрики фильтров (dp.filters_factory.bind), чтобы в
# других файлах можно было использовать эти фильтры без явного импорта. Они будут доступны через
# экземпляр диспетчера, который передается в функцию setup.

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin, event_handlers=[dp.message_handlers])
    dp.filters_factory.bind(IsUser, event_handlers=[dp.message_handlers])
