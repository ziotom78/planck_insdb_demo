# How to prepare a new release

-   Update the version number in the following files:

    -   `pyproject.toml`

    -   `instrumentdb/__init__.py`

    -   `CHANGELOG.md` (be sure to leave an empty `HEAD` title at the
        top);
    
-   Build the release:

    ```
    poetry build
    ```

-   Upload the `.tar.gz` file (saved in `./dist`) to the GitHub release page.
