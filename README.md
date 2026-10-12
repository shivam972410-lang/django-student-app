# Campus Student Portal

A responsive Django student directory with login, search, and student create, edit, and delete pages. The project uses the existing `config` project, `students` app, and local SQLite database.

## Run locally

From the project directory, use the existing virtual environment:

```sh
source venv/bin/activate
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/login/> and sign in with the existing `suraj` superuser account and its current password. The application does not create or reset local accounts. The admin site is at <http://127.0.0.1:8000/admin/>.

To install dependencies into the existing environment if needed, run `pip install -r requirements.txt`. `migrate` applies the pending `students.0001_initial` migration without resetting the existing SQLite database or auth accounts.

## Render deployment with PostgreSQL

The included `render.yaml` defines a Render Blueprint with a Django web service and managed PostgreSQL database. It uses environment variables for the secret key, database URL, allowed host, and CSRF origin. SQLite remains the local development default. The local `db.sqlite3`, virtual environment, and environment files are excluded by `.gitignore`.

1. Commit and push the project to a Git provider supported by Render. Do not add `db.sqlite3`, `venv/`, `.env`, or secrets.
2. In Render, choose **New → Blueprint**, connect the repository, and review the resources and current plan pricing before applying the Blueprint.
3. Render installs `requirements.txt`, collects static files, runs migrations against PostgreSQL, and starts Gunicorn.
4. In the deployed service shell, create a production administrator with `python manage.py createsuperuser`. The local `suraj` account belongs to SQLite and is not copied to PostgreSQL.
5. Open `https://campus-student-portal.onrender.com/login/` (or the custom service hostname if changed) and sign in with the new production account. If the hostname changes, update `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` in the Render service environment.

Render Blueprint reference: <https://render.com/docs/blueprint-spec>.
