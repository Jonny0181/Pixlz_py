owners = [95645231248048128, 170619078401196032]

def is_premium(ctx):
    return ctx.guild.id in premiumservers

def is_owner(ctx):
    return ctx.author.id in owners

def is_guild_owner(ctx):
    return ctx.guild.owner.id
