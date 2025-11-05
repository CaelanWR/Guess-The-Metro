# 🚀 Quick Start: Deploy in 10 Minutes

This guide will get your Guess the Metro app deployed to Streamlit Cloud as quickly as possible.

## Prerequisites

- [ ] GitHub account ([sign up here](https://github.com))
- [ ] Git installed on your computer ([download here](https://git-scm.com/downloads))
- [ ] Your app files ready (app.py, game_data folder, city-data-chart.png)

## Step 1: Prepare Your Files (2 minutes)

1. **Download the setup files** I created for you:
   - `requirements.txt`
   - `.gitignore`
   - `README.md`

2. **Put everything in one folder** with this structure:
   ```
   your-project/
   ├── app.py                 ← Your main Python file
   ├── requirements.txt       ← Downloaded
   ├── .gitignore            ← Downloaded
   ├── README.md             ← Downloaded
   ├── city-data-chart.png   ← Your image
   └── game_data/            ← Your data folder
       ├── memphis/
       ├── charlotte/
       ├── dc/
       ├── pittsburgh/
       └── houston/
   ```

3. **Rename your main file to `app.py`** (if it has a different name)

## Step 2: Create GitHub Repository (2 minutes)

### Option A: Automated (Easiest)

**Mac/Linux:**
```bash
cd /path/to/your-project
chmod +x setup_github.sh
./setup_github.sh
```

**Windows:**
```cmd
cd C:\path\to\your-project
setup_github.bat
```

Follow the prompts and you're done! Skip to Step 3.

### Option B: Manual

1. Go to [github.com/new](https://github.com/new)
2. Name it: `guess-the-metro`
3. Make it **PUBLIC** ← Important!
4. **DO NOT** check "Initialize with README"
5. Click "Create repository"

## Step 3: Push to GitHub (3 minutes)

Open terminal in your project folder:

```bash
# Configure git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Initialize and push
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/guess-the-metro.git
git push -u origin main
```

**Need help with authentication?** See the troubleshooting section below.

## Step 4: Deploy to Streamlit (3 minutes)

1. **Go to:** [share.streamlit.io](https://share.streamlit.io)

2. **Click:** "Sign in with GitHub"

3. **Click:** "New app"

4. **Fill in:**
   - Repository: `YOUR_USERNAME/guess-the-metro`
   - Branch: `main`
   - Main file: `app.py`

5. **Click:** "Deploy!"

6. **Wait 2-3 minutes** while it builds

7. **Done!** Your app is live! 🎉

## Your App URL

Your app will be at:
```
https://YOUR-APP-NAME.streamlit.app
```

## Common Issues & Quick Fixes

### 🔴 "Repository not found" error
**Fix:** Make sure your repository is PUBLIC, not private.
- Go to GitHub → Your repo → Settings → Danger Zone → Change visibility

### 🔴 Git authentication fails
**Fix:** Use a Personal Access Token:
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select `repo` scope
4. Copy the token
5. When prompted for password, paste the token

### 🔴 App crashes with "File not found"
**Fix:** Check your file paths are relative:
```python
# ✅ Good - relative path
data_path = 'game_data/memphis/industry.csv'

# ❌ Bad - absolute path
data_path = '/Users/you/project/game_data/memphis/industry.csv'
```

### 🔴 "ModuleNotFoundError"
**Fix:** Your `requirements.txt` is missing a dependency. Add it:
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
# Add any other missing modules here
```
Then commit and push:
```bash
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

### 🔴 Images not showing
**Fix:** Make sure `city-data-chart.png` is in the root folder, not in a subfolder.

## Updating Your App

Made changes? Deploy them instantly:

```bash
git add .
git commit -m "Update: description of changes"
git push
```

Streamlit Cloud will automatically redeploy within 1-2 minutes!

## Testing Before Deployment

Always test locally first:

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Visit `http://localhost:8501` to test.

## Next Steps

1. ✅ **Test your live app** - Try all features
2. ✅ **Share the URL** - Send to friends/colleagues
3. ✅ **Monitor usage** - Check Streamlit Cloud dashboard
4. ✅ **Update README** - Add your live app URL

## Resources

- **Your files:** All setup files are in the outputs folder
- **Detailed guide:** See `DEPLOYMENT_GUIDE.md` for more information
- **Checklist:** Use `DEPLOYMENT_CHECKLIST.md` to track progress
- **Git commands:** See `GIT_QUICK_REFERENCE.md` for common commands
- **Get help:** [Streamlit Community Forum](https://discuss.streamlit.io)

## Streamlit Cloud Features

Your free tier includes:
- 1 GB RAM
- 1 CPU core
- Unlimited apps (1 public app always-on)
- Automatic SSL (https)
- Custom domain support
- GitHub integration

## Pro Tips

1. **Use descriptive commit messages** - Makes tracking changes easier
2. **Commit frequently** - Small commits are better than big ones
3. **Test locally first** - Catch bugs before deploying
4. **Monitor the logs** - Check for warnings or errors
5. **Enable caching** - Makes your app faster (already done in your code!)

---

## 🎉 Success Checklist

- [ ] Files organized correctly
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] App deployed on Streamlit Cloud
- [ ] App is accessible via URL
- [ ] All features tested and working
- [ ] URL shared with others

---

**Questions?** Open an issue on your GitHub repository or ask in the [Streamlit Forum](https://discuss.streamlit.io).

**Congratulations!** 🎊 Your app is now live and accessible to anyone in the world!
