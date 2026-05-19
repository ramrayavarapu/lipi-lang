# Circuit Breaker Implementation Guide

This document provides the complete implementation guide for the circuit breaker mechanism in the claude-autofix workflow to prevent infinite fix loops.

## Overview

The circuit breaker prevents infinite loops in the claude-autofix workflow by detecting when the most recent commit already has an "Auto-fix:" prefix and halting the process when that is the case.

## Implementation Details

### Circuit Breaker Logic

The circuit breaker activates when:
1. A pull request review triggers the claude-autofix workflow
2. The most recent commit message starts with "Auto-fix:"
3. This means an autofix has already run most recently, so running again could create an infinite loop

### Required Changes to `.github/workflows/claude-autofix.yml`

**IMPORTANT**: Due to GitHub App security restrictions, these changes must be applied manually by a repository administrator with workflow write permissions.

Add the following steps after the existing "Checkout PR branch" step (around line 32):

```yaml
      - name: Check for circuit breaker condition
        id: circuit_breaker
        run: |
          LAST_COMMIT_MSG=$(git log -1 --pretty=format:'%s')
          echo "Last commit message: $LAST_COMMIT_MSG"
          
          if [[ "$LAST_COMMIT_MSG" == Auto-fix:* ]]; then
            echo "Circuit breaker triggered: consecutive autofix detected"
            echo "CIRCUIT_BREAKER_TRIGGERED=true" >> "$GITHUB_ENV"
            exit 0
          fi
          echo "CIRCUIT_BREAKER_TRIGGERED=false" >> "$GITHUB_ENV"

      - name: Post circuit breaker comment and exit
        if: env.CIRCUIT_BREAKER_TRIGGERED == 'true'
        uses: actions/github-script@f28e40c7f34bde8b3046d885e986cb6290c5673b
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body: [
                '🛑 **Circuit Breaker Activated**',
                '',
                'The claude-autofix workflow has detected that the most recent commit is an autofix commit.',
                'To prevent infinite loops, the autofix process has been halted.',
                '',
                '**Manual intervention is required:**',
                '1. Review the recent autofix commits and Copilot feedback',
                '2. Make manual corrections as needed',
                '3. Commit your changes to continue the review process',
                '',
                'The autofix workflow will resume on your next commit.'
              ].join('\n')
            });

      - name: Exit early if circuit breaker triggered
        if: env.CIRCUIT_BREAKER_TRIGGERED == 'true'
        run: |
          echo "Exiting due to circuit breaker activation"
          exit 0
```

### Update Existing Steps

Modify all remaining steps after the circuit breaker steps to include the condition:
```yaml
        if: env.CIRCUIT_BREAKER_TRIGGERED != 'true'
```

This ensures that autofix logic only runs when the circuit breaker hasn't been triggered.

## Data Flow

```
[GitHub Event: changes_requested] 
→ [Checkout PR branch] 
→ [Check last commit message] 
→ [If autofix commit: Post comment & exit] 
→ [Else: Proceed with normal autofix]
```

## Test Coverage

The implementation includes comprehensive test coverage:

### Unit Tests (`tests/test_circuit_breaker_unit.py`)
- Circuit breaker detection logic
- Commit message parsing
- Edge case handling (whitespace, case sensitivity)
- Git integration testing

### API Tests (`tests/test_circuit_breaker_api.py`)
- GitHub API interactions
- Comment posting functionality
- Environment variable validation
- Workflow exit behavior

### UX Tests (`tests/test_circuit_breaker_ux.py`)
- End-to-end user flows
- Circuit breaker activation scenarios
- Manual intervention recovery
- User feedback clarity

## Security Considerations

1. **No security vulnerabilities introduced**: The circuit breaker only reads commit messages
2. **No regression in existing functionality**: Conditional execution preserves existing behavior
3. **Input validation**: Commit message parsing is safe (read-only Git operations)
4. **No secrets exposed**: Implementation doesn't handle or expose sensitive data

## Performance Impact

- **Minimal overhead**: Simple Git command execution (`git log -1`)
- **Early exit**: When triggered, prevents unnecessary API calls to Claude
- **Cost savings**: Reduces API quota consumption by preventing infinite loops

## User Experience

### Circuit Breaker Activation
When the circuit breaker activates, users see:
1. Clear visual indicator (🛑 emoji)
2. Explanation of what happened and why
3. Step-by-step recovery instructions
4. Assurance that workflow will resume after manual intervention

### Recovery Process
1. User reviews autofix commits and Copilot feedback
2. User makes manual corrections
3. User commits changes with regular commit message
4. Workflow resumes normal operation on next Copilot review

## Validation Steps

After implementation, validate with these scenarios:

1. **Normal flow**: Regular commit → Copilot review → Autofix → Success
2. **Circuit breaker activation**: Autofix commit → Copilot review → Circuit breaker triggers
3. **Recovery**: Circuit breaker triggered → Manual fix → Workflow resumes
4. **Edge cases**: Long commit messages, empty commits, multiple consecutive autofixes

## Monitoring

Monitor the following metrics:
- Frequency of circuit breaker activations
- Average time to manual intervention after activation
- Reduction in infinite loop incidents
- API quota usage patterns

## Troubleshooting

### Circuit Breaker Not Triggering
- Verify commit message format exactly matches "Auto-fix:" prefix
- Check environment variable propagation
- Validate Git log command execution

### Circuit Breaker Triggering Incorrectly
- Review commit message parsing logic
- Check for whitespace or encoding issues
- Validate case sensitivity requirements

### Recovery Issues
- Ensure users understand manual intervention steps
- Provide clear guidance on commit message formatting
- Monitor user feedback and adjust documentation

## Implementation Checklist

- [ ] Add circuit breaker steps to workflow file (requires admin)
- [ ] Update existing steps with conditional execution
- [ ] Test in development environment
- [ ] Validate with multiple scenarios
- [ ] Monitor initial deployment
- [ ] Update documentation based on user feedback

## Related Files

- `.github/workflows/claude-autofix.yml` - Main workflow file (requires manual update)
- `tests/test_circuit_breaker_*.py` - Comprehensive test suite
- `STANDARDS.md` - Engineering standards reference
- `docs/architecture/system.yaml` - Architecture documentation

---

**Note**: This implementation follows Rule 2 standards for safety, testing, and infrastructure as code principles. All changes are designed to be minimal, secure, and maintainable.