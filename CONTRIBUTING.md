# Contributing to Luminara

Thank you for your interest in contributing to Lumi! We welcome contributions from the community to help improve and
expand the bot's functionality. Please follow these guidelines when contributing:

## Getting Started

1. **Fork the Repository:** Fork the Luminara repository to your own GitHub account.

2. **Clone Your Fork:** Clone your forked repository to your local machine.

3. **Set Up Development Environment:**
4. 
    * **Docker:** To run the bot, use this command to run your newly edited code:

      ```bash
      docker compose -f docker-compose.dev.yml up --build --watch
      ```

      *Note: Adding `--watch` is recommended as it supports hot reloading. You can use the `.dev stop` command to trigger a rebuild with your latest changes.*

    * **Poetry:** While developing, it is recommended to install & configure poetry locally:

      ```bash
      poetry install
      poetry shell
      poetry pre-commit install
      poetry run pre-commit run --all-files
      ```

## Making Changes

1. **Create a Branch:** Create a new branch for your changes.
2. **Code Style:** Adhere to the existing code style and formatting conventions.
3. **Strict Typing:** Always use strict typing (e.g., `str`, `int`, `List[str]`) for better code quality and
   maintainability.
4. **Pre-Commit Checks:** Before committing, run pre-commit checks to ensure your code passes linting and formatting
   standards.
5. **Clear Commit Messages:** Write clear and concise commit messages that describe the changes you made.

## Submitting Changes

1. **Create a Pull Request:** Create a pull request (PR) from your branch to the `main` branch of the original
   repository.
2. **Review:** Your PR will be reviewed by the Sourcery & Lumi maintainers. Address any feedback or requested changes.
3. **Merge:** Once approved, your PR will be merged into the main branch.

## Additional Notes

* **Documentation:** If you add new functionality or change existing behavior, update or add the docstrings accordingly.

Thank you for your contributions!
