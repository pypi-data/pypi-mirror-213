import CharmCord.CharmErrorHandling as ErrorHandling

EH = ErrorHandling.CharmErrorHandling()


async def currentChannelID(empty, Context):
    try:
        int(Context.guild.id)
    except ValueError:
        EH.Errors(1, "None")
    return Context.guild.id