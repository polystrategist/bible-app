import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _nameController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  bool _isLogin = true;
  bool _isLoading = false;
  String? _error;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _nameController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    final auth = context.read<AuthProvider>();
    Map<String, dynamic> result;

    if (_isLogin) {
      result = await auth.login(
        _emailController.text.trim(),
        _passwordController.text,
      );
    } else {
      result = await auth.register(
        _nameController.text.trim(),
        _emailController.text.trim(),
        _passwordController.text,
        _confirmPasswordController.text,
      );
    }

    if (!mounted) return;

    setState(() => _isLoading = false);

    if (result['success'] == true) {
      Navigator.pop(context);
    } else {
      setState(() => _error = result['message'] as String?);
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();

    // Already logged in — show profile
    if (auth.isAuthenticated) {
      return Scaffold(
        appBar: AppBar(title: const Text('Account')),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    const Icon(Icons.account_circle, size: 64),
                    const SizedBox(height: 8),
                    Text(
                      auth.user?['name'] ?? 'User',
                      style: const TextStyle(
                          fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      auth.user?['email'] ?? '',
                      style: TextStyle(
                          color: Theme.of(context).colorScheme.onSurfaceVariant),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            SwitchListTile(
              title: const Text('Cloud Sync'),
              subtitle: const Text('Sync bookmarks, highlights, and notes'),
              value: auth.syncEnabled,
              onChanged: (v) => auth.setSyncEnabled(v),
            ),
            if (auth.syncEnabled)
              ListTile(
                leading: const Icon(Icons.sync),
                title: const Text('Sync Now'),
                onTap: () {
                  auth.triggerSync();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Syncing...')),
                  );
                },
              ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.logout, color: Colors.red),
              title: const Text('Logout', style: TextStyle(color: Colors.red)),
              onTap: () async {
                await auth.logout();
                if (context.mounted) Navigator.pop(context);
              },
            ),
          ],
        ),
      );
    }

    // Login / Register form
    return Scaffold(
      appBar: AppBar(title: Text(_isLogin ? 'Login' : 'Register')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (!_isLogin)
              TextField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Name',
                  border: OutlineInputBorder(),
                ),
              ),
            if (!_isLogin) const SizedBox(height: 12),
            TextField(
              controller: _emailController,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
            ),
            if (!_isLogin) ...[
              const SizedBox(height: 12),
              TextField(
                controller: _confirmPasswordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Confirm Password',
                  border: OutlineInputBorder(),
                ),
              ),
            ],
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 12),
                child: Text(
                  _error!,
                  style: TextStyle(color: Theme.of(context).colorScheme.error),
                ),
              ),
            const SizedBox(height: 20),
            FilledButton(
              onPressed: _isLoading ? null : _submit,
              child: _isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : Text(_isLogin ? 'Login' : 'Register'),
            ),
            TextButton(
              onPressed: () => setState(() {
                _isLogin = !_isLogin;
                _error = null;
              }),
              child: Text(_isLogin
                  ? 'Don\'t have an account? Register'
                  : 'Already have an account? Login'),
            ),
          ],
        ),
      ),
    );
  }
}
