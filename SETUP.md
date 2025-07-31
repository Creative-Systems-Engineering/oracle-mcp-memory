# Oracle MCP Memory Server Setup Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- VS Code with MCP support
- Oracle Cloud account (free tier)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/oracle-mcp-memory.git
cd oracle-mcp-memory
npm install
```

### 2. Set Up Oracle Cloud Storage

#### Create Object Storage Bucket
1. Log into Oracle Cloud Console
2. Navigate to **Storage** → **Object Storage & Archive Storage** → **Buckets**
3. Click **"Create Bucket"**
4. Name your bucket (e.g., `mcp-memory-bucket`)
5. Click **"Create"**

#### Create Pre-Authenticated Request
1. In your bucket, click **"Pre-Authenticated Requests"**
2. Click **"Create Pre-Authenticated Request"**
3. Configure:
   - **Name**: `mcp-memory-access`
   - **Access Type**: "Permit object reads and writes"
   - **Expiration**: Set to your preference (max 1 year)
4. Click **"Create"**
5. **SAVE THE URL** - you won't see it again!

### 3. Configure VS Code MCP

Edit your MCP configuration file:
- **Linux**: `~/.config/Code/User/mcp.json`
- **macOS**: `~/Library/Application Support/Code/User/mcp.json`
- **Windows**: `%APPDATA%\Code\User\mcp.json`

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/oracle-memory-server.js"],
      "env": {
        "MEMORY_FILE_PATH": "/path/to/local/memory/copilot-memory.json",
        "ORACLE_BASE_URL": "https://your-oracle-bucket-url/o/"
      }
    }
  }
}
```

### 4. Test the Setup

1. Restart VS Code
2. Open the MCP panel
3. Try creating a memory entity
4. Check your Oracle bucket - you should see `copilot-memory.json`

## 🔧 Configuration Options

### Environment Variables

- **`ORACLE_BASE_URL`**: Your Oracle Object Storage pre-authenticated URL
- **`MEMORY_FILE_PATH`**: Local backup file path (optional)

### Oracle Cloud Settings

- **Free Tier**: 20GB Object Storage included
- **Always Free**: No time limits on storage
- **Global Access**: Works from anywhere

## 🚨 Security Notes

- Pre-authenticated URLs are time-limited (configure expiration)
- Keep your Oracle URLs private
- Local files are backups only - Oracle is the source of truth

## ❓ Troubleshooting

### Server Won't Start
- Check Node.js version (18+ required)
- Verify `@modelcontextprotocol/sdk` is installed
- Check file paths in MCP configuration

### Memory Not Syncing
- Verify Oracle URL is correct and not expired
- Check VS Code developer console for errors
- Test Oracle URL manually with curl

### Permission Errors
- Ensure Oracle bucket has correct permissions
- Verify pre-authenticated request hasn't expired
- Check local file path is writable

## 🔗 Resources

- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [VS Code MCP Extension](https://marketplace.visualstudio.com/items?itemName=modelcontextprotocol.mcp)
