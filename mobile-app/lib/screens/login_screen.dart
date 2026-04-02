import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

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
    final theme = ShadTheme.of(context);

    // Already logged in — show profile
    if (auth.isAuthenticated) {
      return Scaffold(
        appBar: AppBar(title: const Text('Account')),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            ShadCard(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    Icon(LucideIcons.circleUserRound,
                        size: 64, color: theme.colorScheme.primary),
                    const SizedBox(height: 8),
                    Text(
                      auth.user?['name'] ?? 'User',
                      style: theme.textTheme.large,
                    ),
                    Text(
                      auth.user?['email'] ?? '',
                      style: theme.textTheme.muted,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            ShadCard(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    ShadSwitch(
                      value: auth.syncEnabled,
                      onChanged: (v) => auth.setSyncEnabled(v),
                      label: const Text('Cloud Sync'),
                    ),
                    if (auth.syncEnabled) ...[
                      const SizedBox(height: 8),
                      ShadButton.outline(
                        leading: const Icon(LucideIcons.refreshCw, size: 16),
                        onPressed: () {
                          auth.triggerSync();
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Syncing...')),
                          );
                        },
                        child: const Text('Sync Now'),
                      ),
                    ],
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            ShadButton.destructive(
              leading: const Icon(LucideIcons.logOut, size: 16),
              onPressed: () async {
                await auth.logout();
                if (context.mounted) Navigator.pop(context);
              },
              child: const Text('Logout'),
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
            if (!_isLogin) ...[
              ShadInput(
                controller: _nameController,
                placeholder: const Text('Name'),
              ),
              const SizedBox(height: 12),
            ],
            ShadInput(
              controller: _emailController,
              placeholder: const Text('Email'),
              keyboardType: TextInputType.emailAddress,
            ),
            const SizedBox(height: 12),
            ShadInput(
              controller: _passwordController,
              placeholder: const Text('Password'),
              obscureText: true,
            ),
            if (!_isLogin) ...[
              const SizedBox(height: 12),
              ShadInput(
                controller: _confirmPasswordController,
                placeholder: const Text('Confirm Password'),
                obscureText: true,
              ),
            ],
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 12),
                child: ShadAlert.destructive(
                  title: Text(_error!),
                ),
              ),
            const SizedBox(height: 20),
            ShadButton(
              enabled: !_isLoading,
              onPressed: _submit,
              leading: _isLoading
                  ? SizedBox.square(
                      dimension: 16,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: theme.colorScheme.primaryForeground,
                      ),
                    )
                  : null,
              child: Text(_isLogin ? 'Login' : 'Register'),
            ),
            const SizedBox(height: 8),
            ShadButton.link(
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
