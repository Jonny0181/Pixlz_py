from discord.ext import commands
from utils import checks
import discord
import asyncio
import os
from datetime import datetime
try:
    import psutil
    psutilAvailable = True
except:
    psutilAvailable = False

class Tools:
    def __init__(self, pixlz):
        self.pixlz = pixlz

    @commands.command()
    @commands.check(checks.is_owner)
    async def eval(self, ctx, *, code: str):
        """ fuck shit up """
        if self._eval.get('env') is None:
            self._eval['env'] = {}
        if self._eval.get('count') is None:
            self._eval['count'] = 0

        self._eval['env'].update({
            'self': self.pixlz,
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'guild': ctx.message.guild,
            'author': ctx.message.author,
        })

        code = code.replace('```py\n', '').replace('```', '').replace('`', '')

        _code = 'async def func(self):\n  try:\n{}\n  finally:\n    self._eval[\'env\'].update(locals())'\
            .format(textwrap.indent(code, '    '))

        before = time.monotonic()
        try:
            exec(_code, self._eval['env'])

            func = self._eval['env']['func']
            output = await func(self)

            if output is not None:
                output = repr(output)
        except Exception as e:
            output = '{}: {}'.format(type(e).__name__, e)
        after = time.monotonic()
        self._eval['count'] += 1
        count = self._eval['count']

        code = code.split('\n')
        if len(code) == 1:
            _in = 'In [{}]: {}'.format(count, code[0])
        else:
            _first_line = code[0]
            _rest = code[1:]
            _rest = '\n'.join(_rest)
            _countlen = len(str(count)) + 2
            _rest = textwrap.indent(_rest, '...: ')
            _rest = textwrap.indent(_rest, ' ' * _countlen)
            _in = 'In [{}]: {}\n{}'.format(count, _first_line, _rest)

        message = '```py\n{}'.format(_in)
        if output is not None:
            message += '\nOut[{}]: {}'.format(count, output)
        ms = int(round((after - before) * 1000))
        if ms > 100:  # noticeable delay
            message += '\n# {} ms\n```'.format(ms)
        else:
            message += '\n```'

        try:
            if ctx.author.id == self.pixlz.user.id:
                await ctx.message.edit(content=message)
            else:
                await ctx.send(message)
        except discord.HTTPException:
            await ctx.send("Output was too big to be printed.")		

    @commands.command()
    @commands.check(checks.is_owner)
    async def bash(self, ctx, *, command: str):
        """ Execute bash commands """

        proc = await asyncio.create_subprocess_shell(command, stdin=None, stderr=PIPE, stdout=PIPE)
        out = (await proc.stdout.read()).decode('utf-8').strip()
        err = (await proc.stderr.read()).decode('utf-8').strip()

        if not out and not err:
            return await ctx.message.add_reaction('ðŸ‘Œ')

        pages = []

        if out:
            pages += pagination.paginate(out, 1950)
        if err:
            pages += pagination.paginate(err, 1950)

        if len(pages) > 1:
            m = await ctx.send(f'The bash output yielded **{len(pages)}** pages of output. Post? (`y`/`n`)')
            try:
                resp = await ctx.pixlz.wait_for('message', check=lambda m: m.content == 'y' or m.content == 'n', timeout=15)

                if resp.content == 'n':
                    return await m.edit(content='Output will not be posted.')

                for page in pages:
                    await ctx.send(f"```bash\n{page}\n```")

            except asyncio.TimeoutError:
                return await m.edit(content='Prompt timed out.')
        else:
            await ctx.send(f"```bash\n{pages[0]}\n```")

def setup(pixlz):
    pixlz.add_cog(Tools(pixlz))