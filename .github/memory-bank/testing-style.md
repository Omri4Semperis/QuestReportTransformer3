## Testing style
- Testing framework is pytest.
- Every test file is named test_<module>.py.
- Each test function docstring starts with the 🦄 emoji.
- Follow Arrange-Act-Assert order.
- Use fixtures; no duplicated setup.
- Bare assert statements only.
- Common mocks live in conftest.py.