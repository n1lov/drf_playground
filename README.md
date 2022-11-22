###  My simple template for a Django + DRF, JWT, grappelli, Swagger/OpenAPI stack (development environment only)


Build / Run:  `sh build.sh`

Build / Run without collecting static files: `docker-compose -f docker-compose.yml up`

**Useful links and commands:**

Create superuser: 

`docker-compose -f docker-compose.yml exec backend python manage.py createsuperuser` or `docker exec -it backend /bin/bash` + `python manage.py createsuperuser`

Grappeli admin page `http://localhost:8000/en/backend/admin/`

DRF auth page `http://localhost:8000/en/api-auth/`

Available API list `http://localhost:8000/en/api-auth/login/en/api/v1/`

Swagger url `http://localhost:8000/api/swagger/`

OpenAPI docs `http://localhost:8000/api/redoc/`

---

**Production version difference (possible next steps):**

Django related:

* add logging
* move user type into JWT payload, blacklist used tokens
* split project into 2-3 versions: development and production (based on the `env.backend.env` -> `PROJECT_ENV` value) -- different settings, storage type, CI/CD flow, and so on
* add i18n translation (`LocaleMiddleware` + `LOCALE_PATHS` in settings)


Infrastructure related:

* add AWS RDS, S3 storage support for /media/ folder (local/aws -- based on the `PROJECT_ENV` value)
* RedisCache for caching, Celery for tasks, Sentry/Datadog for logs, Graphana for monitoring
* copy static to the nginx container instead of using volume
* update gunicorn and nginx config (increase the number of workers and max-requests for gunicorn, and well, set kind of entirely different config for nginx -- add https support and security headers, increase worker_processes, update max body/file size, timeouts, and so on)
* CI/CD : test, build, and deploy stages, product versioning, blue-green deployment. Keywords: Ansimble (playbooks), terraform, AWS (S3, ECR, VPC, EC2, KMS, IGW, RDS, MQ, LB)
