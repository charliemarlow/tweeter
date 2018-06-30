
# move API keys
mv profiles ../profiles

# upload to git
git add .
git commit -m "$1"
git push origin

# add profiles back
mv ../profiles profiles