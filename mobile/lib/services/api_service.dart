import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/api_constants.dart';

/// Base API client that attaches the JWT token to every request.
class ApiService {
  final Dio _dio;

  ApiService() : _dio = Dio(BaseOptions(baseUrl: ApiConstants.baseUrl)) {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final prefs = await SharedPreferences.getInstance();
          final token = prefs.getString('jwt_token');
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
      ),
    );
  }

  /// Get list of topics
  Future<List<dynamic>> getTopics() async {
    try {
      final response = await _dio.get('/lessons');
      return response.data['lessons'] as List<dynamic>;
    } catch (e) {
      return [];
    }
  }

  /// Get overall progress
  Future<Map<String, dynamic>?> getProgress() async {
    try {
      final response = await _dio.get('/progress/summary');
      return response.data;
    } catch (e) {
      return null;
    }
  }

  /// Get specific lesson full content
  Future<Map<String, dynamic>?> getLesson(String topicId) async {
    try {
      final response = await _dio.get('/lessons/$topicId');
      return response.data['lesson'];
    } catch (e) {
      return null;
    }
  }

  /// Mark a lesson as read (studied)
  Future<bool> markLessonRead(String topicId) async {
    try {
      final response = await _dio.post('/lessons/$topicId/study');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// Get a practice question for a topic
  Future<Map<String, dynamic>?> getPracticeQuestion(String topicId) async {
    try {
      final response = await _dio.get('/practice/$topicId');
      return response.data; // Note: returns { 'message' } if mastered/no questions
    } catch (e) {
      return null;
    }
  }

  /// Submit an answer to a practice question
  Future<Map<String, dynamic>?> submitAnswer(String topicId, String questionId, String selectedOption, int attemptNumber) async {
    try {
      final response = await _dio.post(
        '/practice/$topicId/submit',
        data: {
          'question_id': questionId,
          'selected_option': selectedOption,
          'attempt_number': attemptNumber,
        },
      );
      return response.data;
    } catch (e) {
      return null;
    }
  }

  /// Send a message to the Hybrid AI Chat
  Future<Map<String, dynamic>?> sendMessage(String message, {Map<String, dynamic>? contextData}) async {
    try {
      final response = await _dio.post(
        '/chat',
        data: {
          'query': message,                                    // backend expects 'query'
          'current_topic_id': contextData?['current_topic'],  // backend expects 'current_topic_id'
        },
      );
      return response.data; // e.g. { "response": "...", "source": "rule" }
    } catch (e) {
      return {
        'response': "I'm having trouble connecting right now. Please try again later.",
        'source': 'error',
      };
    }
  }

}
