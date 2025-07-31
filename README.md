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

## 🚀 Quick Start (5 Minutes)

> 🔒 **SECURITY NOTICE**: You MUST create your own Oracle Cloud account and storage bucket. Do NOT use URLs from this documentation - they are examples only!
> 
> 📋 **Security Checklist**: Review [SECURITY.md](SECURITY.md) for complete security guidelines before you start.

### Step 1: Clone & Install
```bash
git clone https://github.com/Creative-Systems-Engineering/oracle-mcp-memory.git
cd oracle-mcp-memory
npm install
```

### Step 2: Get Free Oracle Cloud Storage
1. **Sign up** at [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/) 
2. **Create bucket** in Object Storage
3. **Generate pre-authenticated URL** (valid for 1 year)
4. **Copy the URL** - you'll need it for configuration

> 💡 **Detailed Oracle setup guide**: See [ORACLE_SETUP.md](ORACLE_SETUP.md) for complete step-by-step instructions with screenshots.
> 
> 🔧 **VS Code setup guide**: See [SETUP.md](SETUP.md) for full configuration instructions.

### Step 3: Configure VS Code MCP
Edit your MCP config file:
- **Linux**: `~/.config/Code/User/mcp.json`
- **macOS**: `~/Library/Application Support/Code/User/mcp.json`  
- **Windows**: `%APPDATA%\Code\User\mcp.json`

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "node", 
      "args": ["/full/path/to/oracle-memory-server.js"],
      "env": {
        "ORACLE_BASE_URL": "https://objectstorage.region.oraclecloud.com/p/YOUR-ACTUAL-TOKEN/n/YOUR-NAMESPACE/b/YOUR-BUCKET/o/",
        "MEMORY_FILE_PATH": "/full/path/to/local-backup/copilot-memory.json"
      }
    }
  }
}
```

> ⚠️ **REPLACE PLACEHOLDER VALUES**: The URL above is an example. You must replace `YOUR-ACTUAL-TOKEN`, `YOUR-NAMESPACE`, and `YOUR-BUCKET` with values from YOUR Oracle account.

### Step 4: Test It Works
1. **Restart VS Code**
2. **Create a memory**: Ask Copilot to remember something  
3. **Check Oracle Console** - you should see `copilot-memory.json` in your bucket
4. **Multi-device test**: Access the same memory from another VS Code instance

**🎉 Done!** Your AI now has persistent, cloud-backed memory that survives across sessions, devices, and VS Code reinstalls.

## 🌟 Why Oracle Cloud?

**Oracle Cloud offers the most generous free tier for AI memory storage:**

### 🆓 Always Free Benefits
- **20GB Object Storage** - Never expires, no credit card expiration worries
- **20,000 API requests/month** - More than enough for AI memory operations  
- **10TB egress/month** - Massive bandwidth allowance
- **Global availability** - 44 regions worldwide
- **Enterprise SLA** - 99.95% uptime guarantee

### 🏆 Compared to Alternatives
| Provider | Free Storage | Expires? | API Limits | Enterprise Grade |
|----------|-------------|----------|------------|------------------|
| **Oracle** | **20GB** | **Never** | **20K/month** | **✅ Yes** |
| Google Drive | 15GB | Never | 100/day | ❌ No |
| Dropbox | 2GB | Never | 120/hour | ❌ No |
| AWS S3 | 5GB | 12 months | 2K/month | ✅ Yes |
| Azure Blob | 5GB | 12 months | Limited | ✅ Yes |

### 🔒 Enterprise Security
- **Pre-authenticated URLs** - Secure, time-limited access
- **Object versioning** - Recover from accidental changes
- **Encryption at rest** - Your data is always encrypted
- **Audit logging** - Track all access patterns
- **GDPR compliant** - Meets international data protection standards

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
