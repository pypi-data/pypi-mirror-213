current_version="0.3.0"
bump_type="patch" # major / minor / patch


tag_name=v$current_version

####
# Build changelog
####


towncrier build
git commit -m "Building changelog"

####
# Bumping version number
####

bump2version --current-version $current_version $bump_type SBART/__init__.py setup.py --allow-dirty
git add pyproject.tom
git add SBART/__init__.py
git commit -m "new sBART version"

####
# Creating the tag
####

git tag -a v1.4 -m "New sBART release"

####
# Pushing the changes
####

git push --tags
pypi-AgENdGVzdC5weXBpLm9yZwIkMDQ3YjJkMGEtNGY2ZS00MGJlLTgzNTItNTViNGM4NGE1ZDkwAAIqWzMsIjZjODZhNGYxLWFjYjctNDA0MS04NTU1LTgzMjhlODk4ZmU4MCJdAAAGIHtkMaiMkN6Iz8q25Id3CK2N28cMop_dtpZbpH7z3UDX
####
# Finally, publish the package
####

poetry publish --build -u Kamuish
