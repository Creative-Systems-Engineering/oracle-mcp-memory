# Oracle Cloud Free Storage Setup Guide

## 🔒 SECURITY FIRST

**⚠️ CRITICAL SECURITY NOTICE:**
- **Create YOUR OWN Oracle Cloud account** - do not share accounts
- **Generate YOUR OWN storage bucket and URLs** - never use examples from documentation
- **Keep your Pre-Authenticated URLs PRIVATE** - treat them like passwords
- **URLs in this guide are EXAMPLES ONLY** - replace with your actual values

> 📋 **Complete Security Guide**: Read [SECURITY.md](SECURITY.md) for detailed security checklist and best practices.

## 🎯 Goal: Get 20GB Free Cloud Storage for AI Memory

This guide will walk you through setting up Oracle Cloud Object Storage (completely free) for your AI memory. **Total time: ~10 minutes.**

## 📋 What You'll Need

- Valid email address  
- Phone number (for SMS verification)
- Credit card (for verification only - won't be charged)

## 🚀 Step-by-Step Setup

### Step 1: Create Oracle Cloud Account

1. **Go to Oracle Cloud Free Tier**
   - Visit: https://www.oracle.com/cloud/free/
   - Click **"Start for Free"**

2. **Fill Registration Form**
   ```
   Account Type: Personal Use
   Country/Territory: [Your country]
   First Name: [Your name]
   Last Name: [Your name]
   Email: [Valid email - you'll need to verify this]
   Password: [Strong password - save it!]
   ```

3. **Verify Your Email**
   - Check your email inbox
   - Click the verification link from Oracle
   - Complete email verification

4. **Phone Verification**
   - Enter your mobile phone number
   - Oracle will send SMS verification code
   - Enter the 6-digit code

5. **Add Payment Method**
   - **⚠️ Important**: Credit card required for account verification
   - **✅ Promise**: Oracle won't charge for Always Free services
   - Your card will only be charged if you manually upgrade to paid services
   - Enter credit card details

6. **Complete Account Setup**
   - Review and accept terms
   - Click **"Complete Sign-Up"**
   - Account creation takes 5-10 minutes
   - You'll receive confirmation email

### Step 2: Access Oracle Cloud Console

1. **Sign In**
   - Go to: https://cloud.oracle.com
   - Click **"Sign In"**
   - Enter your **Cloud Account Name** (from confirmation email)
   - Sign in with email + password

2. **Navigate to Object Storage**
   - In Oracle Cloud Console, click **hamburger menu** (≡) top-left
   - Go to: **Storage** → **Object Storage & Archive Storage** → **Buckets**

### Step 3: Create Storage Bucket

1. **Select Compartment**
   - Make sure you're in **"root"** compartment (default for new accounts)
   - If dropdown shows different compartment, select "root"

2. **Create Bucket**
   - Click **"Create Bucket"**
   - **Bucket Name**: `ai-memory-storage` (or your preferred name)
   - **Default Storage Tier**: Standard
   - **Object Versioning**: Disable (saves space)
   - **Object Events**: Disable  
   - **Encryption**: Oracle-managed keys (default)
   - Click **"Create"**

### Step 4: Generate Access URL

1. **Open Your Bucket**
   - Click on your bucket name (`ai-memory-storage`)

2. **Create Pre-Authenticated Request**
   - Left sidebar: Click **"Pre-Authenticated Requests"**
   - Click **"Create Pre-Authenticated Request"**

3. **Configure Access**
   ```
   Name: ai-memory-access
   Access Type: "Permit object reads and writes" ⚠️ CRITICAL
   Target: Object (leave blank for full bucket access)
   Expiration: [Set to 1 year from today - maximum allowed]
   ```

4. **Save the URL**
   - Click **"Create Pre-Authenticated Request"**
   - **🚨 CRITICAL**: Copy the **Pre-Authenticated Request URL**
   - **Example URL** (DO NOT USE THIS - IT'S FAKE): 
     ```
     https://objectstorage.us-ashburn-1.oraclecloud.com/p/EXAMPLE-TOKEN-123/n/EXAMPLE-NAMESPACE/b/ai-memory-storage/o/
     ```
   - **⚠️ You cannot retrieve this URL again** - save it safely!
   - **⚠️ This URL is like a password** - keep it private!

### Step 5: Test Your Storage

1. **Test Upload**
   ```bash
   # Replace YOUR_ACTUAL_URL with your real Pre-Authenticated Request URL
   # DO NOT use the example URLs from this documentation!
   curl -X PUT "YOUR_ACTUAL_URL/test.txt" \
        -H "Content-Type: text/plain" \
        -d "Hello from Oracle Cloud!"
   ```

2. **Test Download**
   ```bash
   curl "YOUR_ACTUAL_URL/test.txt"
   # Should return: Hello from Oracle Cloud!
   ```

3. **Verify in Console**
   - Refresh your bucket in Oracle Console
   - You should see `test.txt` file

## ✅ Configuration for MCP

Use your Oracle URL in VS Code MCP configuration:

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/oracle-memory-server.js"],
      "env": {
        "ORACLE_BASE_URL": "YOUR_ACTUAL_ORACLE_URL_FROM_STEP_4",
        "MEMORY_FILE_PATH": "/path/to/local/backup/copilot-memory.json"
      }
    }
  }
}
```

> 🔒 **SECURITY REMINDER**: Replace `YOUR_ACTUAL_ORACLE_URL_FROM_STEP_4` with the URL you copied in Step 4. Never share this URL with anyone!

## 🎊 Success!

You now have:
- ✅ **20GB free cloud storage** (never expires!)
- ✅ **Enterprise-grade reliability** with Oracle infrastructure  
- ✅ **Global accessibility** from anywhere in the world
- ✅ **Secure pre-authenticated access** for your AI memory
- ✅ **Ready for MCP integration** with your AI assistant

## 🚨 Important Notes

### Security
- **🔐 Keep your Pre-Authenticated URL private** - treat it like a password
- **👥 Never share URLs with others** - each person needs their own Oracle account
- **📅 URL expires in 1 year** - set calendar reminder to renew  
- **🛡️ Monitor usage** - check Oracle Console regularly for unexpected activity
- **💾 Local backup recommended** - MCP server creates automatic local backup
- **🚫 Don't commit URLs to Git** - they should never be in version control

> ⚠️ **WARNING**: Anyone with your Pre-Authenticated URL can read/write to your storage bucket. Treat it like a password!

### Free Tier Limits
- **Storage**: 20GB total (more than enough for AI memory)
- **API Calls**: 20,000 per month (very generous)
- **Bandwidth**: 10TB egress per month
- **Duration**: Always Free (no expiration)

### Renewal Process
When your Pre-Authenticated Request expires (after 1 year):
1. Go back to your bucket → Pre-Authenticated Requests
2. Create new request with same settings
3. Update your MCP configuration with new URL
4. Restart VS Code

## 🆘 Need Help?

- **Oracle Documentation**: [Object Storage Quick Start](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/managingobjects_topic-To_upload_objects_to_a_bucket.htm)
- **MCP Setup Issues**: See [SETUP.md](SETUP.md) troubleshooting section
- **GitHub Issues**: Report problems on our repository

---

**Next**: Return to main [SETUP.md](SETUP.md) to configure VS Code MCP integration.
