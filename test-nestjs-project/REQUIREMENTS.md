# Requirements Document

**Project:** Test NestJS Authentication API  
**Cycle:** C1  
**Approved:** 2026-05-22  
**Human Gate 1:** APPROVED

---

## REQ-0001: User Authentication via JWT

**Priority:** CRITICAL  
**Risk Level:** R2 (Production)  
**Status:** approved

### Objective
Implement JWT-based authentication for the NestJS backend API.

### Acceptance Criteria

**AC1:** POST /auth/login endpoint accepts email and password, returns JWT access token on valid credentials  
**AC2:** Invalid credentials return 401 Unauthorized with error message  
**AC3:** POST /auth/register endpoint creates new user account with email, password, and name  
**AC4:** JWT tokens expire after 1 hour  
**AC5:** Protected routes require valid JWT in Authorization header

### Constraints

- Use bcrypt for password hashing
- Use @nestjs/jwt and @nestjs/passport
- Passwords must be validated (min 8 characters)
- Email must be validated (valid email format)
- No duplicate email addresses allowed

### Affected Architecture

- **Modules:** AuthModule, UsersModule
- **Controllers:** AuthController
- **Services:** AuthService, UsersService
- **DTOs:** LoginDto, RegisterDto, UserResponseDto
- **Guards:** JwtAuthGuard
- **Strategies:** JwtStrategy
- **Entities:** User entity (if using database)

### Required Evidence (R2)

- Build Manifest with traceability
- Unit tests for AuthService
- E2E tests for auth endpoints
- TypeScript compilation passes
- npm audit shows no high/critical vulnerabilities

---

## REQ-0002: User Entity and Database Schema

**Priority:** HIGH  
**Risk Level:** R2 (Production)  
**Status:** approved

### Objective
Create User entity with database schema for storing user credentials.

### Acceptance Criteria

**AC1:** User entity has id, email, password, name, createdAt fields  
**AC2:** Email field has unique constraint  
**AC3:** Password field is hashed before storage  
**AC4:** Migration file creates users table

### Constraints

- Use TypeORM or Prisma (project's choice)
- Migration must have rollback capability
- Passwords never stored in plain text

### Required Evidence (R2)

- Migration file with rollback notes
- Entity definition
- Unit tests for User entity operations
