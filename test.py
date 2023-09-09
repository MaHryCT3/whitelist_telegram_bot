import asyncio

from bot.services.backend_api import BackendAPI


async def main():
    api = BackendAPI()
    print(await api.user_exist(123))
    print(await api.user_exist(1234))
    print(await api.steamid_exist('123'))
    print(await api.steamid_exist('1234'))
    print(await api.application_create(123, '123', '123'))
    print(await api.application_create(1234, '1234', '1234'))


if __name__ == '__main__':
    asyncio.run(main())
