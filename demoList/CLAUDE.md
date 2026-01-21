# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a push notification system with two sub-projects:
- **push-frontend**: Vue 3 + Element UI Plus frontend
- **push-backend**: Spring Boot 3.4.4 + JPA backend

### Core Functionality

1. **Multi-platform Push**: Abstract push capability supporting different platforms (W3 Todo, WeLink App)
2. **Configuration Management**: Business types can configure which push platforms to use with static parameters
3. **Push Preview**: Preview complete push parameters before execution
4. **History Tracking**: All push operations are recorded
5. **Group Management**: Manage push recipient groups with member CRUD operations

## Architecture

### Backend Architecture (Spring Boot)

```
push-backend/src/main/java/com/push/
├── controller/           # REST API endpoints
│   ├── PushController          # Push preview & execute
│   ├── PushConfigController     # Push configuration CRUD
│   ├── PushHistoryController    # History query
│   └── PushGroupController      # Group & member management
├── service/
│   └── impl/                  # Business logic
├── strategy/                   # Push platform adapters (Strategy Pattern)
│   ├── PushPlatformStrategy      # Interface
│   ├── W3TodoPushStrategy       # W3 implementation (mocked)
│   └── WeLinkAppPushStrategy   # WeLink implementation (mocked)
├── entity/                     # JPA entities
├── dto/                       # Data transfer objects
├── mapper/                    # JPA repositories
└── PushApplication.java          # Main application class
```

### Frontend Architecture (Vue 3)

```
push-frontend/src/
├── api/                    # API clients
│   ├── request.js           # Axios instance with interceptors
│   ├── push.js
│   ├── config.js
│   ├── history.js
│   └── group.js
├── components/
│   ├── PushDialog.vue          # Push preview & execute dialog
│   ├── PushHistoryDialog.vue   # History query & details
│   └── GroupConfigDialog.vue   # Group & member management
├── App.vue                 # Demo page with push buttons
└── main.js                 # Application entry
```

## Common Development Commands

### Backend (push-backend)

```bash
# Navigate to backend
cd push-backend

# Build and run
mvn clean spring-boot:run

# Package without tests
mvn clean package -DskipTests

# Run packaged JAR
java -jar target/push-backend-1.0.0.jar

# Run specific test
mvn test -Dtest=ClassName

# Skip compilation warnings (if needed)
mvn clean spring-boot:run -Dmaven.compiler.failOnError=false
```

### Frontend (push-frontend)

```bash
# Navigate to frontend
cd push-frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Check dependencies
npm audit
```

### Database Setup

```bash
# Initialize database with schema and sample data
mysql -u root -p < push-backend/src/main/resources/schema.sql

# Or let Spring Boot auto-create (with createDatabaseIfNotExist=true in URL)
```

## Key Technical Details

### Backend

- **Framework**: Spring Boot 3.4.4 with Java 21
- **ORM**: Spring Data JPA (Hibernate)
- **Database**: MySQL 8.0+ with utf8mb4 charset
- **Pattern**: Strategy Pattern for push platform abstraction
- **API Base URL**: `http://localhost:8080/api/push`

### Frontend

- **Framework**: Vue 3 (Composition API with `<script setup>`)
- **UI Library**: Element UI Plus
- **HTTP Client**: Axios with interceptors
- **Dev Server**: Vite on `http://localhost:5173`

### Push Platform Implementation

Current implementation uses **mocked** push (simulated). To integrate with real APIs:

1. Add OpenFeign dependency in `pom.xml`
2. Create Feign Client interfaces for W3 Todo and WeLink App
3. Inject Feign clients in strategy implementations
4. Replace mock `execute()` method with actual Feign calls

Code locations for integration:
- `W3TodoPushStrategy.java:46-62` - Contains commented Feign call example
- `WeLinkAppPushStrategy.java:46-62` - Contains commented Feign call example

## Important Implementation Notes

### Strategy Pattern Usage

Push platforms are discovered automatically via Spring's `@Component` scanning. To add a new platform:

1. Create a class implementing `PushPlatformStrategy`
2. Annotate with `@Component`
3. Implement `buildPushRequest()` and `execute()` methods
4. Return unique platform code from `getPlatformCode()`

### Configuration Management

- **Static parameters**: Stored in `push_config.config_json` (e.g., type, source)
- **Dynamic parameters**: Passed from frontend at push time (e.g., title, content, jumpUrl)
- **Group members**: Automatically populated from `group_member` table

### API Response Format

All endpoints return unified `ApiResponse<T>`:
```java
{
  "code": 200,        // 200 = success, others = error
  "message": "...",
  "data": { ... }
}
```

Frontend axios interceptor checks `res.code === 200` before returning data.

### Data Flow

1. **Push Flow**:
   - User selects group and views preview
   - Frontend calls `/api/push/preview`
   - Backend merges config + dynamic params
   - User confirms → calls `/api/push/execute`
   - Each platform strategy executes independently
   - All attempts recorded to `push_history`

2. **History Query**:
   - User opens history dialog
   - Frontend calls `/api/push/history/page?page=0&size=10`
   - Backend returns paged results from `push_history`

3. **Group Management**:
   - User opens group config dialog
   - Can create/edit/delete groups
   - Manage group members (add/remove employee numbers)

## Known Issues & TODOs

### Current Limitations

1. **Mock Implementation**: Push strategies are mocked for demonstration
2. **No Authentication**: No user/login system implemented
3. **No Validation Layer**: Missing `@Valid` on DTOs
4. **Basic Error Handling**: No global exception handler
5. **Hard-coded Ports**: API response code `200` is magic number

### Potential Improvements

1. Add `@Valid` annotations to DTOs for request validation
2. Implement global `@RestControllerAdvice` for unified error handling
3. Add SLF4J logging framework (currently uses System.out.println)
4. Consider adding retry logic for push failures
5. Add frontend environment variables for API base URL

## File Structure Reference

### Critical Files for Business Logic

| File | Purpose |
|-------|----------|
| `PushServiceImpl.java` | Core push orchestration |
| `W3TodoPushStrategy.java` | W3 platform push implementation |
| `WeLinkAppPushStrategy.java` | WeLink platform push implementation |
| `PushDialog.vue` | Main push UI component |
| `GroupConfigDialog.vue` | Group management UI |

### Configuration Files

| File | Purpose |
|-------|----------|
| `application.yml` | Spring Boot configuration |
| `schema.sql` | Database initialization with sample data |
| `pom.xml` | Maven dependencies |
| `package.json` | NPM dependencies and scripts |

## Testing Notes

- **Backend Tests**: Located in `src/test/java/com/push/`
- **Frontend Tests**: Not currently implemented
- To run all tests: `mvn test`

## Design Documentation

Refer to `推送模块设计文档.md` for:
- Complete database schema with 6 tables
- API endpoint specifications
- Frontend component designs
- Sample SQL initialization data
