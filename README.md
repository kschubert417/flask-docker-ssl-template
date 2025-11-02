# Flask Application Factory Project Setup

## Project Initialization
   Run through these steps the first time setting up this project

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd flask-docker-ssl-template
   ```

2. **Update the domain in the conf/Caddyfile**
   - Replace `yourdomain.com` with whatever your domain name is

3. **Set Up Environment Variables**
   - Copy the `.example_env` file to `.env`:
     ```bash
     cp .example_env .env
     ```
   - Update the `.env` file with your specific configuration values (e.g., `FLASK_SECRET_KEY`, `MYSQL_USER`, `MYSQL_PASSWORD`).

4. **Build and Start Docker Containers**
   ```bash
   docker-compose build
   docker-compose up
   ```

5. **Initialize the Database**
   - Create initial migration:
     ```bash
     docker exec -it flask-docker-ssl-template-app_factory_web-1 bash -c "flask db migrate -m 'initial tables'"
     ```
   - Verify database connection:
     ```bash
     docker exec -it flask-docker-ssl-template-app_factory_web-1 bash -c "flask db current"
     ```
     If successful, you will see output like:
     ```
     INFO  [alembic.env] Running Alembic with active Flask app context.
     INFO  [alembic.runtime.migration] Context impl MySQLImpl.
     INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
     ```
   - Apply migrations:
     ```bash
     docker exec -it flask-docker-ssl-template-app_factory_web-1 bash -c "flask db upgrade"
     ```

6. **Verify Database State**
   ```bash
   docker exec -it flask-docker-ssl-template-app_factory_web-1 bash -c "flask db current"
   ```
   You should see a revision hash (e.g., `Current revision(s): 7d365e2fadd9`).

7. **Run the `create-admin` Command**
   ```bash
   docker exec -it flask-docker-ssl-template-app_factory_web-1 bash -c "flask create-admin"
   ```
   - Follow the prompts to enter the admin user's email, first name, last name, and password.
   - If the user already exists, you will see a message indicating so.

## Project Maintenance
   Follow these steps to make updates to the database
1. **Generate new migration script**
   ```bash
   docker compose exec flask-docker-ssl-template-app_factory_web-1 sh -c "cd /app/migrations && alembic revision --autogenerate -m 'comment about change'"
   ```

2. **Apply changes to the database**
   ```bash
   docker compose exec flask-docker-ssl-template-app_factory_web-1 sh -c "cd /app/migrations && alembic upgrade head"
   ```

## Running the Test Suite

1. **Access the Web Container**
   ```bash
   docker exec -it flask-docker-ssl-template-app_factory_web-1 bash
   ```

2. **Run Tests**
   - To run all tests:
     ```bash
     pytest -v tests/
     ```
   - To run a specific test file:
     ```bash
     pytest tests/unit/test_auth.py
     ```
   - To generate a coverage report:
     ```bash
     pytest --cov=app
     ```

3. **Exit the Container**
   ```bash
   exit
   ```

---
