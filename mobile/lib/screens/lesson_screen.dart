import 'package:flutter/material.dart';
import '../../constants/app_theme.dart';
import '../../services/api_service.dart';
import '../../widgets/code_editor_widget.dart';
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

class _LessonScreenState extends State<LessonScreen>
    with SingleTickerProviderStateMixin {
  final ApiService _api = ApiService();
  bool _isLoading = true;
  Map<String, dynamic>? _lessonData;

  int _currentSection = 0;
  late PageController _pageController;
  late AnimationController _fadeController;
  late Animation<double> _fadeAnimation;

  // Build the ordered list of sections from lesson data
  List<_LessonSection> _sections = [];

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    _fadeController = AnimationController(
      duration: const Duration(milliseconds: 350),
      vsync: this,
    );
    _fadeAnimation =
        CurvedAnimation(parent: _fadeController, curve: Curves.easeInOut);
    _loadLesson();
  }

  @override
  void dispose() {
    _pageController.dispose();
    _fadeController.dispose();
    super.dispose();
  }

  /// Strips any remaining [Source: ...] / [E1] / [R2] etc. citations from text.
  String _stripCitations(String text) {
    return text
        .replaceAll(RegExp(r'\s*\[Source:[^\]]+\]'), '')
        .replaceAll(RegExp(r'\s*\[[ETOR]\d+[^\]]*\]'), '')
        .trim();
  }

  Future<void> _loadLesson() async {
    final data = await _api.getLesson(widget.topicId);
    if (mounted) {
      setState(() {
        _lessonData = data;
        _isLoading = false;
        if (data != null) {
          _buildSections(data);
        }
      });
      _fadeController.forward();
    }
  }

  void _buildSections(Map<String, dynamic> data) {
    _sections = [];

    // Section 1: Overview (explanation)
    final explanation = _stripCitations(data['explanation'] ?? '');
    if (explanation.isNotEmpty) {
      _sections.add(_LessonSection(
        type: _SectionType.explanation,
        title: 'Overview',
        content: explanation,
      ));
    }

    // Section 2: Analogy
    final analogy = data['analogy'] != null
        ? _stripCitations(data['analogy'] as String)
        : null;
    if (analogy != null && analogy.isNotEmpty) {
      _sections.add(_LessonSection(
        type: _SectionType.analogy,
        title: 'Real-World Analogy',
        content: analogy,
      ));
    }

    // Section 3: Code Example + IDE
    final codeExample = data['code_example'] as String?;
    if (codeExample != null && codeExample.isNotEmpty) {
      _sections.add(_LessonSection(
        type: _SectionType.codeExample,
        title: 'Code Example & Playground',
        content: codeExample,
      ));
    }

    // Section 4: Code Breakdown
    final codeBreakdown = data['code_breakdown'] != null
        ? _stripCitations(data['code_breakdown'] as String)
        : null;
    if (codeBreakdown != null && codeBreakdown.isNotEmpty) {
      _sections.add(_LessonSection(
        type: _SectionType.breakdown,
        title: 'How It Works',
        content: codeBreakdown,
      ));
    }

    // Section 5: Key Points
    final keyPoints = data['key_points'] as List<dynamic>?;
    if (keyPoints != null && keyPoints.isNotEmpty) {
      _sections.add(_LessonSection(
        type: _SectionType.keyPoints,
        title: 'Key Points',
        content: '',
        keyPoints: keyPoints.cast<String>(),
      ));
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

  void _goToNextSection() {
    if (_currentSection < _sections.length - 1) {
      _fadeController.reverse().then((_) {
        _pageController.nextPage(
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeInOut,
        );
        _fadeController.forward();
      });
    } else {
      _markReadAndContinue();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: Text(widget.title),
        bottom: _isLoading || _sections.isEmpty
            ? null
            : PreferredSize(
                preferredSize: const Size.fromHeight(6),
                child: _SectionProgressBar(
                  current: _currentSection,
                  total: _sections.length,
                ),
              ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => ChatScreen(initialContext: widget.title),
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
              : _sections.isEmpty
                  ? const Center(child: Text('No content available.'))
                  : FadeTransition(
                      opacity: _fadeAnimation,
                      child: PageView.builder(
                        controller: _pageController,
                        physics: const NeverScrollableScrollPhysics(),
                        onPageChanged: (i) =>
                            setState(() => _currentSection = i),
                        itemCount: _sections.length,
                        itemBuilder: (context, index) {
                          return _SectionPage(
                            section: _sections[index],
                            isLast: index == _sections.length - 1,
                            sectionNumber: index + 1,
                            totalSections: _sections.length,
                            onNext: _goToNextSection,
                          );
                        },
                      ),
                    ),
    );
  }
}

// ── Section progress bar ──────────────────────────────────────────────────────

class _SectionProgressBar extends StatelessWidget {
  final int current;
  final int total;

  const _SectionProgressBar({required this.current, required this.total});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: List.generate(total, (i) {
        final active = i <= current;
        return Expanded(
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            height: 4,
            margin: const EdgeInsets.symmetric(horizontal: 2),
            decoration: BoxDecoration(
              color: active ? AppTheme.primary : AppTheme.divider,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
        );
      }),
    );
  }
}

// ── Section page ──────────────────────────────────────────────────────────────

class _SectionPage extends StatelessWidget {
  final _LessonSection section;
  final bool isLast;
  final int sectionNumber;
  final int totalSections;
  final VoidCallback onNext;

  const _SectionPage({
    required this.section,
    required this.isLast,
    required this.sectionNumber,
    required this.totalSections,
    required this.onNext,
  });

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(24, 20, 24, 120),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Section label
          Row(
            children: [
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppTheme.primaryLight,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  'Section $sectionNumber of $totalSections',
                  style: Theme.of(context).textTheme.labelLarge?.copyWith(
                        color: AppTheme.primary,
                        fontSize: 12,
                      ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Section title
          Text(
            section.title,
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 20),

          // Section body
          _buildBody(context),

          const SizedBox(height: 32),

          // Next / Practice button
          _buildNextButton(context),
        ],
      ),
    );
  }

  Widget _buildBody(BuildContext context) {
    switch (section.type) {
      case _SectionType.explanation:
        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Text(
              section.content,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
          ),
        );

      case _SectionType.analogy:
        return Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                AppTheme.primary.withOpacity(0.06),
                AppTheme.accent.withOpacity(0.06),
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppTheme.primary.withOpacity(0.2)),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Icon(Icons.lightbulb_outline,
                  color: AppTheme.primary, size: 28),
              const SizedBox(width: 16),
              Expanded(
                child: Text(
                  section.content,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: AppTheme.textPrimary,
                        fontStyle: FontStyle.italic,
                      ),
                ),
              ),
            ],
          ),
        );

      case _SectionType.codeExample:
        return ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: CodeEditorWidget(initialCode: section.content),
        );

      case _SectionType.breakdown:
        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Text(
              section.content,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontFamily: 'monospace',
                    fontSize: 14,
                    height: 1.7,
                    color: AppTheme.textPrimary,
                  ),
            ),
          ),
        );

      case _SectionType.keyPoints:
        return Column(
          children: section.keyPoints!.asMap().entries.map((entry) {
            return Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppTheme.surface,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.divider),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 28,
                    height: 28,
                    alignment: Alignment.center,
                    decoration: const BoxDecoration(
                      color: AppTheme.primary,
                      shape: BoxShape.circle,
                    ),
                    child: Text(
                      '${entry.key + 1}',
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 13,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      entry.value,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: AppTheme.textPrimary,
                          ),
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        );
    }
  }

  Widget _buildNextButton(BuildContext context) {
    if (isLast) {
      return Column(
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppTheme.success.withOpacity(0.08),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppTheme.success.withOpacity(0.3)),
            ),
            child: Row(
              children: [
                const Icon(Icons.check_circle,
                    color: AppTheme.success, size: 20),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'You\'ve read all sections! Ready to test your knowledge?',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: AppTheme.success,
                        ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: onNext,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.success,
            ),
            icon: const Icon(Icons.sports_esports_outlined,
                color: Colors.white),
            label: const Text("I've Read This → Practice"),
          ),
        ],
      );
    }

    return ElevatedButton.icon(
      onPressed: onNext,
      icon: const Icon(Icons.arrow_forward_rounded, color: Colors.white),
      label: const Text('Next Section'),
    );
  }
}

// ── Data models ───────────────────────────────────────────────────────────────

enum _SectionType { explanation, analogy, codeExample, breakdown, keyPoints }

class _LessonSection {
  final _SectionType type;
  final String title;
  final String content;
  final List<String>? keyPoints;

  const _LessonSection({
    required this.type,
    required this.title,
    required this.content,
    this.keyPoints,
  });
}
