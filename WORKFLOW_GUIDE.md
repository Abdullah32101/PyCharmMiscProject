# 🚀 GitHub Actions Workflow Guide

This document explains the automated workflows set up for your test framework.

## 📋 Available Workflows

### 1. **Test Framework Automation** (`.github/workflows/test-automation.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main` or `master`
- Daily at 2 AM UTC (scheduled)
- Manual trigger

**Features:**
- ✅ **Multi-device testing** (Desktop, iPhone X, iPad Pro)
- ✅ **Database integration** with MySQL
- ✅ **Code coverage** reporting
- ✅ **HTML test reports** generation
- ✅ **Screenshot capture** on failures
- ✅ **PR comments** with test results
- ✅ **Artifact upload** for test results

**Jobs:**
1. **test-automation**: Runs comprehensive tests
2. **code-quality**: Code formatting, linting, type checking
3. **notify-results**: Success/failure notifications

### 2. **Deploy to Staging** (`.github/workflows/deploy-staging.yml`)

**Triggers:**
- Push to `develop` or `staging` branches
- Manual trigger with environment selection

**Features:**
- ✅ **Pre-deployment testing** (smoke tests)
- ✅ **Environment-specific deployment**
- ✅ **Deployment package creation**
- ✅ **Deployment notifications**

### 3. **Scheduled Test Runner** (`.github/workflows/scheduled-tests.yml`)

**Triggers:**
- Daily at 6 AM UTC
- Every Monday at 9 AM UTC
- Manual trigger with test suite selection

**Features:**
- ✅ **Comprehensive test suites**
- ✅ **Mobile-specific testing**
- ✅ **Desktop-specific testing**
- ✅ **Database integration testing**
- ✅ **Automated issue creation** with results
- ✅ **Long-term artifact storage** (90 days)

## 🛠️ Workflow Configuration

### Environment Variables

```yaml
PYTHON_VERSION: '3.9'
HEADLESS: 'true'
MOBILE_TEST: 'true'
TEST_DEVICES: 'desktop,iPhone X,iPad Pro'
```

### Database Configuration

The workflows automatically set up MySQL with:
- **Host**: 127.0.0.1
- **Database**: test_framework
- **User**: test_user
- **Password**: test_password
- **Port**: 3306

## 📊 Test Reporting

### Generated Reports

1. **HTML Reports**: Self-contained test reports
2. **JUnit XML**: For CI/CD integration
3. **Coverage Reports**: Code coverage analysis
4. **Screenshots**: Failed test captures
5. **Error Links**: Debug information

### Artifact Storage

- **Test Results**: 30 days retention
- **Coverage Reports**: 30 days retention
- **Scheduled Results**: 90 days retention
- **Deployment Packages**: 7 days retention

## 🔧 Manual Workflow Triggers

### Test Automation
```bash
# Trigger via GitHub UI or API
# Navigate to Actions > Test Framework Automation > Run workflow
```

### Deploy to Staging
```bash
# Manual deployment with environment selection
# Options: staging, testing
```

### Scheduled Tests
```bash
# Manual test suite execution
# Options: all, mobile, desktop, database
```

## 📈 Workflow Metrics

### Performance Indicators

- **Test Execution Time**: Monitored for optimization
- **Success Rate**: Tracked over time
- **Coverage Trends**: Code coverage monitoring
- **Failure Analysis**: Automated issue creation

### Quality Gates

- **Code Formatting**: Black and isort compliance
- **Linting**: Flake8 standards
- **Type Checking**: MyPy validation
- **Security Scanning**: Bandit analysis

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failures**
   - Check MySQL service health
   - Verify database credentials
   - Ensure port availability

2. **Chrome Installation Issues**
   - Verify Ubuntu package sources
   - Check system dependencies
   - Validate Chrome binary

3. **Test Failures**
   - Review screenshot artifacts
   - Check error links
   - Analyze test logs

### Debug Commands

```bash
# Check workflow status
gh run list

# View workflow logs
gh run view <run-id>

# Download artifacts
gh run download <run-id>

# Rerun failed workflow
gh run rerun <run-id>
```

## 🔄 Workflow Lifecycle

### Development Flow

1. **Code Push** → Triggers test automation
2. **Test Execution** → Multi-device testing
3. **Quality Checks** → Code formatting and linting
4. **Results Upload** → Artifacts and reports
5. **Notifications** → PR comments and summaries

### Deployment Flow

1. **Branch Push** → Triggers deployment
2. **Pre-deployment Tests** → Smoke test execution
3. **Package Creation** → Deployment artifacts
4. **Environment Deployment** → Staging/testing
5. **Status Notification** → Deployment summary

### Scheduled Flow

1. **Time Trigger** → Automated execution
2. **Test Suite Selection** → Based on schedule
3. **Comprehensive Testing** → Full framework validation
4. **Issue Creation** → Results documentation
5. **Artifact Storage** → Long-term retention

## 📞 Support

### Workflow Issues

- Check GitHub Actions logs
- Review workflow configuration
- Verify environment setup
- Contact development team

### Customization

- Modify trigger conditions
- Add new test suites
- Configure notification channels
- Adjust retention policies

## 🎯 Best Practices

### Development

- ✅ Commit frequently to trigger tests
- ✅ Review PR comments for test results
- ✅ Monitor coverage trends
- ✅ Address quality gate failures

### Maintenance

- ✅ Regular workflow updates
- ✅ Dependency management
- ✅ Performance monitoring
- ✅ Security scanning

### Collaboration

- ✅ Share test results with team
- ✅ Document workflow changes
- ✅ Train team on workflow usage
- ✅ Gather feedback for improvements 