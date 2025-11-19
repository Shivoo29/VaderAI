# Contributing to Vader AI

Thank you for your interest in contributing to Vader AI! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a positive community
- Remember: we're all here to build something cool together

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

1. Check if the feature has been suggested already
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach
   - Any related examples

### Pull Requests

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the coding style
   - Add tests for new features
   - Update documentation
4. **Test your changes**: Run tests and ensure everything works
5. **Commit**: Use clear commit messages
6. **Push**: Push to your fork
7. **Submit PR**: Create a pull request to main repository

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/VaderAI.git
cd VaderAI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black backend/
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions small and focused
- Add unit tests for new features

```python
def process_audio(audio_data: np.ndarray, sample_rate: int) -> str:
    """
    Process audio data and return transcription

    Args:
        audio_data: Audio samples as numpy array
        sample_rate: Sample rate in Hz

    Returns:
        Transcribed text
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)

- Use functional components with hooks
- Follow ESLint configuration
- Use meaningful variable names
- Keep components small and reusable
- Add prop types or TypeScript types

```jsx
export default function VoiceButton({ isRecording, onClick }) {
  return (
    <button
      onClick={onClick}
      className={isRecording ? 'recording' : 'idle'}
    >
      {isRecording ? 'Stop' : 'Record'}
    </button>
  )
}
```

### Arduino/C++ (ESP32)

- Follow Arduino style guide
- Comment hardware connections
- Use descriptive variable names
- Include error handling

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_auth.py
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment-related changes
- Add JSDoc/docstrings for new functions
- Include examples in documentation

## Areas We Need Help

- [ ] Multi-language support
- [ ] Mobile app development
- [ ] Voice quality improvements
- [ ] Smart home integrations
- [ ] Performance optimizations
- [ ] Additional voice personalities
- [ ] Better error handling
- [ ] Accessibility improvements
- [ ] Documentation improvements
- [ ] Test coverage

## Questions?

- Open an issue for questions
- Tag maintainers if needed
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**May the Force be with you!**
