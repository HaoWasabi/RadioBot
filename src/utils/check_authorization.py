from nextcord import Interaction

async def check_authorization(interaction: Interaction, author):
    """Helper function to check if the user is authorized."""
    if interaction.user != author:
        await interaction.response.send_message(
            "You are not authorized to use this action.",
            ephemeral=True
        )
        return False
    return True
