# CI/CD and auto-deploy

The repository now deploys automatically from GitHub Actions when code is pushed to the `branch-for-deploy` branch.

## What the workflow does

- runs backend tests on every push and pull request;
- runs frontend production build on every push and pull request;
- deploys only after both checks pass;
- connects to the server over SSH and runs `./deploy.sh <branch>`.

## Required GitHub secrets

Configure these repository secrets before using auto-deploy:

- `CI_DATABASE_URL`
- `CI_MAIL_PASSWORD`
- `CI_MAIL_SERVER`
- `CI_MAIL_PORT`
- `CI_MAIL_USERNAME`
- `CI_MAIL_DEFAULT_SENDER`
- `DEPLOY_HOST`
- `DEPLOY_PORT`
- `DEPLOY_USER`
- `DEPLOY_PATH`
- `DEPLOY_SSH_KEY`
- `DEPLOY_KNOWN_HOSTS`

## Secret values for deploy

- `DEPLOY_HOST`: server hostname or IP.
- `DEPLOY_PORT`: SSH port, usually `22`.
- `DEPLOY_USER`: Linux user used for deploy.
- `DEPLOY_PATH`: absolute path to the checked out project on the server.
- `DEPLOY_SSH_KEY`: private SSH key that can access the server.
- `DEPLOY_KNOWN_HOSTS`: output of `ssh-keyscan -H <host>`.

Example:

```bash
ssh-keyscan -H your-domain.example
```

## Server expectations

The remote server should already have:

- Docker and Docker Compose plugin installed;
- this repository cloned into `DEPLOY_PATH`;
- a valid `.env` file in the project root;
- permissions to run `docker compose`;
- `deploy.sh` available in the repository root.

## Trigger rule

Auto-deploy runs only for:

- push to `branch-for-deploy`

If you want production deploys from another branch later, update the branch in [ci.yml](/C:/Users/goshr/PycharmProjects/ukno-hisory/.github/workflows/ci.yml:1) and, if needed, the default branch name in [deploy.sh](/C:/Users/goshr/PycharmProjects/ukno-hisory/deploy.sh:1).
