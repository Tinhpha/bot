import discord
from discord.ext import commands
from datetime import timedelta
import config
from logger import send_log


# ==========================
# CHECK ADMIN
# ==========================

def is_admin():

    async def predicate(ctx):

        if not ctx.author.guild_permissions.administrator:
            await ctx.send(
                "❌ Bạn không có quyền sử dụng lệnh này."
            )
            return False

        return True

    return commands.check(predicate)



# ==========================
# BAN
# ==========================

class Moderation(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.command(
        name="ban"
    )
    @is_admin()
    async def ban(
        self,
        ctx,
        member: discord.Member,
        *,
        reason="Không có lý do"
    ):


        if member == ctx.author:

            await ctx.send(
                "❌ Không thể tự ban chính mình."
            )
            return


        if member.top_role >= ctx.guild.me.top_role:

            await ctx.send(
                "❌ Không thể ban người có role cao hơn bot."
            )
            return


        await member.ban(
            reason=reason
        )


        await ctx.send(
            f"✅ Đã ban {member.mention}"
        )


        await send_log(
            bot=self.bot,
            user=member,
            guild=ctx.guild,
            reason=reason,
            messages=[],
            action="ADMIN BAN"
        )



# ==========================
# MUTE
# ==========================

    @commands.command(
        name="mute"
    )
    @is_admin()
    async def mute(
        self,
        ctx,
        member: discord.Member
    ):


        if member.top_role >= ctx.guild.me.top_role:

            await ctx.send(
                "❌ Không thể mute người có role cao hơn bot."
            )

            return


        duration = discord.utils.utcnow()

        until = duration + timedelta(
            minutes=10
        )


        await member.timeout(
            until,
            reason="Admin mute"
        )


        await ctx.send(
            f"🔇 Đã mute {member.mention} 10 phút"
        )



# ==========================
# UNMUTE
# ==========================

    @commands.command(
        name="unmute"
    )
    @is_admin()
    async def unmute(
        self,
        ctx,
        member: discord.Member
    ):


        await member.timeout(
            None,
            reason="Admin unmute"
        )


        await ctx.send(
            f"🔊 Đã unmute {member.mention}"
        )



# ==========================
# UNBAN
# ==========================

    @commands.command(
        name="unban"
    )
    @is_admin()
    async def unban(
        self,
        ctx,
        user_id: int
    ):


        try:

            user = await self.bot.fetch_user(
                user_id
            )


            await ctx.guild.unban(
                user
            )


            await ctx.send(
                f"✅ Đã unban `{user}`"
            )


        except discord.NotFound:

            await ctx.send(
                "❌ Không tìm thấy user bị ban."
            )



# ==========================
# SETUP
# ==========================

async def setup(bot):
    await bot.add_cog(Moderation(bot))