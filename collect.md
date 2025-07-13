# AI Repository Analysis Prompt

Please perform a comprehensive analysis of this Git repository to establish context for future AI-assisted development. Create a detailed report that will serve as a reference for all future AI interactions with this codebase.

## Analysis Framework

### 1. Repository Overview
- **Project Name & Description**: What does this project do?
- **Primary Language(s)**: Main programming languages used
- **Project Type**: (web app, library, CLI tool, mobile app, etc.)
- **Maturity Level**: (prototype, MVP, production-ready, mature)
- **Last Activity**: Recent commit patterns and development velocity

### 2. Architecture & Structure
- **Project Structure**: Map out the directory structure and explain the purpose of each major directory
- **Architectural Pattern**: (MVC, microservices, monolith, layered, hexagonal, etc.)
- **Data Flow**: How data moves through the system
- **Key Components**: Identify and explain core modules/components
- **Entry Points**: Main application entry points and how they're structured
- **Build System**: How the project is built and deployed

### 3. Technology Stack Analysis
- **Runtime/Platform**: (Node.js, Python, Java, .NET, etc.)
- **Frameworks**: Primary frameworks and their versions
- **Libraries**: Key dependencies and their purposes
- **Database**: Database technology and ORM/query tools
- **Frontend Stack**: (if applicable) UI frameworks, build tools, styling
- **Testing Framework**: Testing libraries and testing strategy
- **Development Tools**: Linters, formatters, pre-commit hooks

### 4. Configuration & Environment
- **Environment Variables**: Document expected env vars and their purposes
- **Configuration Files**: Explain key config files and their structure
- **Deployment Configuration**: Docker, CI/CD, deployment scripts
- **Development Setup**: How to get the project running locally
- **Required Services**: External services, databases, APIs needed

### 5. Code Patterns & Conventions
- **Coding Standards**: Formatting, naming conventions, style guides
- **Common Patterns**: Recurring code patterns and architectural decisions
- **Error Handling**: How errors are handled throughout the system
- **Logging**: Logging strategy and implementation
- **State Management**: (if applicable) How application state is managed
- **API Design**: REST/GraphQL conventions, request/response patterns

### 6. Security Implementation
- **Authentication**: How users are authenticated
- **Authorization**: Permission/role systems
- **Input Validation**: Validation strategies and implementation
- **Security Headers**: HTTP security headers and middleware
- **Secrets Management**: How sensitive data is handled
- **Known Security Considerations**: Any security-related code patterns

### 7. Data Layer
- **Database Schema**: Tables, relationships, indexes
- **Migration Strategy**: How database changes are managed
- **Query Patterns**: Common database interaction patterns
- **Caching**: Caching strategies and implementation
- **Data Validation**: Schema validation and constraints

### 8. Testing Strategy
- **Test Types**: Unit, integration, e2e tests and their coverage
- **Test Structure**: How tests are organized and named
- **Mocking Strategy**: How external dependencies are mocked
- **Test Data**: How test data is managed and created
- **Testing Utilities**: Common test helpers and utilities

### 9. Development Workflow
- **Branch Strategy**: Git workflow and branching conventions
- **Code Review Process**: PR/MR templates and review requirements
- **CI/CD Pipeline**: Automated testing and deployment
- **Release Process**: How releases are cut and deployed
- **Development Scripts**: Available npm/make/bash scripts

### 10. External Integrations
- **APIs**: External APIs consumed and their purposes
- **Services**: Third-party services integrated
- **Webhooks**: Incoming/outgoing webhook handling
- **Message Queues**: Async processing and queuing systems
- **Monitoring**: APM, logging, alerting systems

### 11. Performance Considerations
- **Performance Patterns**: Optimization strategies in use
- **Bottlenecks**: Known or potential performance issues
- **Caching Strategy**: Performance-related caching
- **Resource Usage**: Memory, CPU, I/O considerations
- **Scalability**: How the system scales

### 12. Documentation & Knowledge
- **Existing Documentation**: README, wikis, inline comments
- **Code Comments**: Quality and patterns of code documentation
- **API Documentation**: OpenAPI/Swagger specs, API docs
- **Architecture Decisions**: ADRs or documented decisions
- **Known Issues**: TODOs, FIXMEs, known bugs

### 13. Development Context
- **Team Size**: Estimated team size based on commit patterns
- **Development Velocity**: Commit frequency and patterns
- **Code Quality**: General code quality observations
- **Technical Debt**: Areas needing refactoring or improvement
- **Recent Changes**: Notable recent developments

### 14. AI-Specific Insights
- **Complex Areas**: Parts of codebase that need extra context
- **Common Tasks**: Frequent development tasks for this project
- **Gotchas**: Non-obvious behaviors or requirements
- **Best Practices**: Project-specific best practices to follow
- **Pitfalls**: Common mistakes to avoid

## Output Format

Structure your analysis as a comprehensive markdown document with:
- Clear headings and subheadings
- Code examples where relevant
- File paths and line numbers for references
- Links to relevant files or documentation
- Bullet points for lists and key information
- Tables for structured data where appropriate

## Instructions for Analysis

1. **Start with the README** and any documentation files
2. **Examine package.json/requirements.txt** and similar dependency files
3. **Analyze the directory structure** systematically
4. **Look for configuration files** (.env examples, config directories)
5. **Examine entry points** (main.js, app.py, etc.)
6. **Study the database layer** (models, migrations, schemas)
7. **Review test files** to understand testing patterns
8. **Check CI/CD configuration** (.github/workflows, .gitlab-ci.yml)
9. **Analyze key business logic** files
10. **Look for security-related code** (auth, validation, middleware)

Save this analysis as `doc/CONTEXT.md` in the repository root for future reference by AI tools.

---

*This analysis should be updated whenever significant architectural changes are made to the project.*
