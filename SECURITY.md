# 🔒 Security Checklist for Oracle MCP Memory

## Before You Start

- [ ] **Read this entire checklist** - security is critical for cloud storage
- [ ] **Understand that Oracle URLs are like passwords** - treat them accordingly
- [ ] **Confirm you have your own Oracle account** - never share accounts

## During Oracle Setup

- [ ] **Create your own Oracle Cloud account** - use your own email and phone
- [ ] **Use strong, unique password** - consider password manager
- [ ] **Enable 2FA if available** - extra security for your Oracle account
- [ ] **Create your own bucket** - unique name, don't copy examples
- [ ] **Generate your own Pre-Authenticated Request** - with proper expiration
- [ ] **Copy URL immediately** - you cannot retrieve it again
- [ ] **Store URL securely** - password manager, encrypted notes, etc.

## Security Best Practices

- [ ] **Never share your Oracle URL** - each person needs their own account
- [ ] **Don't post URLs in forums/chat** - even for debugging help
- [ ] **Don't commit URLs to Git** - check `.gitignore` protects you
- [ ] **Don't email URLs to yourself** - email is not secure
- [ ] **Don't store in plain text files** - use encrypted storage
- [ ] **Set calendar reminder** - URLs expire in 1 year
- [ ] **Monitor Oracle Console** - check for unexpected usage

## VS Code Configuration Security

- [ ] **Use absolute file paths** - don't rely on environment variables
- [ ] **Store MCP config outside Git repo** - if working on public projects
- [ ] **Restart VS Code after configuration** - ensure settings take effect
- [ ] **Test with dummy data first** - before storing sensitive information

## What URLs Look Like

✅ **SAFE - Example/Template URLs** (these are fake):
```
https://objectstorage.region.oraclecloud.com/p/YOUR-TOKEN/n/YOUR-NAMESPACE/b/YOUR-BUCKET/o/
https://objectstorage.us-ashburn-1.oraclecloud.com/p/EXAMPLE-123/n/EXAMPLE/b/bucket/o/
```

❌ **DANGER - Real URLs** (never share these patterns):
```
https://objectstorage.us-ashburn-1.oraclecloud.com/p/eyJ1IjoiNWE4MjY4YmItZjRhMy00...
https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/vK7yj2Qw9Xm3Bp8nF6gH...
```

## Emergency Response

If you accidentally expose your Oracle URL:

1. **Immediately disable the Pre-Authenticated Request**:
   - Go to Oracle Console → Your Bucket → Pre-Authenticated Requests
   - Find your request and click "Delete" or "Disable"

2. **Create new Pre-Authenticated Request**:
   - Generate new URL with different expiration
   - Update your VS Code MCP configuration

3. **Check for unauthorized access**:
   - Review Oracle Console for unexpected files
   - Check activity logs if available

4. **Rotate related credentials**:
   - Consider changing Oracle account password
   - Review other cloud services for similar exposures

## Signs of Compromise

Watch for these warning signs:

- [ ] **Unexpected files** in your Oracle bucket
- [ ] **Increased storage usage** without your knowledge
- [ ] **Oracle billing alerts** if you exceed free tier
- [ ] **Performance issues** with unusually slow access
- [ ] **Memory corruption** in your AI assistant

## Regular Maintenance

Monthly security review:

- [ ] **Check Oracle Console** - review stored files and usage
- [ ] **Review MCP configuration** - ensure settings are correct
- [ ] **Test backup/restore** - ensure you can recover from issues
- [ ] **Update expiration reminder** - prepare for URL renewal
- [ ] **Review access logs** - if available in Oracle Console

## Getting Help Securely

When asking for help:

- [ ] **Never include real URLs** - use placeholder examples
- [ ] **Redact sensitive information** - replace tokens with "XXXXX"
- [ ] **Use generic examples** - "my-bucket" instead of real names
- [ ] **Focus on error messages** - not configuration details
- [ ] **Ask in appropriate forums** - Oracle support, GitHub issues, etc.

## Example Safe Help Request

❌ **BAD** - Never do this:
```
"My Oracle URL https://objectstorage.us-ashburn-1.oraclecloud.com/p/eyJ1IjoiNWE4... isn't working"
```

✅ **GOOD** - Safe way to ask for help:
```
"My Oracle Pre-Authenticated Request URL isn't working. I'm getting a 403 error when trying to upload. The URL format is https://objectstorage.region.oraclecloud.com/p/[TOKEN]/n/[NAMESPACE]/b/[BUCKET]/o/ - any troubleshooting suggestions?"
```

---

## 🎯 Remember

**Your Oracle Pre-Authenticated URL is like a password to your cloud storage. Treat it with the same care you would treat your bank account password!**

✅ **You're ready when**: You have your own Oracle account, your own unique URL, and you understand how to keep it secure.

🔗 **Next step**: Continue with [ORACLE_SETUP.md](ORACLE_SETUP.md) or [SETUP.md](SETUP.md)
