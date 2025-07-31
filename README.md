# Oracle MCP Memory Server

## 🚀 Enterprise-Grade AI Memory with Oracle Cloud

A revolutionary **Model Context Protocol (MCP) memory server** that provides persistent, cloud-backed AI memory using Oracle Object Storage. Never lose your AI context again - work seamlessly across devices with enterprise-grade reliability.

## 📁 File Structure

```
oracle-mcp-memory/
├── oracle-memory-server.js    # Custom MCP memory server with built-in Oracle sync
├── package.json               # Node.js dependencies for MCP server
├── package-lock.json          # Locked dependency versions
└── README.md                  # This documentation
```

## ⚙️ How It Works

1. **Native Integration**: `oracle-memory-server.js` replaces the standard MCP memory server
2. **Automatic Sync**: Every memory read loads from Oracle Cloud, every write saves to Oracle Cloud
3. **Transparent Operation**: VS Code uses this exactly like normal memory but with cloud backing
4. **Enterprise Storage**: 20GB Oracle Object Storage with pre-authenticated URLs
5. **Zero Maintenance**: No external scripts, services, or manual sync required

## 🔧 Configuration

### MCP Configuration (`~/.config/Code - Insiders/User/mcp.json`):
```json
{
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
```

### Oracle Object Storage:
- **Bucket**: Your Oracle Cloud bucket name
- **Storage**: 20GB free tier
- **Authentication**: Pre-authenticated URLs
- **Object**: `copilot-memory.json`

## 🗂️ Memory Location

- **Local Backup**: Configurable local path
- **Cloud Primary**: Oracle Object Storage bucket

## 🔄 Evolution Journey

This solution evolved through 5 phases:
1. **Google Drive API** (failed - OAuth complexity)
2. **Supabase PostgreSQL** (race conditions) 
3. **Bidirectional Sync** (file corruption issues)
4. **Dropbox Manual** (working but limited)
5. **Oracle Native** (current - optimal solution)

## ✅ Benefits

- ✅ **Enterprise reliability** with Oracle Cloud infrastructure
- ✅ **Native MCP integration** - no external processes
- ✅ **Automatic sync** on every memory operation
- ✅ **20GB storage** for unlimited memory growth
- ✅ **Zero maintenance** required
- ✅ **Atomic operations** eliminate race conditions
- ✅ **Fallback safety** with local file backup

## 🎯 Status: Production Ready

This system is actively running and automatically syncing all memory operations to Oracle Cloud. No further maintenance or external scripts are required.
