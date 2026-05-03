import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Manages authentication state: login, registration, token persistence.
class AuthService extends ChangeNotifier {
  String? _token;
  Map<String, dynamic>? _user;

  String? get token => _token;
  Map<String, dynamic>? get user => _user;
  bool get isAuthenticated => _token != null;

  /// Load saved token from local storage on app start.
  Future<void> loadToken() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('jwt_token');
    final name = prefs.getString('user_name');
    final email = prefs.getString('user_email');
    if (_token != null && name != null) {
      _user = {'full_name': name, 'email': email};
    }
    notifyListeners();
  }

  /// Save token and user info after successful login/register.
  Future<void> saveSession(String token, Map<String, dynamic> user) async {
    _token = token;
    _user = user;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('jwt_token', token);
    await prefs.setString('user_name', user['full_name'] ?? '');
    await prefs.setString('user_email', user['email'] ?? '');
    notifyListeners();
  }

  /// Clear token and user on logout.
  Future<void> logout() async {
    _token = null;
    _user = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    notifyListeners();
  }
}
