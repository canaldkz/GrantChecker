import time, requests, asyncio, telebot, os
import config as cfg

bot = telebot.TeleBot(os.environ.get('token'))
URL = f'https://grant.testcenter.kz/api/v1/grant/test-type/1/test-year/{cfg.YEAR}/student/{cfg.S_IKT}/iin/{cfg.S_IIN}'


async def check():
    resp = requests.get(URL).json()
    if resp['errorCode']:
        print(f'{time.strftime("%m.%d %X")} :: {resp["errorMessage"]["ru"]}')
        return
    if resp['data']['hasGrant'] is True:
        msg = f'{time.strftime("%m.%d %X")}\n{resp["data"]["fullname"]}\n{resp["data"]["eduProgramCode"]} - {resp["data"]["eduProgramNameRus"]}\n{resp["data"]["instituteNameRus"]}'
        print(msg)
        return msg
    if resp['data']['hasGrant'] is False:
        msg = f'{time.strftime("%m.%d %X")}\n{resp["data"]["fullname"]}\nК сожалению, вы не получили грант.'
        print(msg)
        return msg


def announce(msg):
    for user in cfg.TG_IDS:
        bot.send_message(user, msg)
    return


async def main():
    print(
        f'=== GrantChecker v0.1 ===\nИИН: {cfg.S_IIN}, ИКТ: {cfg.S_IKT}, ГОД: {cfg.YEAR}, ЧАСТОТА: {cfg.FREQ} мин.'
    )
    print('Параметры редактируются в файле config.py')
    print('=========================')

    result = None

    while True:
        try:
            result = await check()
            if result:
                break
        except Exception as e:
            print(e)
            bot.send_message(cfg.TG_REPORT, e)
        await asyncio.sleep(cfg.FREQ * 60)

    announce(result)


if __name__ == '__main__':
    asyncio.run(main())
