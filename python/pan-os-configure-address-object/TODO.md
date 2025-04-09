# TODO List: Panorama Address Object Creator

## Phase 1: Project Setup & Foundation

- [ ] Initialize Git repository for version control.
- [ ] Create a Python virtual environment (e.g., using `venv`).
- [ ] Activate the virtual environment.
- [ ] Install core dependencies:
  - [ ] `pip install python==3.10.*` (or target specific version 3.10-3.12)
  - [ ] `pip install "pydantic>=2.11,<3.0"`
  - [ ] `pip install "pan-os-python>=1.12.1,<1.13.0"`
- [ ] Install development dependencies:
  - [ ] `pip install ruff flake8 mypy ipython`
- [ ] Create `requirements.txt` for core dependencies.
- [ ] Create `dev-requirements.txt` (or similar) for development dependencies.
- [ ] Configure `ruff` (e.g., in `pyproject.toml` or `.ruff.toml`).
- [ ] Configure `flake8` (e.g., in `.flake8` - if needed alongside Ruff).
- [ ] Configure `mypy` (e.g., in `mypy.ini` or `pyproject.toml`).
- [ ] Define basic project structure (e.g., `src/panorama_creator/`, `tests/`, `config/`, `scripts/`, `.gitignore`).
- [ ] Create the main entry point script (e.g., `src/panorama_creator/main.py` or `scripts/run_creator.py`).

## Phase 2: Core Data Handling

- [ ] Define the Pydantic model `AddressObjectInput` for input data structure and validation (Ref: PRD Section 7). Include field constraints (e.g., `name` length/pattern, `description` length).
- [ ] Implement function/class to read the input file (Decide on JSON or YAML, implement parser).
- [ ] Add error handling for file not found or file read errors (Ref: PRD Section 8).
- [ ] Implement function/class to parse and validate the list of objects from the input file using the Pydantic model.
- [ ] Add error handling to report detailed validation errors from Pydantic (Ref: PRD Section 8). Decide on fail-fast vs. report-all approach for validation errors.

## Phase 3: Panorama Interaction Logic

- [ ] Implement function/class to securely retrieve Panorama connection details (hostname, API key, device group) (Ref: PRD FR9, NFR1). Start with environment variables.
- [ ] Implement function/class to establish connection to Panorama using `pan-os-python`'s `Panorama` class (Ref: PRD FR1).
- [ ] Add error handling for connection failures (e.g., DNS resolution, network timeout) (Ref: PRD Section 8).
- [ ] Add error handling for authentication failures (invalid API key) (Ref: PRD Section 8).
- [ ] Implement function to check if an `AddressObject` exists by name within the target Device Group using `panos.objects.AddressObject.refreshall()` or similar (Ref: PRD FR4). Handle potential API errors.
- [ ] Implement function to create a _single_ `AddressObject` of type 'ip-netmask' using `panos.objects.AddressObject` and its `create()` method (Ref: PRD FR5). Ensure it's added to the correct Device Group context. Handle potential API errors during creation (Ref: PRD Section 8).
- [ ] Implement function to trigger a Panorama commit using `panorama.commit()` (Ref: PRD FR7).
- [ ] Add error handling for commit failures, capturing job ID and error messages if possible (Ref: PRD Section 8).

## Phase 4: Application Workflow & CLI

- [ ] Set up command-line argument parsing (e.g., using `argparse` or `typer`) (Ref: PRD NFR3):
  - [ ] Required argument for input file path.
  - [ ] Optional flag for controlling commit (e.g., `--no-commit`) (Ref: PRD FR8).
  - [ ] Optional argument for configuration file path (if implementing config file).
  - [ ] Standard `--help` flag generation.
- [ ] Develop the main script execution flow:
  - [ ] Parse CLI arguments.
  - [ ] Load configuration (from env vars/config file).
  - [ ] Establish Panorama connection.
  - [ ] Read and validate the input file data.
  - [ ] Iterate through the validated address object definitions.
  - [ ] For each object:
    - [ ] Check if it exists on Panorama (FR4).
    - [ ] If exists, log warning and skip (FR6).
    - [ ] If not exists, attempt creation (FR5).
    - [ ] Log success/failure/skip status for each object (FR10).
  - [ ] After loop, if objects were added (or attempted) and commit is enabled:
    - [ ] Trigger commit (FR7).
    - [ ] Log commit initiation and result (success/failure) (FR10).
- [ ] Implement clear exit codes for success (0) and different failure modes (non-zero) (Ref: PRD NFR2).

## Phase 5: Configuration Enhancements

- [ ] _Optional/Alternative:_ Implement logic to read configuration from a file (e.g., `config.yaml`) (Ref: PRD FR9).
- [ ] _Optional:_ Define clear precedence for configuration sources (e.g., Environment Variables > Config File) and document it.

## Phase 6: Logging & Quality Assurance

- [ ] Implement logging using Python's `logging` module (Ref: PRD FR10, NFR6).
  - [ ] Configure basic console logging (INFO level by default).
  - [ ] Add DEBUG level logging for detailed steps and API interactions.
  - [ ] Ensure sensitive data (API key) is masked or omitted from logs (NFR1).
- [ ] Apply code formatting using `ruff format` across the codebase (NFR4).
- [ ] Run linters (`ruff check`, `flake8` if used) and fix reported issues (NFR4).
- [ ] Run static type checking (`mypy`) and fix reported errors/add annotations (NFR4).
- [ ] Write unit tests (e.g., using `unittest` or `pytest`):
  - [ ] Test Pydantic model validation (valid/invalid data).
  - [ ] Test input file reading/parsing logic.
  - [ ] Test configuration loading logic.
  - [ ] Test CLI argument parsing.
- [ ] _Optional but Recommended:_ Write integration tests (may require mocking `pan-os-python` or a test Panorama instance):
  - [ ] Test Panorama connection logic.
  - [ ] Test object existence check logic.
  - [ ] Test object creation logic.
  - [ ] Test commit logic (if feasible).

## Phase 7: Documentation

- [ ] Create `README.md` file.
- [ ] Add project description and goals to `README.md`.
- [ ] Document prerequisites (Python version, Panorama access) in `README.md`.
- [ ] Document installation steps (`git clone`, `venv`, `pip install`) in `README.md`.
- [ ] Document configuration (Environment variables, config file format) in `README.md`.
- [ ] Document usage instructions (command-line examples) in `README.md`.
- [ ] Provide an example input file (JSON/YAML) in `README.md` or as a separate file.
- [ ] Explain logging output and levels in `README.md`.
- [ ] Document how to run linters and tests in `README.md`.
- [ ] Add docstrings to key functions, classes, and modules (Ref: PRD NFR4).
- [ ] Add inline comments for complex or non-obvious code sections.

---

_Note: This list represents a logical flow. Tasks within phases might be done in parallel or iteratively._
