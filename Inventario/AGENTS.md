# AGENTS.md

## 1. Build, Lint, and Test Commands

### Environment Setup
- Create virtual env: `python -m venv venv`
- Activate:
  - Linux/macOS: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

### Build
- (Optional) Build package: `python setup.py build`

### Linting
- Flake8: `flake8 .`
- Black check: `black --check .`
- Isort check: `isort --check-only .`
- Mypy type check: `mypy .`

### Testing
- Run all tests: `pytest`
- Run single test:
  ```
  pytest path/to/test_file.py::TestClass::test_method
  ```

### Django Commands (if applicable)
- Make migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Run development server: `python manage.py runserver`

## 2. Code Style Guidelines

### Formatting
- Use Black with default line length (88).
- Auto-format on save via editor integration.

### Imports
- Order:
  1. Standard library
  2. Third-party
  3. Local application
- Separate groups with one blank line.
- Prefer absolute imports; avoid `from module import *`.

### Typing
- Annotate all public functions, methods, and module-level variables.
- Use `Optional[...]` for nullable types.
- Use `TypedDict`, `Protocol`, or `@dataclass` for structured data.
- Enforce types with `mypy --strict`.

### Naming Conventions
- Modules/packages: `snake_case`.
- Classes: `PascalCase`.
- Functions/variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Private names: prefix with `_`.

### Error Handling
- Catch specific exceptions; avoid bare `except:`.
- Use context managers (`with`) for files and resources.
- Log exceptions with `logger.exception()`.

### Logging
- Use Python `logging` module.
- Configure via `logging.config.dictConfig`.
- Use structured/JSON output in production.

## 3. Cursor Rules

_No `.cursor/rules/` or `.cursorrules` directory detected._

## 4. Copilot Rules

_No `.github/copilot-instructions.md` file detected._
