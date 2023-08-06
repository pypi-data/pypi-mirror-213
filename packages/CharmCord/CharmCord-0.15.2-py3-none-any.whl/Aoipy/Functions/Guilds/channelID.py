import CharmCord.CharmErrorHandling as ErrorHandling

EH = ErrorHandling.CharmErrorHandling()


async def channelID(Name, Context):
    if len(Name) < 1:
        raise EH.Errors(4, "No parameter provided for '$channelID'")
    from CharmCord.Classes.CharmCord import bots
    try:
        channel = await bots.fetch_user(Name)
        return channel.name
    except ValueError:
        EH.Errors(2, Name)