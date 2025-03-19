import aiohttp

# from config.secures import SMS_SECURES
# from resources.redis import redis_cache as cache

timeout = aiohttp.ClientTimeout(total=30)


async def sms_access_token():
    pass
    # payload = {
    #     'email': SMS_SECURES.SMS_EMAIL,
    #     'password': SMS_SECURES.SMS_PASSWORD,
    # }
    #
    # ssl_context = ssl.create_default_context(cafile=certifi.where())
    # async with aiohttp.ClientSession(timeout=timeout) as session:
    #     async with session.post(SMS_SECURES.SMS_TOKEN_URL, data=payload, ssl=ssl_context) as response:
    #         if response.status == 200:
    #             data = await response.json()
    #             return data['data']['token']
    #         else:
    #             return None


async def send_sms(message: str, phone: str):
    pass
    # if not (token := await cache.get('sms_sender_token')):
    #     token = await sms_access_token()
    #     await cache.set('sms_sender_token', token, expire=int(29.5 * 24 * 60 * 60))
    #
    # headers = {
    #     'Authorization': f'Bearer {token}'
    # }
    # payload = {
    #     'mobile_phone': phone,
    #     'message': message,
    #     'from': 'Lorry.uz'
    # }
    #
    # ssl_context = ssl.create_default_context(cafile=certifi.where())
    # async with aiohttp.ClientSession(timeout=timeout) as session:
    #     async with session.post(SMS_SECURES.SMS_SEND_URL, data=payload, headers=headers, ssl=ssl_context) as response:
    #         if response.status == 200:
    #             return await response.json()
    #         else:
    #             return None
