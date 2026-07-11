# Architecture

## Deployment boundary

NOVA uses two independently deployable processes:

1. A static web client hosted by Cloudflare Pages.
2. A Python 3.12 service running on the Windows workstation.

The local service owns SQLite data, model access, microphones, cameras, files,
and operating-system automation. The static client owns presentation and sends
authenticated requests to explicitly configured service origins.

## Design principles

- Feature modules depend on stable core interfaces, not on each other.
- Configuration enters through validated environment variables.
- Secrets and user data remain outside version control.
- Logs are structured in production and readable during local development.
- Automation actions require explicit authorization and least privilege.
- External AI providers are adapters so local and hosted models remain
  replaceable.

## Planned layers

- API: HTTP/WebSocket transport, request validation, and authentication.
- Application: use cases and orchestration.
- Domain: provider-independent models and policies.
- Infrastructure: SQLite, AI engines, voice, vision, browser, and Windows APIs.

