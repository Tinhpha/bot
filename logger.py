import discord
from datetime import datetime

import config


# ==========================
# SEND LOG
# ==========================

async def send_log(
    bot,
    user,
    guild,
    reason,
    messages,
    action="BAN"
):

    channel = guild.get_channel(
        config.LOG_CHANNEL_ID
    )


    if not channel:
        print(
            "Không tìm thấy log channel"
        )
        return



    # ==========================
    # BASIC INFO
    # ==========================

    created = user.created_at.strftime(
        "%d/%m/%Y %H:%M"
    )


    joined = (
        user.joined_at.strftime(
            "%d/%m/%Y %H:%M"
        )
        if user.joined_at
        else "Unknown"
    )


    roles = [
        role.name
        for role in user.roles
        if role.name != "@everyone"
    ]


    role_text = (
        ", ".join(roles)
        if roles
        else "Không có"
    )



    # ==========================
    # MESSAGE LOG
    # ==========================

    spam_text = ""


    for msg in messages:

        content = msg.content.strip()


        if not content:
            content = "[Không có nội dung]"


        spam_text += (
            f"**#{msg.channel.name}**\n"
            f"{content[:300]}\n\n"
        )


    if len(spam_text) > 3500:

        spam_text = (
            spam_text[:3500]
            +
            "\n..."
        )



    # ==========================
    # EMBED
    # ==========================


    embed = discord.Embed(
        title=f"🚨 {action}",
        description=(
            f"**User:** {user.mention}\n"
            f"**ID:** `{user.id}`\n\n"
            f"**Lý do:** `{reason}`"
        ),
        timestamp=datetime.utcnow()
    )


    embed.set_thumbnail(
        url=user.display_avatar.url
    )


    embed.add_field(
        name="📅 Account tạo",
        value=created,
        inline=True
    )


    embed.add_field(
        name="📥 Join server",
        value=joined,
        inline=True
    )


    embed.add_field(
        name="🎭 Role",
        value=role_text[:1024],
        inline=False
    )


    if spam_text:

        embed.add_field(
            name="💬 Tin nhắn spam",
            value=spam_text,
            inline=False
        )


    embed.set_footer(
        text=f"{guild.name} | AutoMod"
    )


    await channel.send(
        embed=embed
    )