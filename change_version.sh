#!/bin/bash -eux

BUILD_NO=6

OLD=0\.1\.${BUILD_NO}
NEW=0\.1\.`expr ${BUILD_NO} + 1`

cat <<EOF | while read FILE
pyproject.toml
tests/test_vital_statistics_jp.py
vital_statistics_jp/__init__.py
EOF

do
    echo $FILE
    sed -i "s/${OLD}/${NEW}/" $FILE
    git add $FILE
done 

git status
git diff --cached | cat
echo git commit '[update] package version'
echo git tag -a v${NEW} -m 'new version'
