import discord
import asyncio
from pynput.keyboard import Controller, Key, KeyCode


class PauseClient(discord.Client):
    """Small bot client for initiating pause and play requests over discord"""
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.keyboard = Controller()
        self.pause_key = KeyCode.from_vk(0xB3)
        self.space_key = KeyCode.from_vk(0x20)
        self.selector = True  # True for space command, False for pause
        self.pause_strings = ['!pause', '!play']
        self.start_bot()

    def start_bot(self):
        """Starts bot client"""
        token = self.token
        loop = asyncio.get_event_loop()
        loop.create_task(self.start(self.token))
        try:
            loop.run_forever()
        finally:
            loop.stop()

    def pause_play_request(self):
        """Sends pause or space request based on selection"""
        key = self.space_key if self.selector is True else self.pause_key
        self.keyboard.press(key)
        self.keyboard.release(key)

    async def on_message(self, message):
        """Defines user inputs"""
        if message.author.id == self.user.id:
            return
        
        def matcher(msg, match):
            return msg.startswith(f'!{match}')

        async def send_key():
            key_name = 'space' if self.selector is True else 'media pause/play'
            reply = f'Currently using {key_name}'
            await message.channel.send(reply)

        msg = message.content.lower()
        if matcher(msg, 'play') or matcher(msg, 'pause'):
            self.pause_play_request()

        if matcher(msg, 'switch'): 
            self.selector = not self.selector
            await send_key()

        if matcher(msg, 'key_space'): 
            self.selector = True
            await send_key()

        if matcher(msg, 'key_pause_play'): 
            self.selector = False
            await send_key()

        if matcher(msg, 'test'):
            reply = 'This is a test'
            await message.channel.send(reply)

        if matcher(msg, 'help'):
            reply = '!pause or !play - play/pause the media\n'
            reply += '!swtich - change key from space to pause/play VK\n'
            reply += '!key_space - change key output to space\n'
            reply += '!key_pause_play - change key output to space\n'
            reply += '!pauser_exit - shut down the bot'
            await message.channel.send(reply)

        if matcher(msg, 'pauser_exit'):
            await message.channel.send('Leaving')
            await self.logout()
            loop = asyncio.get_running_loop()
            loop.stop()

    async def on_ready(self):
        print('loaded')
        game = discord.Game('use !help')
        await self.change_presence(status=discord.Status.idle, activity=game)


token = ''
with open('token.txt', 'r') as file:
    token = file.read()

Cli = PauseClient(token)
