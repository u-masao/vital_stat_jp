#!/bin/bash -eux

CURRENT_BUILD_NO=`cat BUILD_NO`
expr ${CURRENT_BUILD_NO} + 1 > BUILD_NO

CURRENT=0\.1\.${CURRENT_BUILD_NO}
NEXT=0\.1\.`expr ${CURRENT_BUILD_NO} + 1`

echo version change $CURRENT to $NEXT

cat <<EOF | while read FILE
pyproject.toml
tests/test_vital_statistics_jp.py
vital_statistics_jp/__init__.py
EOF

do
    echo $FILE
    sed -i "s/${CURRENT}/${NEXT}/" $FILE
    git add $FILE
done 

git add BUILD_NO
git status
git diff --cached | cat
git commit -m '[update] package version'
git tag -a v${NEXT} -m 'new version'

poetry build 

echo git push
echo git push origin v${NEXT}
echo poetry publish
