# Git and GitHub Practice

This exercise uses a small Python file to practise checking Git status, staging changes, committing, and pushing to GitHub.

## Project file

- `hello.py` - simple Python program

## Open the project folder

In PowerShell:

```powershell
cd "C:\Users\Trainer\Downloads\AI TRAINIG\Day2\git_hub_exercise\GIT_exercise"
```

## First-time setup

If this folder is not already a Git repository, initialize it:

```powershell
git init
git branch -M main
```

Check the current state:

```powershell
git status
```

Stage the project files, then check what will be committed:

```powershell
git add .
git status
```

Create the first commit:

```powershell
git commit -m "Add hello program"
```

Connect the local repository to GitHub. Run `git remote add` only if no `origin` remote exists:

```powershell
git remote add origin https://github.com/Deepikakanchi/day2.git
```

If `origin` already exists but its URL is incorrect, update it instead:

```powershell
git remote set-url origin https://github.com/Deepikakanchi/day2.git
```

Verify the remote and push the `main` branch:

```powershell
git remote -v
git push -u origin main
```

## Push a later change

After editing `hello.py` or another project file, stage, commit, and push the changes:

```powershell
git status
git add .
git status
git commit -m "Update hello program"
git push
```

## Common issues

- **`No configured push destination`**: add or correct the `origin` remote, then push with `git push -u origin main`.
- **`remote origin already exists`**: use `git remote set-url origin <repository-url>` instead of adding it again.
- **`Repository not found`**: check the repository URL and ensure the GitHub account has permission to access it.
- **`nothing to commit`**: there are no staged changes. Edit or create a file, then run `git add .` and commit.

