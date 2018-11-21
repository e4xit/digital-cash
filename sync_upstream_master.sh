#!/usr/bin/env fish

# show current branch
set -g git_current_branch (git branch | grep \* | cut -d ' ' -f2)

git fetch upstream;
git checkout master;
git merge upstream/master;

# switch back to previous branch
git checkout $git_current_branch
