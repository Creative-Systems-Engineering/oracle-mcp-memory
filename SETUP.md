# Oracle MCP Memory Server Setup Guide

## � SECURITY FIRST

**⚠️ IMPORTANT**: You must create your own Oracle Cloud account and generate your own storage URLs. All URLs in this documentation are examples only - never use them in production!

## �🚀 Quick Start

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

### 2. Set Up Oracle Cloud Storage (FREE!)

Oracle Cloud provides 20GB of Object Storage for FREE forever - no credit card expires, no time limits!

> 📚 **Complete Oracle Setup Guide**: For detailed step-by-step instructions with screenshots, see [ORACLE_SETUP.md](ORACLE_SETUP.md)

#### Quick Oracle Setup Summary:
1. **Create Account**: [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/) (requires phone + credit card verification)
2. **Create Bucket**: Navigate to Object Storage → Create bucket
3. **Generate Access URL**: Create Pre-Authenticated Request with "read/write" permissions  
4. **Test Connection**: Verify upload/download works with curl
5. **Configure MCP**: Add Oracle URL to VS Code MCP settings

**Your Oracle URL will look like**:
```
https://objectstorage.us-ashburn-1.oraclecloud.com/p/YOUR-TOKEN/n/YOUR-NAMESPACE/b/YOUR-BUCKET/o/
```

> ⚠️ **Critical Security Notes**: 
> - The Pre-Authenticated Request URL can only be viewed once during creation - save it securely!
> - This URL is like a password - anyone with it can access your storage
> - Never share your URL or commit it to version control
> - Each user must create their own Oracle account and URLs

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

### General Issues

#### Server Won't Start
- Check Node.js version (18+ required): `node --version`
- Verify `@modelcontextprotocol/sdk` is installed: `npm list @modelcontextprotocol/sdk`
- Check file paths in MCP configuration are absolute paths
- Restart VS Code after configuration changes

#### Memory Not Syncing
- Verify Oracle URL is correct and not expired
- Check VS Code developer console for errors (Help → Toggle Developer Tools)
- Test Oracle URL manually with curl (see Oracle setup section)

### Oracle Cloud Specific Issues

#### "403 Forbidden" Error
**Cause**: Pre-Authenticated Request (PAR) has wrong permissions or expired
**Solution**:
1. Check PAR expiration date in Oracle Console
2. Ensure PAR has "Permit object reads and writes" permission
3. Create new PAR if expired:
   ```bash
   # Test your PAR URL
   curl -I "YOUR_PAR_URL/test.txt"
   # Should return 200 OK or 404 Not Found (not 403)
   ```

#### "404 Not Found" for Oracle URL
**Cause**: Incorrect bucket name, region, or namespace in URL
**Solution**:
1. Double-check your PAR URL format
2. Verify bucket exists in Oracle Console
3. Ensure you're in the correct region/compartment

#### Connection Timeouts
**Cause**: Network issues or Oracle region problems
**Solution**:
1. Try different Oracle region (create bucket in different region)
2. Check your internet connection
3. Test with curl first:
   ```bash
   curl -v "YOUR_PAR_URL" --max-time 10
   ```

#### Memory File Corrupted
**Cause**: Concurrent read/write operations or network interruption
**Solution**:
1. Check local backup file: `MEMORY_FILE_PATH/copilot-memory.json`
2. Restore from local backup if needed
3. Delete corrupted file from Oracle and let MCP recreate:
   ```bash
   curl -X DELETE "YOUR_PAR_URL/copilot-memory.json"
   ```

#### "Cannot Load Memory" Error
**Cause**: Invalid JSON in memory file or network issues
**Solution**:
1. Check Oracle Console - view the memory file content
2. Validate JSON format:
   ```bash
   curl "YOUR_PAR_URL/copilot-memory.json" | jq .
   ```
3. Reset memory if corrupted:
   ```bash
   curl -X DELETE "YOUR_PAR_URL/copilot-memory.json"
   ```

### Oracle Cloud Account Issues

#### Free Tier Limitations
- **Storage**: 20GB total across all Object Storage buckets
- **Requests**: 20,000 requests per month (very generous for MCP usage)
- **Bandwidth**: 10TB egress per month
- **PAR Duration**: Maximum 1 year expiration

#### Account Suspension
If your Oracle account gets suspended:
1. Contact Oracle Support (usually billing verification issue)
2. Ensure you haven't exceeded free tier limits
3. Keep local backup files as emergency restore

#### Regional Availability
If Oracle services aren't available in your region:
1. Choose nearest available region during signup
2. Consider using Always Free eligible regions:
   - US East (Ashburn)
   - US West (Phoenix)
   - EU West (Frankfurt)
   - UK South (London)
   - Japan East (Tokyo)
   - South Korea Central (Seoul)
   - Australia East (Sydney)

### VS Code MCP Configuration Issues

#### MCP Server Not Listed
**Cause**: Configuration file syntax error or wrong path
**Solution**:
1. Validate JSON syntax in your MCP config:
   ```bash
   # Linux/macOS
   cat ~/.config/Code/User/mcp.json | jq .
   
   # Windows
   type "%APPDATA%\Code\User\mcp.json" | jq .
   ```
2. Check absolute paths are correct
3. Restart VS Code completely

#### Environment Variables Not Working
**Cause**: MCP config doesn't support environment variable expansion
**Solution**: Use absolute URLs and paths in the configuration:
```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "node",
      "args": ["/full/path/to/oracle-memory-server.js"],
      "env": {
        "ORACLE_BASE_URL": "https://objectstorage.us-ashburn-1.oraclecloud.com/p/your-token/n/namespace/b/bucket/o/",
        "MEMORY_FILE_PATH": "/full/path/to/copilot-memory.json"
      }
    }
  }
}
```

### Emergency Recovery

#### Complete Reset
If everything breaks, here's how to start fresh:

1. **Backup Current Memory** (if accessible):
   ```bash
   curl "YOUR_PAR_URL/copilot-memory.json" > backup-memory.json
   ```

2. **Delete Corrupted Files**:
   ```bash
   curl -X DELETE "YOUR_PAR_URL/copilot-memory.json"
   rm -f /path/to/local/copilot-memory.json
   ```

3. **Restart MCP Server**: Restart VS Code

4. **Restore from Backup** (if needed):
   ```bash
   curl -X PUT "YOUR_PAR_URL/copilot-memory.json" \
        -H "Content-Type: application/json" \
        -d @backup-memory.json
   ```

#### Getting Help
1. **Check Oracle Console**: View actual files and bucket status
2. **Test with Curl**: Verify Oracle connectivity outside of VS Code
3. **VS Code Logs**: Help → Toggle Developer Tools → Console tab
4. **Oracle Support**: Free tier accounts get community support
5. **GitHub Issues**: Report bugs on our repository

## 🔗 Resources

- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [VS Code MCP Extension](https://marketplace.visualstudio.com/items?itemName=modelcontextprotocol.mcp)
