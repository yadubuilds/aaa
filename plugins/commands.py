import asyncio, os, sys
from pyrogram import Client, filters, enums
from config import CMD_HNDLR

# --- 1. UPDATE & RESTART ---
@Client.on_message(filters.me & filters.command("restart", CMD_HNDLR))
async def restart_bot(_, m):
    await m.edit("`Restarting...`")
    os.execl(sys.executable, sys.executable, "main.py")

@Client.on_message(filters.me & filters.command("update", CMD_HNDLR))
async def update_bot(_, m):
    await m.edit("`Updating...`")
    os.system("git pull")
    os.execl(sys.executable, sys.executable, "main.py")

# --- 2. BROADCAST (DMs, CONTACTS, GROUPS) ---
@Client.on_message(filters.me & filters.command(["bcast", "cbcast", "gbcast"], CMD_HNDLR))
async def broadcast(c, m):
    if not m.reply_to_message: return await m.edit("Reply to a message!")
    
    # Extract delay and schedule
    args = m.text.split()
    delay = float(args[1]) if len(args) > 1 else 2
    wait = int(args[2]) if len(args) > 2 else 0
    
    cmd = m.command[0]
    await m.edit(f"Waiting {wait}s before starting...")
    await asyncio.sleep(wait)
    
    count = 0
    await m.edit("Broadcasting...")
    
    # Select target
    if cmd == "bcast": # All DMs
        async for dial in c.get_dialogs():
            if dial.chat.type == enums.ChatType.PRIVATE:
                try:
                    await m.reply_to_message.copy(dial.chat.id)
                    count += 1
                    await asyncio.sleep(delay)
                except: continue
    
    elif cmd == "cbcast": # Only Contacts
        for user in await c.get_contacts():
            try:
                await m.reply_to_message.copy(user.id)
                count += 1
                await asyncio.sleep(delay)
            except: continue

    elif cmd == "gbcast": # Group Members
        async for mem in c.get_chat_members(m.chat.id):
            try:
                await m.reply_to_message.copy(mem.user.id)
                count += 1
                await asyncio.sleep(delay)
            except: continue

    await m.edit(f"✅ Sent to {count} users.")

# --- 3. CONTACT & GROUP TOOLS ---
@Client.on_message(filters.me & filters.command("save", CMD_HNDLR))
async def save_contact(c, m):
    if not m.reply_to_message: return
    u = m.reply_to_message.from_user
    await c.add_contact(u.id, u.first_name or "User")
    await m.edit(f"Saved {u.first_name}")

@Client.on_message(filters.me & filters.command("getlink", CMD_HNDLR))
async def get_link(c, m):
    link = await c.export_chat_invite_link(m.chat.id)
    await m.edit(link)

@Client.on_message(filters.me & filters.command("reqdm", CMD_HNDLR))
async def dm_requests(c, m):
    if not m.reply_to_message: return
    count = 0
    async for req in c.get_chat_join_requests(m.chat.id):
        try:
            await m.reply_to_message.copy(req.user.id)
            count += 1
            await asyncio.sleep(1)
        except: continue
    await m.edit(f"DMed {count} join requests.")
