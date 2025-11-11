## Version File
The project version is different depending on project language:
- Python - pyproject.toml
- Go - VERSION
- Java gradle.properties

## Version Format
Other than `master` branch all branches should have project version with suffix.
Suffix depends on the language: java should use `-SNAPSHOT` python `.dev0`
- Development/feature/fix versions use suffix (e.g., `0.2.7-SNAPSHOT` or `1.1.1.dev0`)
- Release versions remove suffix (e.g., `0.3.0`)