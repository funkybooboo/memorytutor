# Deployment Guide

This guide covers deploying MemoryTutor, a multi-language AI tutoring application, in various environments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Considerations](#production-considerations)
- [Backup and Recovery](#backup-and-recovery)
- [Monitoring](#monitoring)

## Local Development

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- (Optional) Mem0 API key for hosted mode

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd memorytutor
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the application**
   ```bash
   python tutor.py
   ```

### Development Workflow

For local development with self-hosted mode:
- Set `MEM0_MODE=self-hosted` in `.env`
- Set `USE_DOCKER_QDRANT=false` in `.env`
- Data will be stored in `.qdrant_data/` directory
- This directory persists between runs

## Docker Deployment

### Prerequisites

- Docker 20.10 or higher
- Docker Compose 2.0 or higher

### Quick Start

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **For self-hosted mode**, ensure these settings in `.env`:
   ```bash
   MEM0_MODE=self-hosted
   # USE_DOCKER_QDRANT is automatically set to true in docker-compose.yml
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **View logs**
   ```bash
   docker-compose logs -f memorytutor
   ```

5. **Interact with the tutor**
   ```bash
   docker attach memorytutor-app
   ```

   Press `Ctrl+P` then `Ctrl+Q` to detach without stopping the container.

6. **Stop services**
   ```bash
   docker-compose down
   ```

### Docker Architecture

The Docker setup consists of two services:

1. **qdrant**: Qdrant vector database
   - Stores memory vectors
   - Persistent data via Docker volume
   - Health checks ensure it's ready before app starts

2. **memorytutor**: Python application
   - Waits for Qdrant to be healthy
   - Interactive terminal support
   - Reads configuration from `.env`

### Data Persistence

All memory data is stored in a named Docker volume:

```bash
# List volumes
docker volume ls | grep qdrant

# Inspect volume
docker volume inspect memorytutor_qdrant_data

# Backup volume (see Backup section below)
```

## Production Considerations

### Security

1. **Environment Variables**
   - Never commit `.env` to version control
   - Use secrets management in production (e.g., Docker secrets, Kubernetes secrets)
   - Rotate API keys regularly

2. **Network Security**
   - In production, don't expose Qdrant ports (6333, 6334) publicly
   - Use internal Docker networks
   - Consider adding authentication to Qdrant

3. **Resource Limits**

   Add resource limits to `docker-compose.yml`:
   ```yaml
   memorytutor:
     deploy:
       resources:
         limits:
           cpus: '1.0'
           memory: 1G
         reservations:
           cpus: '0.5'
           memory: 512M
   ```

### Scaling

**Qdrant Scaling:**
- For production workloads, consider Qdrant Cloud
- Or deploy Qdrant cluster with multiple nodes
- Configure appropriate memory limits based on collection size

**Application Scaling:**
- MemoryTutor is designed for single-user interactive sessions
- For multi-user support, use different `USER_ID` values
- Consider adding a web interface for concurrent users

### High Availability

For production deployments:

1. **Qdrant Persistence**
   - Use external storage (NFS, cloud volumes) for Qdrant data
   - Configure automatic backups

2. **Health Checks**
   ```yaml
   memorytutor:
     healthcheck:
       test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
       interval: 30s
       timeout: 10s
       retries: 3
   ```

3. **Restart Policies**
   ```yaml
   memorytutor:
     restart: unless-stopped
   ```

### Using Hosted Mem0 in Production

For simpler production deployments:

1. Set `MEM0_MODE=hosted` in `.env`
2. Provide `MEM0_API_KEY`
3. Remove Qdrant service from `docker-compose.yml` or don't start it
4. All memory management handled by Mem0 Platform

## Backup and Recovery

### Backing Up Qdrant Data

**Docker Volume Backup:**

```bash
# Stop the application
docker-compose stop memorytutor

# Create backup directory
mkdir -p backups

# Backup volume to tarball
docker run --rm \
  -v memorytutor_qdrant_data:/source:ro \
  -v $(pwd)/backups:/backup \
  alpine \
  tar czf /backup/qdrant-backup-$(date +%Y%m%d-%H%M%S).tar.gz -C /source .

# Restart application
docker-compose start memorytutor
```

**Automated Backups:**

Create a cron job for daily backups:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /path/to/memorytutor && ./scripts/backup-qdrant.sh
```

### Restoring from Backup

```bash
# Stop services
docker-compose down

# Remove existing volume
docker volume rm memorytutor_qdrant_data

# Create new volume
docker volume create memorytutor_qdrant_data

# Restore data
docker run --rm \
  -v memorytutor_qdrant_data:/target \
  -v $(pwd)/backups:/backup \
  alpine \
  tar xzf /backup/qdrant-backup-YYYYMMDD-HHMMSS.tar.gz -C /target

# Restart services
docker-compose up -d
```

### Backup Hosted Mem0 Data

For hosted mode, Mem0 Platform handles backups. You can export memories using:

```python
from mem0 import MemoryClient
client = MemoryClient(api_key="your-key")
memories = client.get_all(user_id="your-user")
# Save to file for backup
```

## Monitoring

### Application Logs

**Docker:**
```bash
# View real-time logs
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# Export logs to file
docker-compose logs > app.log
```

**Local:**
Standard output from `python tutor.py`

### Qdrant Monitoring

Access Qdrant dashboard (when running):
- Local: http://localhost:6333/dashboard
- Docker: http://localhost:6333/dashboard

**Health Check:**
```bash
curl http://localhost:6333/healthz
```

**Collection Stats:**
```bash
curl http://localhost:6333/collections/spanish_tutor_session
```

### Metrics to Monitor

1. **Memory Usage**
   - Qdrant memory consumption
   - Number of vectors stored
   - Collection size

2. **API Usage**
   - OpenAI API calls
   - Response times
   - Error rates

3. **Disk Space**
   - Qdrant data directory size
   - Docker volume usage
   - Log file sizes

### Alerting

Set up alerts for:
- Qdrant service down
- Disk space > 80% usage
- OpenAI API errors
- Memory limit reached

## Troubleshooting

### Common Issues

**Qdrant Connection Failed:**
```bash
# Check if Qdrant is running
docker-compose ps

# Check Qdrant logs
docker-compose logs qdrant

# Verify health
curl http://localhost:6333/healthz
```

**Memory Persistence Issues:**
```bash
# Verify volume exists
docker volume ls | grep qdrant

# Check volume mount
docker inspect memorytutor-qdrant | grep -A 10 Mounts
```

**Port Conflicts:**
```bash
# Check if ports are in use
lsof -i :6333
lsof -i :6334

# Change ports in docker-compose.yml if needed
```

## Migration

### From Local to Docker

1. Backup local Qdrant data: `tar czf qdrant-backup.tar.gz .qdrant_data/`
2. Set up Docker environment
3. Extract backup into Docker volume (see Restore section)
4. Update `.env` with `USE_DOCKER_QDRANT=true`
5. Start Docker services

### From Self-Hosted to Hosted

1. Export all memories from local Qdrant
2. Set `MEM0_MODE=hosted` in `.env`
3. Add `MEM0_API_KEY`
4. Optionally import memories to Mem0 Platform
5. Stop Qdrant service

## Support

For issues and questions:
- Check troubleshooting section in main README
- Review configuration documentation in configuration.md
- Submit issues on GitHub repository
