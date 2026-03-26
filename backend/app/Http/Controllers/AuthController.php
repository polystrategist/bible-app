<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    /**
     * Register a new user
     * 
     * POST /api/auth/register
     * 
     * @bodyParam name string required The user's name
     * @bodyParam email string required The user's email address
     * @bodyParam password string required The password (min 8 characters)
     * @bodyParam password_confirmation string required Password confirmation
     * 
     * @response 201 {
     *   "status": "success",
     *   "message": "User registered successfully",
     *   "user": {
     *     "id": 1,
     *     "name": "John Doe",
     *     "email": "john@example.com"
     *   },
     *   "token": "1|abc123..."
     * }
     */
    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'status' => 'success',
            'message' => 'User registered successfully',
            'user' => $user,
            'token' => $token,
        ], 201);
    }

    /**
     * Login user
     * 
     * POST /api/auth/login
     * 
     * @bodyParam email string required The user's email address
     * @bodyParam password string required The password
     * 
     * @response 200 {
     *   "status": "success",
     *   "message": "Login successful",
     *   "user": {
     *     "id": 1,
     *     "name": "John Doe",
     *     "email": "john@example.com"
     *   },
     *   "token": "1|abc123..."
     * }
     * 
     * @response 401 {
     *   "status": "error",
     *   "message": "Invalid credentials"
     * }
     */
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|string|email',
            'password' => 'required|string',
        ]);

        if (!Auth::attempt($request->only('email', 'password'))) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        $user = User::where('email', $request->email)->firstOrFail();
        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'status' => 'success',
            'message' => 'Login successful',
            'user' => $user,
            'token' => $token,
        ]);
    }

    /**
     * Logout user (revoke all tokens)
     * 
     * POST /api/auth/logout
     * 
     * @authenticated
     * 
     * @response 200 {
     *   "status": "success",
     *   "message": "Successfully logged out"
     * }
     */
    public function logout(Request $request)
    {
        $request->user()->tokens()->delete();

        return response()->json([
            'status' => 'success',
            'message' => 'Successfully logged out',
        ]);
    }

    /**
     * Get authenticated user
     * 
     * GET /api/auth/user
     * 
     * @authenticated
     * 
     * @response 200 {
     *   "status": "success",
     *   "user": {
     *     "id": 1,
     *     "name": "John Doe",
     *     "email": "john@example.com"
     *   }
     * }
     */
    public function user(Request $request)
    {
        return response()->json([
            'status' => 'success',
            'user' => $request->user(),
        ]);
    }
}
