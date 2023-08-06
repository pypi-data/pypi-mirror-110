cd ..;
rm -rf dist;
flit build --format wheel;
flit build --format sdist;
twine upload --repository testpypi dist/*
