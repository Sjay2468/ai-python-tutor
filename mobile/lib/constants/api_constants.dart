/// Central place for all API endpoint constants.
class ApiConstants {
  // Deployed production backend URL
  static const String baseUrl = 'https://ai-python-tutor-ten.vercel.app/api/v1';

  // Auth
  static const String register = '$baseUrl/auth/register';
  static const String login = '$baseUrl/auth/login';
  static const String logout = '$baseUrl/auth/logout';

  // Lessons
  static const String lessons = '$baseUrl/lessons';
  static String lessonById(String id) => '$baseUrl/lessons/$id';
  static String markStudied(String id) => '$baseUrl/lessons/$id/study';

  // Practice
  static String practice(String topicId) => '$baseUrl/practice/$topicId';
  static String submitAnswer(String topicId) => '$baseUrl/practice/$topicId/submit';
  static String completePractice(String topicId) => '$baseUrl/practice/$topicId/complete';

  // Chat
  static const String chat = '$baseUrl/chat';

  // Progress
  static const String progress = '$baseUrl/progress';
  static String progressByTopic(String topicId) => '$baseUrl/progress/$topicId';
}
