# Contributing to AutoQ

Thank you for your interest in contributing to AutoQ! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/AutoQ.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

Follow the instructions in [SETUP.md](SETUP.md) to set up your development environment.

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Use meaningful variable and function names
- Keep functions small and focused

### TypeScript/React (Frontend)
- Follow React best practices
- Use functional components with hooks
- Use TypeScript for type safety
- Follow the existing component structure
- Use TailwindCSS for styling

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Guidelines

1. **Description**: Provide a clear description of what your PR does
2. **Issue Reference**: Reference any related issues
3. **Testing**: Describe how you tested your changes
4. **Screenshots**: Include screenshots for UI changes
5. **Documentation**: Update documentation if needed

## Code Review Process

1. All PRs require at least one review
2. Address review comments promptly
3. Keep PRs focused and reasonably sized
4. Ensure CI/CD checks pass

## Reporting Bugs

When reporting bugs, please include:
- AutoQ version
- Operating system
- Python/Node.js version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Error messages/logs

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Provide a clear use case
- Explain why it would be valuable
- Consider implementation complexity

## Areas for Contribution

### High Priority
- Improve question generation quality
- Add more question types
- Enhance PDF parsing for complex layouts
- Add unit tests
- Improve documentation

### Medium Priority
- Add support for more document formats
- Implement practice mode for students
- Add analytics dashboard
- Improve UI/UX
- Add internationalization

### Low Priority
- Add dark mode
- Add keyboard shortcuts
- Add export to more formats
- Add question templates

## Community

- Be respectful and inclusive
- Help others in discussions
- Share your use cases and feedback
- Report security issues privately

## License

By contributing to AutoQ, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions about contributing!
