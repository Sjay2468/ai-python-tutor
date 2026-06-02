import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../constants/app_theme.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import 'auth/welcome_screen.dart';
import 'lesson_screen.dart';
import 'progress_screen.dart';
import 'chat_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService _api = ApiService();
  bool _isLoading = true;
  List<dynamic> _topics = [];
  Map<String, dynamic>? _progress;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    
    final results = await Future.wait([
      _api.getTopics(),
      _api.getProgress(),
    ]);

    if (mounted) {
      setState(() {
        _topics = results[0] as List<dynamic>;
        _progress = results[1] as Map<String, dynamic>?;
        _isLoading = false;
      });
    }
  }

  void _handleLogout() async {
    await context.read<AuthService>().logout();
    if (!mounted) return;
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (_) => const WelcomeScreen()),
      (route) => false,
    );
  }

  Widget _buildTopicCard(Map<String, dynamic> topic) {
    // Topic comes from /lessons/topics. Status requires cross-referencing with progress.
    final topicId = topic['id'];
    final topicProgress = _progress?['topics']?.firstWhere(
      (t) => t['topic_id'] == topicId,
      orElse: () => null,
    );

    final isMastered = topicProgress?['is_mastered'] ?? false;
    final isStarted = topicProgress != null;

    IconData iconData = Icons.radio_button_unchecked;
    Color iconColor = AppTheme.divider;

    if (isMastered) {
      iconData = Icons.check_circle;
      iconColor = AppTheme.success;
    } else if (isStarted) {
      iconData = Icons.play_circle_fill;
      iconColor = AppTheme.warning;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => LessonScreen(
                topicId: topicId,
                title: topic['title'],
              ),
            ),
          ).then((_) => _loadData()); // Refresh progress when returning
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            children: [
              Icon(iconData, color: iconColor, size: 28),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      topic['title'] ?? 'Unknown Topic',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      topic['description'] ?? '',
                      style: Theme.of(context).textTheme.bodyMedium,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: AppTheme.textSecondary),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthService>().user;
    final userName = user?['full_name']?.split(' ').first ?? 'Student';
    
    // Overall progress percentage
    final overallProgress = _progress?['overall_progress_percentage'] ?? 0.0;
    final progressVal = overallProgress / 100.0;

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: const Text('Python Tutor'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _handleLogout,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const ChatScreen()),
          );
        },
        backgroundColor: AppTheme.primary,
        icon: const Icon(Icons.auto_awesome, color: Colors.white),
        label: const Text('AI Mentor', style: TextStyle(color: Colors.white)),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadData,
              child: ListView(
                padding: const EdgeInsets.all(24.0),
                children: [
                  Text(
                    'Hello, $userName! 👋',
                    style: Theme.of(context).textTheme.headlineLarge,
                  ),
                  const SizedBox(height: 24),
                  
                  // Global Progress Card
                  GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const ProgressScreen()),
                      );
                    },
                    child: Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: AppTheme.primary,
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: [
                          BoxShadow(
                            color: AppTheme.primary.withOpacity(0.3),
                            blurRadius: 10,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Row(
                        children: [
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Your Journey',
                                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                        color: Colors.white,
                                      ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  '${overallProgress.toInt()}% Completed',
                                  style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                                        color: Colors.white,
                                      ),
                                ),
                              ],
                            ),
                          ),
                          Stack(
                            alignment: Alignment.center,
                            children: [
                              SizedBox(
                                width: 60,
                                height: 60,
                                child: CircularProgressIndicator(
                                  value: progressVal,
                                  backgroundColor: Colors.white.withOpacity(0.2),
                                  color: Colors.white,
                                  strokeWidth: 6,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 32),
                  Text(
                    'Topics',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 16),
                  
                  // Topic List
                  ..._topics.map((t) => _buildTopicCard(t)),
                  const SizedBox(height: 40),
                ],
              ),
            ),
    );
  }
}
