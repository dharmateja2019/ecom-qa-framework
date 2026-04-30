# Interview Notes & Learnings

## Jenkins Learnings

- Jenkins uses `archiveArtifacts`, not `upload-artifact`
- Parameterized builds reduce multiple jobs
- Docker path issues may require PATH updates
- macOS Docker may need `DOCKER_HOST`

## GitHub Actions Learnings

- Each job runs on a fresh runner
- Separate jobs need separate artifact uploads
- Runners are ephemeral
- `needs:` creates job dependency flow
- Matrix strategy useful for multi-suite execution

## Docker Learnings

- Dockerfile builds runtime image
- docker-compose defines runtime services
- Volumes persist reports/results
- Same compose file usable locally + CI

## Testing Learnings

- Smoke = critical fast checks
- Regression = broad validation
- API tests should dominate pyramid
- UI tests for business flows
- DB tests validate persistence

## CI Design Thinking

GitHub Actions = automated repo CI
Jenkins = enterprise orchestration
Docker = consistent execution layer

## Real Issues Solved

- Jenkinsfile not found
- Docker command not found in Jenkins
- Artifact path mismatch
- Container report persistence
- CI warning handling

## Strong Interview Answer

“I built a QA framework executable across local, GitHub Actions, and Jenkins using Dockerized infrastructure with selective smoke/regression/API/UI/DB execution.”
