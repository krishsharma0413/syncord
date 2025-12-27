# Syncord
```
                                                                  $$\ 
                                                                  $$ |
 $$$$$$$\ $$\   $$\ $$$$$$$\   $$$$$$$\  $$$$$$\   $$$$$$\   $$$$$$$ |
$$  _____|$$ |  $$ |$$  __$$\ $$  _____|$$  __$$\ $$  __$$\ $$  __$$ |
\$$$$$$\  $$ |  $$ |$$ |  $$ |$$ /      $$ /  $$ |$$ |  \__|$$ /  $$ |
 \____$$\ $$ |  $$ |$$ |  $$ |$$ |      $$ |  $$ |$$ |      $$ |  $$ |
$$$$$$$  |\$$$$$$$ |$$ |  $$ |\$$$$$$$\ \$$$$$$  |$$ |      \$$$$$$$ |
\_______/  \____$$ |\__|  \__| \_______| \______/ \__|       \_______|
          $$\   $$ |                                                  
          \$$$$$$  |                                                  
           \______/ 
```

**Syncord** is a CLI-based file synchronization and storage tool that uses **Discord** as a backend as **encrypted file storage**.

It allows you to upload files or entire directories to Discord, encrypt and partition them locally, and later download and reconstruct them securely; all through a simple command-line interface or an optional TUI dashboard.

Syncord is distributed as a **single executable (`syncord.exe`)** built using PyInstaller. The executable can be placed directly in your system `PATH` and used from anywhere.

---

## ✨ Features

- 🔐 **End-to-end encryption**
  - Files are encrypted locally before upload.
  - Encryption key is never stored on Discord.
  - Without the key, data cannot be recovered. Make sure not to change it after upload.

- 📦 **Automatic file partitioning**
  - Large files are split into chunks.
  - Chunks comply with Discord upload limits (discord limits: 8MB; chunk size: 5MB pre-encryption; ~7MB post-encryption)
  - Files are reassembled seamlessly on download. Thanks to SQLite tracking partitions.

- 📁 **Directory uploads**
  - Upload entire directories at once.
  - download the entire directory and sub-directories too.


- 🖥️ **CLI-first design**
  - Simple, scriptable commands.
  - Works globally when added to `PATH`

- 🧭 **TUI dashboard**
  - Interactive terminal interface.
  - View stored files and usage information.

- 📊 **Usage statistics**
  - Track uploads, downloads, and storage usage.

- 🗄️ **Local metadata database**
  - SQLite-backed metadata.
  - No dependency on Discord message history alone.

---

## 📦 Installation

### Prebuilt Binary (Recommended)

1. Download `syncord.exe`
2. Place it in a directory included in your system `PATH`
3. Verify installation:

```bash
syncord --help
```

Syncord can now be invoked from **any directory**.

---

## ⚙️ Mandatory Initial Setup

### ⚠️ **Syncord requires setup before first use.**  
Both the **Discord bot token** and the **Guild ID are mandatory**.

### Required Configuration

- Discord Bot Token.
- Discord Guild ID (server where files will be uploaded).
- Encryption key (generated locally).

### One-time setup command

```bash
syncord setup --token YOUR_DISCORD_BOT_TOKEN --guild-id YOUR_GUILD_ID --encryption-key
```

### Important Notes

- 🔑 The encryption key is critical.
- ❌ Losing the key means **permanent data loss**.
- 🔒 Discord cannot decrypt or recover your files.
- 🛑 Syncord will not function without a valid token and guild ID.

---

## 📤 Uploading Files

### Upload a single file

```bash
syncord upload file.ext
```

### Upload an entire directory

```bash
syncord upload folder_name
```

Behavior:
- All files inside the directory are processed.
- Folder structure is logically preserved.
- Each directory becomes its own Syncord folder namespace.

---

## 📥 Downloading Files

```bash
syncord download folder_on_syncord/file
```

Syncord will:
1. Locate all required partitions.
2. Download them from Discord.
3. Decrypt locally.
4. Reassemble the original file.

NOTE:
If no folder is provided, syncord assume it to be `default` where every file is uploaded.

---

## 🖥️ TUI Dashboard

```bash
syncord dashboard
```

The dashboard provides:
- Stored file overview.
- download folders and file.
- Storage usage.
- Interactive navigation.

---

## 📊 Usage Statistics

```bash
syncord stats
```

Displays:
- Total files uploaded
- Total downloads
- Storage usage
- Other tracked metrics

---

## 🧾 Command Summary

```text
syncord setup        Mandatory initial configuration
syncord upload       Upload a file or directory
syncord download     Download and reconstruct a file
syncord dashboard    Launch terminal UI dashboard
syncord stats        Show usage statistics
```

---

## 🔐 Security Model

- All encryption happens **locally**.
- Discord only stores encrypted binary chunks.
- Metadata is stored locally using SQLite.
- Discord never sees:
  - File contents.
  - Plaintext filenames.
  - Encryption keys.

> Syncord assumes you trust your local system; not Discord.

---

## 📁 Project Structure

```text
dist/
 ├── syncord.exe          # executable
core/
 ├── db_manager.py        # SQLite metadata handling
 ├── setup.py             # Configuration & setup logic
 ├── partition.py         # File chunking & reconstruction
 ├── tui.py               # Terminal UI dashboard
 ├── encrypter.py         # Encryption & Decryption
 ├── discord_handler.py   # discord bot logic
files/
 ├── uuid/file.bin        # temp storage
main.py                   # CLI entry point
```

---

## ⚠️ Limitations & Notes

- Requires a Discord bot with proper guild permissions. READ_MESSAGE_HISTORY & VIEW_CHANNEL & SEND_MESSAGES & ATTACH_FILES
- Subject to Discord rate limits.
- Not intended as a public cloud storage replacement.
- Designed for personal or controlled environments.

---

## 📜 Disclaimer

This project is intended for **educational and personal use**.  
Ensure compliance with Discord’s Terms of Service when using Syncord.

---

## 🧠 Future Updates

Issue you might face and should be fixed soon:
- rate limiting from discord because of constant up & down of bot on multi upload.
  - Best solution: maintain the connection or bulk upload and download together instead of treating each file individually; would require to rewrite `partition.py` a little.
- unexpected error of unclosed aiohttp client.