import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import time


OWNER_ID = 2tane olcaksa vürgülün yanına diğeri,


IZINLI_ROLLER = [
    , 
    ,  
]

TOKEN = ''


def yetkili_mi(interaction: discord.Interaction) -> bool:
    """Kullanıcının yetkili olup olmadığını kontrol eder"""
    if interaction.user.id == OWNER_ID:
        return True
    
    for rol_id in IZINLI_ROLLER:
        rol = interaction.guild.get_role(rol_id)
        if rol and rol in interaction.user.roles:
            return True
    
    return False

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ Bot başlatıldı: {self.user.name}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'>>> FRENESIS Çevrimiçi: {bot.user.name}')
    print(f'>>> Bot ID: {bot.user.id}')


@bot.tree.command(name="dm-duyuru", description="Sunucudaki TÜM üyelere toplu DM gönderir")
@app_commands.describe(mesaj="Gönderilecek mesaj içeriğini girin")
async def dm_duyuru(interaction: discord.Interaction, mesaj: str):
    if not yetkili_mi(interaction):
        return await interaction.response.send_message(
            "**Yetkiniz Yok!**\nBu komutu sadece **Bot Sahibi** veya **Yetkili roller** kullanabilir.",
            ephemeral=True
        )
    
    await interaction.response.send_message("**Tüm üyelere** DM gönderimi başlatılıyor...", ephemeral=False)
    
    target_members = [m for m in interaction.guild.members if not m.bot]
    total = len(target_members)
    
    if total == 0:
        return await interaction.followup.send(" Gönderilecek üye bulunamadı.")
    
    success = 0
    fail = 0
    basarili_liste = []
    basarisiz_liste = []
    
    for member in target_members:
        try:
         
            dm_embed = discord.Embed(
                title="DUYURU",
                description=f"{member.mention}\n\n{mesaj}",
                color=discord.Color.blue()
            )
            dm_embed.add_field(name="@everyone @here", value="Bu duyuru herkesi ilgilendirmektedir.", inline=False)
            dm_embed.set_footer(text=f"Gönderen: {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            dm_embed.timestamp = discord.utils.utcnow()
            
            await member.send(embed=dm_embed)
            success += 1
            basarili_liste.append(member.name)
            
        except discord.Forbidden:
            fail += 1
            basarisiz_liste.append(f"{member.name} (DM kapalı)")
            
        except Exception as e:
            fail += 1
            basarisiz_liste.append(f"{member.name} (Hata)")
        
        await asyncio.sleep(1.5)
    
   
    result_embed = discord.Embed(
        title="DM GÖNDERİM RAPORU",
        description=f"**{interaction.guild.name}** sunucusunda işlem tamamlandı!",
        color=discord.Color.gold()
    )
    
    result_embed.add_field(name="BAŞARILI", value=f"**{success}** kişi", inline=True)
    result_embed.add_field(name="BAŞARISIZ", value=f"**{fail}** kişi", inline=True)
    result_embed.add_field(name="TOPLAM", value=f"**{total}** kişi", inline=True)
    result_embed.add_field(name="BAŞARI ORANI", value=f"**%{round((success/total)*100) if total > 0 else 0}**", inline=True)
    
    if basarili_liste:
        basarili_text = "\n".join(basarili_liste[:20])
        if len(basarili_liste) > 20:
            basarili_text += f"\n... ve {len(basarili_liste) - 20} kişi daha"
        result_embed.add_field(name="BAŞARILI GÖNDERİLENLER", value=f"```{basarili_text}```", inline=False)
    
    if basarisiz_liste:
        basarisiz_text = "\n".join(basarisiz_liste[:20])
        if len(basarisiz_liste) > 20:
            basarisiz_text += f"\n... ve {len(basarisiz_liste) - 20} kişi daha"
        result_embed.add_field(name="GÖNDERİLEMEYENLER", value=f"```{basarisiz_text}```", inline=False)
    
    result_embed.set_footer(text=f"Komutu kullanan: {interaction.user.name}")
    result_embed.timestamp = discord.utils.utcnow()
    
   
    await interaction.followup.send(embed=result_embed)


@bot.tree.command(name="dm-duyuru-ozel-rol", description="Belirttiğin ID'deki role toplu DM gönderir")
@app_commands.describe(
    rol_id="DM göndermek istediğin rolün ID'sini yaz",
    mesaj="Gönderilecek mesaj içeriğini girin"
)
async def dm_duyuru_ozel_rol(interaction: discord.Interaction, rol_id: str, mesaj: str):
    if not yetkili_mi(interaction):
        return await interaction.response.send_message(
            "**Yetkiniz Yok!**\nBu komutu sadece **Bot Sahibi** veya **Yetkili roller** kullanabilir.",
            ephemeral=True
        )
    
    try:
        rol_id_int = int(rol_id)
    except ValueError:
        return await interaction.response.send_message("Geçersiz rol ID'si!", ephemeral=True)
    
    rol = interaction.guild.get_role(rol_id_int)
    if not rol:
        return await interaction.response.send_message(f"❌ Rol bulunamadı! ID: {rol_id}", ephemeral=True)
    
    await interaction.response.send_message(f"**{rol.name}** rolüne DM gönderimi başlatılıyor...", ephemeral=False)
    
    target_members = [m for m in rol.members if not m.bot]
    total = len(target_members)
    
    if total == 0:
        return await interaction.followup.send("⚠️Bu rolde mesaj atılacak üye bulunamadı.")
    
    success = 0
    fail = 0
    basarili_liste = []
    basarisiz_liste = []
    
    for member in target_members:
        try:
            
            dm_embed = discord.Embed(
                title="ÖZEL DUYURU",
                description=f"{member.mention}\n\n{mesaj}",
                color=discord.Color.purple()
            )
            dm_embed.add_field(name="Hedef Rol", value=rol.name, inline=True)
            dm_embed.add_field(name="@everyone @here", value="Bu duyuru özel rolünüze özeldir.", inline=False)
            dm_embed.set_footer(text=f"Gönderen: {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            dm_embed.timestamp = discord.utils.utcnow()
            
            await member.send(embed=dm_embed)
            success += 1
            basarili_liste.append(member.name)
            
        except discord.Forbidden:
            fail += 1
            basarisiz_liste.append(f"{member.name} (DM kapalı)")
            
        except Exception as e:
            fail += 1
            basarisiz_liste.append(f"{member.name} (Hata)")
        
        await asyncio.sleep(1.5)
    
   
    result_embed = discord.Embed(
        title="ÖZEL ROL DM GÖNDERİM RAPORU",
        description=f"**{rol.name}** rolüne işlem tamamlandı!",
        color=discord.Color.gold()
    )
    
    result_embed.add_field(name="BAŞARILI", value=f"**{success}** kişi", inline=True)
    result_embed.add_field(name="BAŞARISIZ", value=f"**{fail}** kişi", inline=True)
    result_embed.add_field(name="TOPLAM", value=f"**{total}** kişi", inline=True)
    result_embed.add_field(name="BAŞARI ORANI", value=f"**%{round((success/total)*100) if total > 0 else 0}**", inline=True)
    
    if basarili_liste:
        basarili_text = "\n".join(basarili_liste[:20])
        if len(basarili_liste) > 20:
            basarili_text += f"\n... ve {len(basarili_liste) - 20} kişi daha"
        result_embed.add_field(name="BAŞARILI GÖNDERİLENLER", value=f"```{basarili_text}```", inline=False)
    
    if basarisiz_liste:
        basarisiz_text = "\n".join(basarisiz_liste[:20])
        if len(basarisiz_liste) > 20:
            basarisiz_text += f"\n... ve {len(basarisiz_liste) - 20} kişi daha"
        result_embed.add_field(name="GÖNDERİLEMEYENLER", value=f"```{basarisiz_text}```", inline=False)
    
    result_embed.set_footer(text=f"Komutu kullanan: {interaction.user.name}")
    result_embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=result_embed)

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ HATA: Token geçersiz!")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
