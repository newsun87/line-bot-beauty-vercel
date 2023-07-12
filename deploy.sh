sudo rm -rf .git
echo "# line-bot-beauty-vercel" > README.md
git init
git add .
git commit -m "update project"  
git branch -M main
git remote add origin git@github.com:newsun87/line-bot-beauty-vercel.git
git push -u origin main
