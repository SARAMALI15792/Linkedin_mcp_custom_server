# Publishing LinkedIn MCP Server to PyPI

This guide explains how to publish your LinkedIn MCP Server package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. **API Token**: Generate an API token at [https://pypi.org/manage/account/#api-tokens](https://pypi.org/manage/account/#api-tokens)
3. **Build Tools**: Already installed (`build` and `twine`)

## Step 1: Verify Package Structure

Your package should have this structure:

```
linkedin_custom_mcp/
├── linkedin_mcp_server/        # Package directory
│   ├── __init__.py            # With __version__ = "1.0.0"
│   ├── __main__.py            # CLI entry point
│   ├── server.py              # Main server code
│   ├── config.py              # Configuration
│   ├── utils.py               # Utilities
│   └── tools/                 # Tool implementations
├── pyproject.toml             # Package metadata
├── README.md                  # Documentation
├── LICENSE                    # MIT License
└── MANIFEST.in                # Package data
```

## Step 2: Clean Previous Builds

```bash
cd "C:\Users\saram\OneDrive\Desktop\mcp-servers\linkedin_custom_mcp"
rm -rf dist/ build/ *.egg-info
```

## Step 3: Build the Package

```bash
python -m build
```

This creates two files in `dist/`:
- `linkedin_mcp_server-1.0.0.tar.gz` (source distribution)
- `linkedin_mcp_server-1.0.0-py3-none-any.whl` (wheel distribution)

## Step 4: Test on TestPyPI (Optional but Recommended)

### Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted:
- **Username**: `__token__`
- **Password**: Your TestPyPI API token (starts with `pypi-`)

### Test Installation from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ linkedin-mcp-server
```

### Test the Command

```bash
linkedin-mcp-server
```

## Step 5: Publish to PyPI

Once you've verified everything works on TestPyPI:

```bash
python -m twine upload dist/*
```

When prompted:
- **Username**: `__token__`
- **Password**: Your PyPI API token (starts with `pypi-`)

## Step 6: Verify Publication

1. Visit your package page: [https://pypi.org/project/linkedin-mcp-server/](https://pypi.org/project/linkedin-mcp-server/)
2. Check that README renders correctly
3. Verify badges display properly
4. Test installation:

```bash
pip install linkedin-mcp-server
```

## Configuration for Claude Desktop

After publishing, users can configure Claude Desktop like this:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["linkedin-mcp-server"]
    }
  }
}
```

Or with pip:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "linkedin-mcp-server"
    }
  }
}
```

## Updating the Package

### 1. Update Version

Edit `linkedin_mcp_server/__init__.py`:

```python
__version__ = "1.0.1"  # Increment version
```

Update `pyproject.toml`:

```toml
version = "1.0.1"
```

### 2. Update Changelog

Document changes in README.md

### 3. Rebuild and Upload

```bash
rm -rf dist/
python -m build
python -m twine upload dist/*
```

## Troubleshooting

### Error: "File already exists"

You cannot upload the same version twice to PyPI. Increment the version number in:
- `linkedin_mcp_server/__init__.py`
- `pyproject.toml`

### Error: "Invalid package name"

- Package names must use hyphens, not underscores (✓ `linkedin-mcp-server`, ✗ `linkedin_mcp_server`)
- This is already correctly configured

### Error: "README rendering issues"

- Ensure README.md uses standard Markdown
- Check that all image URLs are absolute, not relative
- Validate with: `python -m readme_renderer README.md`

### Error: "Missing dependencies"

Ensure all dependencies are listed in `pyproject.toml` under `[project.dependencies]`

## Best Practices

1. **Semantic Versioning**: Follow [SemVer](https://semver.org/)
   - MAJOR.MINOR.PATCH (e.g., 1.0.0)
   - Increment MAJOR for breaking changes
   - Increment MINOR for new features
   - Increment PATCH for bug fixes

2. **Test Before Publishing**:
   - Always test on TestPyPI first
   - Install in a fresh virtual environment
   - Verify CLI commands work

3. **Documentation**:
   - Keep README.md up-to-date
   - Include usage examples
   - Document breaking changes

4. **Git Tags**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

5. **GitHub Release**:
   - Create a GitHub release matching the PyPI version
   - Include changelog
   - Attach wheel and source distributions

## Security

- **Never commit API tokens** to git
- Store tokens securely (password manager or keyring)
- Use scoped tokens (limited to this package)
- Regularly rotate tokens

## Resources

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)

## Support

If you encounter issues:
1. Check the [PyPI Help](https://pypi.org/help/)
2. Review [Python Packaging tutorials](https://packaging.python.org/tutorials/)
3. Ask in [Python Packaging Discussions](https://discuss.python.org/c/packaging/)
