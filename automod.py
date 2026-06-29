import discord
import time
import re
import asyncio
from collections import defaultdict, deque

import config
from logger import send_log

BOT_INSTANCE = None
punished_users = set()
async def remove_punished(user_id):

    await asyncio.sleep(300)

    punished_users.discard(user_id)
# ==========================
# CACHE
# ==========================

message_cache = defaultdict(
    lambda: deque(maxlen=50)
)

voice_cache = defaultdict(
    lambda: deque(maxlen=20)
)
# ==========================
# BLACKLIST
# ==========================

SCAM_WORDS = [
    "grabify",
    "iplogger",
    "free-nitro",
    "steam-gift",
    "nitro-free",
    "gift-discord"
]
WEBHOOK_REGEX = re.compile(
    r"(discord\.com/api/webhooks/|discordapp\.com/api/webhooks/)",
    re.I
)

INVITE_REGEX = re.compile(
    r"(discord\.gg/|discord\.com/invite/)",
    re.I
)



# ==========================
# PROTECTION
# ==========================

def can_punish(member):

    if config.IGNORE_BOTS:
        if member.bot:
            return False


    if config.IGNORE_OWNER:
        if member.guild.owner_id == member.id:
            return False


    if config.IGNORE_ADMIN:
        if member.guild_permissions.administrator:
            return False


    bot_member = member.guild.me

    if bot_member:
        if member.top_role >= bot_member.top_role:
            return False


    return True





# ==========================
# BAN
# ==========================
async def punish(
    message,
    reason
):

    member = message.author


    if not can_punish(member):
        return


    if member.id in punished_users:
        return


    punished_users.add(member.id)


    history = list(
        message_cache[
            (
                message.guild.id,
                member.id
            )
        ]
    )


    if config.DELETE_SPAM_MESSAGES:

        for msg in history:

            try:
                await msg.delete()

            except:
                pass


    try:

        await member.ban(
            reason=reason
        )


        await send_log(
            bot=BOT_INSTANCE,
            user=member,
            guild=message.guild,
            reason=reason,
            messages=history,
            action="BAN"
        )


        print(
            f"[BAN] {member} | {reason}"
        )


        asyncio.create_task(
            remove_punished(member.id)
        )


    except discord.Forbidden:

        punished_users.discard(member.id)

        print(
            "Không đủ quyền ban:",
            member
        )



# ==========================
# CHECK
# ==========================


async def check_message(message):

    now = time.time()


    key = (
        message.guild.id,
        message.author.id
    )


    cache = message_cache[key]


    cache.append(message)



    recent = [
        m for m in cache
        if now - m.created_at.timestamp()
        <= config.MESSAGE_WINDOW
    ]


    # ======================
    # Attachment spam
    # ======================

    if len(message.attachments) >= 5:

        await punish(
            message,
            "Spam Attachment"
        )

        return
    # ======================
    # Normal spam
    # ======================

    if len(recent) >= config.MESSAGE_SPAM_LIMIT:

        await punish(
            message,
            "Spam quá nhiều tin nhắn"
        )

        return



    # ======================
    # Same content
    # ======================


    content = (
        message.content
        .lower()
        .strip()
    )


    same = [
        m for m in recent
        if m.content.lower().strip()
        == content
    ]


    if len(same) >= config.SAME_MESSAGE_LIMIT:

        await punish(
            message,
            "Spam cùng nội dung"
        )

        return




    # ======================
    # Multi channel spam
    # ======================


    channels = set(
        m.channel.id
        for m in recent
    )


    if len(channels) >= config.MULTI_CHANNEL_LIMIT:

        await punish(
            message,
            "Spam nhiều channel"
        )

        return




    # ======================
    # Role mention
    # ======================

    role_mentions = sum(
        len(m.role_mentions)
        for m in recent
    )


    if role_mentions >= config.ROLE_MENTION_LIMIT:

        await punish(
            message,
            "Spam mention role"
        )

        return

    # ======================
    # Webhook spam
    # ======================
    if WEBHOOK_REGEX.search(message.content):

        await punish(
            message,
            "Spam Webhook"
    )

        return

    # ======================
    # Everyone / Here
    # ======================

    everyone = sum(
        1
        for m in recent
        if m.mention_everyone
    )


    if everyone >= 3:

        await punish(
            message,
            "Spam @everyone/@here"
        )

        return




    # ======================
    # Invite
    # ======================

    if INVITE_REGEX.search(
        message.content
    ):

        await punish(
            message,
            "Spam Discord Invite"
        )

        return




    # ======================
    # Scam
    # ======================

    text = (
        message.content
        .lower()
    )


    for word in SCAM_WORDS:

        if word in text:

            await punish(
                message,
                "Spam Scam Link"
            )

            return




# ==========================
# EVENT
# ==========================
async def on_voice_state_update(
    member,
    before,
    after
):

    if member.bot:
        return


    if before.channel == after.channel:
        return


    now = time.time()


    history = voice_cache[
    (
        member.guild.id,
        member.id
    )
]

    history.append(now)


    # chỉ giữ trong 30 giây

    while history:

        if now - history[0] > config.VOICE_WINDOW:
            history.popleft()

        else:
            break



    if len(history) >= config.VOICE_MOVE_LIMIT:


        if not can_punish(member):
            return


        try:
            punished_users.add(member.id)

            await member.ban(
                reason="Voice channel spam"
            )

            await send_log(
                bot=BOT_INSTANCE,
                user=member,
                guild=member.guild,
                reason="Spam Voice Channel",
                messages=[],
                action="BAN"
            )


            print(
                f"[VOICE BAN] {member}"
            )
            asyncio.create_task(
            remove_punished(member.id)
)

            history.clear()


        except discord.Forbidden:

            punished_users.discard(member.id)
            history.clear()
            print(
                "Không thể ban voice spammer"
    )
async def on_message(message):

    if not message.guild:
        return


    if message.author.bot:
        return


    await check_message(message)

def setup(bot):

    global BOT_INSTANCE

    BOT_INSTANCE = bot

    bot.add_listener(
        on_message,
        "on_message"
    )

    bot.add_listener(
        on_voice_state_update,
        "on_voice_state_update"
    )