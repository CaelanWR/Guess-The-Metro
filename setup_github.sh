#!/bin/bash
# Automated Git Setup Script for Guess the Metro
# This script initializes git, commits files, and pushes to GitHub

echo "🚀 Guess the Metro - GitHub Setup Script"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed. Please install git first."
    echo "   Download from: https://git-scm.com/downloads"
    exit 1
fi

# Get user information
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter your repository name (default: guess-the-metro): " REPO_NAME
REPO_NAME=${REPO_NAME:-guess-the-metro}

read -p "Enter your name for git commits: " GIT_NAME
read -p "Enter your email for git commits: " GIT_EMAIL

echo ""
echo "📝 Configuration Summary:"
echo "   GitHub Username: $GITHUB_USERNAME"
echo "   Repository Name: $REPO_NAME"
echo "   Git Name: $GIT_NAME"
echo "   Git Email: $GIT_EMAIL"
echo ""
read -p "Is this correct? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ Setup cancelled."
    exit 1
fi

# Configure git
echo ""
echo "⚙️  Configuring git..."
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

# Initialize git repository
echo "📁 Initializing git repository..."
if [ -d ".git" ]; then
    echo "   ⚠️  Git repository already exists. Skipping initialization."
else
    git init
    echo "   ✅ Git initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "   ⚠️  Warning: .gitignore not found. Creating one..."
    cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.Python
env/
venv/
.streamlit/secrets.toml
.DS_Store
*.log
EOF
    echo "   ✅ .gitignore created"
fi

# Stage all files
echo "📦 Staging files..."
git add .
echo "   ✅ Files staged"

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Guess the Metro game"
echo "   ✅ Commit created"

# Create main branch
echo "🌿 Setting up main branch..."
git branch -M main
echo "   ✅ Main branch set"

# Add remote origin
echo "🔗 Adding remote repository..."
REMOTE_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
git remote add origin "$REMOTE_URL" 2>/dev/null || git remote set-url origin "$REMOTE_URL"
echo "   ✅ Remote added: $REMOTE_URL"

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
echo "   You may be prompted for your GitHub credentials."
echo "   If using a personal access token, enter it as your password."
echo ""

if git push -u origin main; then
    echo ""
    echo "✅ SUCCESS! Your repository is now on GitHub!"
    echo ""
    echo "📍 Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "Next steps:"
    echo "1. Visit your repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "2. Go to https://share.streamlit.io to deploy your app"
    echo "3. Sign in with GitHub and select your repository"
    echo "4. Set main file to: app.py"
    echo "5. Click Deploy!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo ""
    echo "1. Repository doesn't exist on GitHub"
    echo "   → Create it at: https://github.com/new"
    echo "   → Name it: $REPO_NAME"
    echo "   → Make it PUBLIC (required for free Streamlit)"
    echo "   → DO NOT initialize with README"
    echo ""
    echo "2. Authentication failed"
    echo "   → You may need a Personal Access Token"
    echo "   → Create one at: https://github.com/settings/tokens"
    echo "   → Use the token as your password when pushing"
    echo ""
    echo "3. Remote already exists"
    echo "   → Run: git remote remove origin"
    echo "   → Then run this script again"
    echo ""
    echo "To try pushing again manually:"
    echo "   git push -u origin main"
    exit 1
fi
