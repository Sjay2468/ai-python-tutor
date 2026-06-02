import 'package:flutter/material.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/dracula.dart';
import '../../constants/app_theme.dart';
import '../../services/api_service.dart';
import 'practice_screen.dart';
import 'chat_screen.dart';

class LessonScreen extends StatefulWidget {
  final String topicId;
  final String title;

  const LessonScreen({
    super.key,
    required this.topicId,
    required this.title,
  });

  @override
  State<LessonScreen> createState() => _LessonScreenState();
}

class _LessonScreenState extends State<LessonScreen> {
  final ApiService _api = ApiService();
  bool _isLoading = true;
  Map<String, dynamic>? _lessonData;

  @override
  void initState() {
    super.initState();
    _loadLesson();
  }

  Future<void> _loadLesson() async {
    final data = await _api.getLesson(widget.topicId);
    if (mounted) {
      setState(() {
        _lessonData = data;
        _isLoading = false;
      });
    }
  }

  Future<void> _markReadAndContinue() async {
    await _api.markLessonRead(widget.topicId);
    if (!mounted) return;
    
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => PracticeScreen(
          topicId: widget.topicId,
          title: widget.title,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: Text(widget.title),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => ChatScreen(
                initialContext: widget.title,
              ),
            ),
          );
        },
        backgroundColor: AppTheme.primary,
        child: const Icon(Icons.auto_awesome, color: Colors.white),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _lessonData == null
              ? const Center(child: Text('Failed to load lesson.'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Overview Card
                      Card(
                        child: Padding(
                          padding: const EdgeInsets.all(20.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Overview',
                                style: Theme.of(context).textTheme.titleLarge,
                              ),
                              const SizedBox(height: 12),
                              Text(
                                _lessonData!['explanation'] ?? '',
                                style: Theme.of(context).textTheme.bodyLarge,
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 24),

                      // Analogy Card
                      if (_lessonData!['analogy'] != null) ...[
                        Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: AppTheme.primaryLight,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: AppTheme.primary.withOpacity(0.2)),
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Icon(Icons.lightbulb_outline, color: AppTheme.primary),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Analogy',
                                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                            color: AppTheme.primary,
                                          ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      _lessonData!['analogy'],
                                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                            color: AppTheme.textPrimary,
                                          ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // Code Snippet
                      if (_lessonData!['code_example'] != null) ...[
                        Text(
                          'Code Example',
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                        const SizedBox(height: 12),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(16),
                          child: HighlightView(
                            _lessonData!['code_example'],
                            language: 'python',
                            theme: draculaTheme,
                            padding: const EdgeInsets.all(16),
                            textStyle: const TextStyle(
                              fontFamily: 'monospace',
                              fontSize: 14,
                              height: 1.5,
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // Code Breakdown
                      if (_lessonData!['code_breakdown'] != null) ...[
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'How it works',
                                  style: Theme.of(context).textTheme.titleLarge,
                                ),
                                const SizedBox(height: 12),
                                Text(
                                  _lessonData!['code_breakdown'],
                                  style: Theme.of(context).textTheme.bodyMedium,
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 32),
                      ],

                      ElevatedButton(
                        onPressed: _markReadAndContinue,
                        child: const Text("I've Read This -> Practice"),
                      ),
                    ],
                  ),
                ),
    );
  }
}
