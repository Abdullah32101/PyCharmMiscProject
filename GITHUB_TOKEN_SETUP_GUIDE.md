# GitHub Personal Access Token Setup Guide

## 🔧 Fix for "Resource not accessible by integration" Error

This guide will help you fix the GitHub Actions permission error you're encountering.

## 📋 Steps to Add Your Personal Access Token

### Step 1: Go to Repository Settings
1. Navigate to your repository: `https://github.com/Abdullah32101/PyCharmMiscProject`
2. Click on the **"Settings"** tab
3. In the left sidebar, click **"Secrets and variables"** → **"Actions"**

### Step 2: Add Repository Secret
1. Click **"New repository secret"**
2. **Name**: `PERSONAL_ACCESS_TOKEN`
3. **Value**: Paste your personal access token here
4. Click **"Add secret"**

## 🔑 Creating a Personal Access Token (if needed)

If you don't have a personal access token with the right permissions:

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Note**: `PyCharmMiscProject Actions Token`
4. **Expiration**: Choose an appropriate expiration (e.g., 90 days)
5. **Scopes**: Select these permissions:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `issues` (Full control of issues)
6. Click **"Generate token"**
7. **Copy the token** (you won't see it again!)

## ✅ What This Fixes

- **Issue Creation**: Your workflows can now create issues automatically
- **Permission Error**: Resolves the "Resource not accessible by integration" error
- **Token Security**: Uses your personal token instead of the limited GITHUB_TOKEN

## 🔍 Alternative: Disable Issue Creation

If you prefer not to use a personal access token, the workflow will:
- ✅ Continue to run all tests
- ✅ Generate test reports
- ✅ Upload artifacts
- ⚠️ Skip creating GitHub issues (but won't fail)

## 🚀 Test the Fix

1. Add the secret as described above
2. Push a change to trigger the workflow
3. Check the workflow logs to see if issue creation works

## 📝 Notes

- The token is stored securely as a repository secret
- Only repository owners and collaborators can see/use the secret
- The workflow will continue to work even if the token is missing
- You can revoke the token anytime from GitHub settings

---
*This guide was created to fix the GitHub Actions permission issue you encountered.* 