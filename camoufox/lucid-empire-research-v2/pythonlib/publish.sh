rm -rf ./dist
rm -rf ./lucid_browser/*.mmdb
rm -rf ./lucid_browser/*.png

vermin . --eval-annotations --target=3.8  --violations lucid_browser/ || exit 1

python -m build
twine check dist/*

read -p "Confirm publish? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    twine upload dist/*
fi
