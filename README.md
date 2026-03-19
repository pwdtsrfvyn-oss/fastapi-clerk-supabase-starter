# LaunchStack

**Deploy a production-ready FastAPI backend in 60 seconds.**

FastAPI + Clerk Auth + Supabase + Redis on Railway. Built by Altora Labs.

## What is LaunchStack?

LaunchStack is a production-ready Python API backend pre-wired with everything you need:

- **Clerk JWT Auth** -- SwiftUI, React, Next.js, React Native, Flutter, Vue
- **Supabase PostgreSQL** -- full database with REST API and Row Level Security
- **Redis Caching** -- sub-millisecond responses, auto-provisioned on Railway
- **API Docs** -- interactive Swagger UI at /docs
- **Health Checks** -- pre-configured at /health
- **Example CRUD** -- working auth + cache + DB patterns to copy

## Quick Start

1. Deploy to Railway
2. Set your environment variables
3. Your API is live

## Environment Variables

SUPABASE_URL -- Your Supabase project URL
SUPABASE_SERVICE_KEY -- Service role key
CLERK_JWKS_URL -- Clerk JWKS endpoint
REDIS_URL -- Auto-injected by Railway

## API Endpoints

GET /health -- Health check
GET /api/v1/items -- List items (cached, auth required)
POST /api/v1/items -- Create item (auth required)
DELETE /api/v1/items/{id} -- Delete item (auth required)

## Setup

1. Create a free Clerk account and copy your JWKS URL
2. Create a free Supabase project
3. Run supabase_schema.sql in the SQL Editor
4. Deploy to Railway and set env vars

## License

MIT -- Built by Altora Labs LLC
