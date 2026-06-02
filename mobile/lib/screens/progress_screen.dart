import 'package:flutter/material.dart';
import 'package:percent_indicator/circular_percent_indicator.dart';
import '../../constants/app_theme.dart';
import '../../services/api_service.dart';

class ProgressScreen extends StatefulWidget {
  const ProgressScreen({super.key});

  @override
  State<ProgressScreen> createState() => _ProgressScreenState();
}

class _ProgressScreenState extends State<ProgressScreen> {
  final ApiService _api = ApiService();
  bool _isLoading = true;
  Map<String, dynamic>? _progress;

  @override
  void initState() {
    super.initState();
    _loadProgress();
  }

  Future<void> _loadProgress() async {
    final data = await _api.getProgress();
    if (mounted) {
      setState(() {
        _progress = data;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text('My Progress')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_progress == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('My Progress')),
        body: const Center(child: Text('Failed to load progress data.')),
      );
    }

    final overallProgress = _progress!['overall_progress_percentage'] ?? 0.0;
    final topics = _progress!['topics'] as List<dynamic>? ?? [];
    
    int masteredCount = topics.where((t) => t['is_mastered'] == true).length;
    int totalTopics = 9;

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: const Text('Detailed Progress'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            // Big Circular Progress
            CircularPercentIndicator(
              radius: 80.0,
              lineWidth: 16.0,
              percent: overallProgress / 100.0,
              center: Text(
                '${overallProgress.toInt()}%',
                style: Theme.of(context).textTheme.headlineLarge,
              ),
              progressColor: AppTheme.success,
              backgroundColor: AppTheme.divider.withOpacity(0.5),
              circularStrokeCap: CircularStrokeCap.round,
              animation: true,
              animationDuration: 1200,
            ),
            const SizedBox(height: 32),
            
            // Stats Row
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    context, 
                    'Topics Mastered', 
                    '$masteredCount / $totalTopics',
                    Icons.workspace_premium,
                    AppTheme.warning,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _buildStatCard(
                    context, 
                    'Topics Started', 
                    '${topics.length}',
                    Icons.play_circle_fill,
                    AppTheme.primary,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 32),
            
            // Topic Breakdown
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                'Topic Breakdown',
                style: Theme.of(context).textTheme.titleLarge,
              ),
            ),
            const SizedBox(height: 16),
            ...topics.map((t) {
              final isMastered = t['is_mastered'] ?? false;
              return ListTile(
                contentPadding: EdgeInsets.zero,
                leading: Icon(
                  isMastered ? Icons.check_circle : Icons.trending_up,
                  color: isMastered ? AppTheme.success : AppTheme.warning,
                  size: 32,
                ),
                title: Text(
                  t['topic_id'],
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                subtitle: Text(
                  'Mastery Score: ${t['mastery_score']}/3',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
                trailing: Text(
                  isMastered ? 'Mastered' : 'In Progress',
                  style: Theme.of(context).textTheme.labelLarge?.copyWith(
                    color: isMastered ? AppTheme.success : AppTheme.warning,
                  ),
                ),
              );
            }).toList(),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(BuildContext context, String title, String value, IconData icon, Color color) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 12),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 4),
            Text(
              title,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
}
