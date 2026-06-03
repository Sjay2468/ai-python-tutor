import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:dio/dio.dart';
import '../constants/api_constants.dart';

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

  /// Perform login against the Flask backend.
  /// Returns null on success, or an error message string on failure.
  Future<String?> login(String email, String password) async {
    final dio = Dio();
    try {
      final response = await dio.post(
        ApiConstants.login,
        data: {'email': email, 'password': password},
      );
      if (response.statusCode == 200) {
        final data = response.data;
        await saveSession(data['token'], data['user']);
        return null; // success
      }
      return 'Login failed. Please try again.';
    } on DioException catch (e) {
      if (e.response != null && e.response!.data is Map) {
        return e.response!.data['error'] ?? 'Login failed. Please try again.';
      }
      return 'Could not connect to server. Please check your internet connection.';
    } catch (e) {
      debugPrint('Login error: $e');
      return 'An unexpected error occurred. Please try again.';
    }
  }

  /// Perform registration against the Flask backend.
  /// Returns null on success, or an error message string on failure.
  Future<String?> register(String fullName, String email, String password, String skillLevel) async {
    final dio = Dio();
    try {
      final response = await dio.post(
        ApiConstants.register,
        data: {
          'full_name': fullName,
          'email': email,
          'password': password,
          'skill_level': skillLevel,
        },
      );
      if (response.statusCode == 201) {
        final data = response.data;
        await saveSession(data['token'], data['user']);
        return null; // success
      }
      return 'Registration failed. Please try again.';
    } on DioException catch (e) {
      if (e.response != null && e.response!.data is Map) {
        return e.response!.data['error'] ?? 'Registration failed. Please try again.';
      }
      return 'Could not connect to server. Please check your internet connection.';
    } catch (e) {
      debugPrint('Registration error: $e');
      return 'An unexpected error occurred. Please try again.';
    }
  }
}
