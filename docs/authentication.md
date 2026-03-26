# Believers Sword Authentication System

## Overview

The Believers Sword app uses **Laravel Sanctum** for API token-based authentication. Users can register, login, and manage their authentication state through the frontend Pinia store.

---

## Backend API Endpoints

### Public Routes

#### POST `/api/auth/register`

Register a new user account.

**Request:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirmation": "securepassword123"
}
```

**Response (201):**
```json
{
    "status": "success",
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "token": "1|abc123xyz..."
}
```

**Validation:**
- `name`: required, max 255 chars
- `email`: required, valid email, unique
- `password`: required, min 8 chars, must match confirmation

#### POST `/api/auth/login`

Authenticate user and receive access token.

**Request:**
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (200):**
```json
{
    "status": "success",
    "message": "Login successful",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "token": "1|abc123xyz..."
}
```

**Response (401):**
```json
{
    "status": "error",
    "message": "The provided credentials are incorrect."
}
```

---

### Protected Routes (Require Bearer Token)

Include token in `Authorization` header:
```
Authorization: Bearer <your-token>
```

#### POST `/api/auth/logout`

Revoke all user tokens (logout from all devices).

**Response:**
```json
{
    "status": "success",
    "message": "Successfully logged out"
}
```

#### GET `/api/auth/user`

Get authenticated user information.

**Response:**
```json
{
    "status": "success",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

#### POST `/api/sync`

Push sync data to backend (see sync_system.md for details).

#### GET `/api/sync/pull`

Pull sync data from backend.

---

## Frontend Implementation

### Auth Store (`FrontEndApp/src/store/authStore.ts`)

Pinia store for managing authentication state.

#### State

- `user: User | null` - Current authenticated user
- `token: string | null` - Bearer token
- `isAuthenticated: boolean` - Auth status
- `syncData: boolean` - Sync enabled flag

#### Actions

```typescript
// Register new user
await authStore.register(name, email, password, passwordConfirmation)

// Login
await authStore.login(email, password)

// Logout
await authStore.logout()

// Get user info
await authStore.getUser()

// Initialize from localStorage
authStore.initAuth()

// Toggle sync
authStore.toggleSync()
```

#### Usage Example

```typescript
import { useAuthStore } from '@/store/authStore';

const authStore = useAuthStore();

// On app start
authStore.initAuth();

// Check if logged in
if (authStore.isAuthenticated) {
    console.log('User:', authStore.user);
    console.log('Token:', authStore.token);
}

// Login
const result = await authStore.login('john@example.com', 'password123');
if (result.success) {
    console.log('Logged in as:', result.user?.name);
}

// Enable sync
authStore.toggleSync();

// Logout
await authStore.logout();
```

---

## Database Schema

### `users` Table (Laravel Default)

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email_verified_at TIMESTAMP NULL,
    remember_token VARCHAR(100) NULL,
    two_factor_secret VARCHAR(255) NULL,
    two_factor_recovery_codes TEXT NULL,
    two_factor_confirmed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `personal_access_tokens` Table (Laravel Sanctum)

```sql
CREATE TABLE personal_access_tokens (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tokenable_type VARCHAR(255) NOT NULL,
    tokenable_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    token VARCHAR(64) UNIQUE NOT NULL,
    abilities TEXT NULL,
    last_used_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX tokenable (tokenable_type, tokenable_id)
);
```

---

## Security Features

1. **Password Hashing**: Bcrypt hashing via Laravel's `Hash` facade
2. **Token Authentication**: Stateless API tokens via Sanctum
3. **CSRF Protection**: Sanctum handles CSRF for stateful requests
4. **Input Validation**: All inputs validated before processing
5. **Rate Limiting**: Can be configured via Laravel's rate limiter
6. **Token Expiration**: Tokens can have expiration dates set
7. **Multi-Device Support**: Users can have multiple tokens

---

## Setup Instructions

### Backend Setup

1. **Install Sanctum:**
   ```bash
   composer require laravel/sanctum
   ```

2. **Publish Config:**
   ```bash
   php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
   ```

3. **Run Migrations:**
   ```bash
   php artisan migrate
   ```

4. **Add Middleware:**
   In `bootstrap/app.php` or `app/Http/Kernel.php`:
   ```php
   ->withMiddleware(function (Middleware $middleware) {
       $middleware->statefulApi();
   })
   ```

5. **Configure `.env`:**
   ```
   SANCTUM_STATEFUL_DOMAINS=localhost,localhost:3000
   SESSION_DRIVER=cookie
   SESSION_DOMAIN=localhost
   ```

### Frontend Setup

1. **Install Dependencies:**
   ```bash
   cd FrontEndApp
   yarn add pinia axios
   ```

2. **Import Store:**
   In your main.ts or App.vue:
   ```typescript
   import { useAuthStore } from '@/store/authStore';
   
   const authStore = useAuthStore();
   authStore.initAuth();
   ```

---

## Testing

### Manual Testing

1. **Register:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"name":"Test User","email":"test@example.com","password":"password123","password_confirmation":"password123"}'
   ```

2. **Login:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123"}'
   ```

3. **Get User:**
   ```bash
   curl -X GET http://localhost:8000/api/auth/user \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

4. **Logout:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/logout \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Automated Testing

Create test cases in `backend/tests/Feature/AuthTest.php`:

```php
public function test_user_can_register()
{
    $response = $this->post('/api/auth/register', [
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);

    $response->assertStatus(201);
    $response->assertJson(['status' => 'success']);
}

public function test_user_can_login()
{
    User::create([
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => Hash::make('password123'),
    ]);

    $response = $this->post('/api/auth/login', [
        'email' => 'test@example.com',
        'password' => 'password123',
    ]);

    $response->assertStatus(200);
    $response->assertJson(['status' => 'success']);
}
```

---

## Error Handling

### Common Errors

1. **Validation Error (422):**
   ```json
   {
       "message": "The given data was invalid.",
       "errors": {
           "email": ["The email has already been taken."]
       }
   }
   ```

2. **Unauthorized (401):**
   ```json
   {
       "status": "error",
       "message": "Unauthenticated."
   }
   ```

3. **Server Error (500):**
   ```json
   {
       "status": "error",
       "message": "Internal server error"
   }
   ```

### Frontend Error Handling

```typescript
try {
    const result = await authStore.login(email, password);
    if (!result.success) {
        // Show error to user
        alert(result.message);
    }
} catch (error) {
    console.error('Auth error:', error);
    alert('An unexpected error occurred');
}
```

---

## Best Practices

1. **Token Storage**: Store tokens in localStorage for persistence
2. **HTTPS**: Always use HTTPS in production
3. **Token Expiration**: Consider implementing token expiration
4. **Refresh Tokens**: Implement refresh token flow for long sessions
5. **Rate Limiting**: Protect auth endpoints from brute force
6. **Password Strength**: Enforce strong password requirements
7. **Email Verification**: Consider implementing email verification
8. **2FA**: Add two-factor authentication for enhanced security

---

## Integration with Sync System

The auth system integrates with the sync system:

1. User must be authenticated to use sync
2. Token is included in all sync API requests
3. Sync operations are skipped if not authenticated
4. Logout revokes all sync permissions

```typescript
import { useAuthStore } from '@/store/authStore';
import { syncData } from '@/util/Sync/sync';

const authStore = useAuthStore();

if (authStore.isAuthenticated && authStore.syncData) {
    await syncData(syncPayload);
} else {
    console.log('Sync disabled: not authenticated');
}
```

---

## Version History

- **1.0.0** (March 24, 2026): Initial implementation
  - User registration
  - User login
  - Token-based authentication
  - Logout functionality
  - Integration with sync system

---

## Support

For issues or questions, refer to:
- Laravel Sanctum Documentation: https://laravel.com/docs/sanctum
- Pinia Documentation: https://pinia.vuejs.org/
- Believers Sword Documentation: `docs/sync_system.md`
