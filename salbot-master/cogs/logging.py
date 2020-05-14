import logging
import asyncio
from discord.ext import commands
import os

bot_log_id = os.environ["BOT_LOG_CHANNEL"]
bot_errors_id = os.environ["BOT_ERRORS_CHANNEL"]
bot_automation_id = os.environ["BOT_AUTOMATION_CHANNEL"]

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.__logger = logger
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

            
        self.__logger.error(f"Error in comand {ctx.command.qualified_name}", exc_info=error)

def setup(bot):
    logging.shutdown()
    logger = logging.getLogger('salc1bot')
    logger.handlers = []
    
    class DiscordLogger(logging.Handler):
        def __init__(self, channel):
            logging.Handler.__init__(self)
            self.channel = bot.get_channel(int(channel))

        def emit(self, record):
            # Main logging.
            asyncio.ensure_future(self.channel.send(
                '`{}`'.format(self.format(record))))

    class LevelFilter(logging.Filter):
        def __init__(self, level):
            self.__level = level

        def filter(self, record):
            return record.levelno <= self.__level

    class SubloggerFilter(logging.Filter):
        def __init__(self, sublogger):
            self.__sublogger = sublogger

        def filter(self, record):
            return not record.name.endswith(self.__sublogger)
    
    formatter = logging.Formatter(
        'PID %(process)s: %(asctime)s - %(levelname)s %(filename)s:%(lineno)d - %(message)s')

    logger = logging.getLogger('salc1bot')
    logger.setLevel(logging.DEBUG)

    # shell logs
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # discord bot-log
    bot_log = DiscordLogger(bot_log_id)
    bot_log.setLevel(logging.DEBUG)
    bot_log.setFormatter(formatter)
    bot_log.addFilter(LevelFilter(logging.INFO))
    bot_log.addFilter(SubloggerFilter("automated"))
    logger.addHandler(bot_log)
    
    # error logger
    bot_errors = DiscordLogger(bot_errors_id)
    bot_errors.setLevel(logging.ERROR)
    bot_errors.setFormatter(formatter)
    logger.addHandler(bot_errors)
    
    # for quickly creating child loggers
    def create_child_logger(name, channel, level, formatting="%(asctime)s - %(message)s", parent_logger=logger):
        child_logger = parent_logger.getChild(name)
        child_logger.setLevel(level)

        ch = DiscordLogger(channel)
        ch.setLevel(level)
        formatter = logging.Formatter(formatting)
        ch.setFormatter(formatter)
        child_logger.addHandler(ch)
        return child_logger

    automated_response_logger = create_child_logger(
        "automated", bot_automation_id, logging.DEBUG)

    bot.add_cog(CommandErrorHandler(bot, logger))