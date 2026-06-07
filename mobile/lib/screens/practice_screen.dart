import 'package:flutter/material.dart';
import '../../constants/app_theme.dart';
import '../../services/api_service.dart';

class PracticeScreen extends StatefulWidget {
  final String topicId;
  final String title;

  const PracticeScreen({
    super.key,
    required this.topicId,
    required this.title,
  });

  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen>
    with SingleTickerProviderStateMixin {
  final ApiService _api = ApiService();
  bool _isLoading = true;
  List<dynamic>? _questions;
  int _currentIndex = 0;
  List<_QuestionProgressState> _questionStates = [];
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _loadQuestions();
  }

  Future<void> _loadQuestions() async {
    setState(() => _isLoading = true);
    final data = await _api.getPracticeQuestion(widget.topicId);
    if (mounted) {
      setState(() {
        if (data != null && data.containsKey('questions')) {
          _questions = data['questions'];
          _questionStates = List.generate(
            _questions!.length,
            (_) => _QuestionProgressState(),
          );
        } else if (data != null && data.containsKey('message')) {
          _questions = []; // mastered
          _questionStates = [];
        } else {
          _questions = null;
          _questionStates = [];
        }
        _isLoading = false;
      });
    }
  }

  Future<void> _submitAnswer() async {
    final state = _questionStates[_currentIndex];
    if (state.selectedOption == null || state.isAnswerLocked) return;
    setState(() {
      _isSubmitting = true;
      state.isAnswerLocked = true; // lock immediately on submit
    });

    final currentQ = _questions![_currentIndex];
    final questionId = currentQ['id'].toString();

    final result = await _api.submitAnswer(
      widget.topicId,
      questionId,
      state.selectedOption!,
      1, // always attempt 1 — hint progression removed in favour of locking
    );

    if (!mounted) return;
    setState(() {
      _isSubmitting = false;
      if (result != null) {
        state.isCorrect = result['correct'] ?? false;
        state.feedbackHint = result['hint'] as String?;
        state.correctOption = result['correct_option'] as String?;
        state.correctOptionText = result['correct_option_text'] as String?;
      }
    });
  }

  void _prevQuestion() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
      });
    }
  }

  void _nextQuestion() {
    if (_currentIndex < _questions!.length - 1) {
      setState(() {
        _currentIndex++;
      });
    } else {
      _finishPractice();
    }
  }

  Future<void> _finishPractice() async {
    final total = _questions!.length;
    final correct = _questionStates.where((q) => q.isCorrect).length;

    // Show score splash then call complete API
    await _showScoreSplash(correct, total);

    // Save result to backend
    await _api.completePractice(widget.topicId, correct, total);

    if (mounted) {
      Navigator.pop(context);
    }
  }

  /// Shows a full-screen score splash for 3 seconds then resolves.
  Future<void> _showScoreSplash(int correct, int total) async {
    final scorePercent = total > 0 ? ((correct / total) * 100).round() : 0;
    final mastered = scorePercent >= 70;

    final completer = Future.delayed(const Duration(seconds: 3));

    await showGeneralDialog(
      context: context,
      barrierDismissible: false,
      barrierColor: Colors.black87,
      pageBuilder: (ctx, anim, secondAnim) {
        return _ScoreSplashDialog(
          correct: correct,
          total: total,
          scorePercent: scorePercent,
          mastered: mastered,
          dismissAfter: completer,
        );
      },
      transitionBuilder: (ctx, anim, secondAnim, child) {
        return FadeTransition(
          opacity: anim,
          child: ScaleTransition(
            scale: CurvedAnimation(parent: anim, curve: Curves.easeOutBack),
            child: child,
          ),
        );
      },
      transitionDuration: const Duration(milliseconds: 400),
    );
  }

  // ── Option button builder ─────────────────────────────────────────────────

  Widget _buildOptionButton(String key, String text) {
    final state = _questionStates[_currentIndex];
    final isSelected = state.selectedOption == key;
    final isCorrectKey = state.correctOption == key;

    Color bgColor = AppTheme.surface;
    Color borderColor = AppTheme.divider;
    Color textColor = AppTheme.textPrimary;
    Widget? trailingIcon;

    if (state.isAnswerLocked) {
      if (isCorrectKey) {
        bgColor = AppTheme.success.withOpacity(0.1);
        borderColor = AppTheme.success;
        textColor = AppTheme.success;
        trailingIcon = const Icon(Icons.check_circle, color: AppTheme.success, size: 20);
      } else if (isSelected && !state.isCorrect) {
        bgColor = AppTheme.error.withOpacity(0.08);
        borderColor = AppTheme.error;
        textColor = AppTheme.error;
        trailingIcon = const Icon(Icons.cancel, color: AppTheme.error, size: 20);
      } else {
        bgColor = AppTheme.surface;
        borderColor = AppTheme.divider.withOpacity(0.4);
        textColor = AppTheme.textSecondary.withOpacity(0.5);
      }
    } else if (isSelected) {
      bgColor = AppTheme.primaryLight;
      borderColor = AppTheme.primary;
      textColor = AppTheme.primary;
    }

    return AnimatedContainer(
      duration: const Duration(milliseconds: 250),
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: borderColor,
          width: isSelected || (isCorrectKey && state.isAnswerLocked) ? 2 : 1,
        ),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: state.isAnswerLocked
            ? null
            : () => setState(() => state.selectedOption = key),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 32,
                height: 32,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: borderColor),
                  color: (isSelected && !state.isAnswerLocked)
                      ? AppTheme.primary
                      : Colors.transparent,
                ),
                child: Text(
                  key.toUpperCase(),
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: (isSelected && !state.isAnswerLocked)
                        ? Colors.white
                        : textColor,
                    fontSize: 13,
                  ),
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Text(
                  text,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: textColor,
                        fontWeight: isSelected || isCorrectKey
                            ? FontWeight.w600
                            : FontWeight.normal,
                      ),
                ),
              ),
              if (trailingIcon != null) ...[
                const SizedBox(width: 8),
                trailingIcon,
              ],
            ],
          ),
        ),
      ),
    );
  }

  // ── Feedback area ─────────────────────────────────────────────────────────

  Widget _buildFeedback() {
    final state = _questionStates[_currentIndex];
    if (!state.isAnswerLocked) return const SizedBox.shrink();

    return AnimatedOpacity(
      opacity: state.isAnswerLocked ? 1.0 : 0.0,
      duration: const Duration(milliseconds: 300),
      child: Container(
        margin: const EdgeInsets.only(bottom: 24),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: state.isCorrect
              ? AppTheme.success.withOpacity(0.08)
              : AppTheme.error.withOpacity(0.08),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: state.isCorrect ? AppTheme.success : AppTheme.error,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(
                  state.isCorrect ? Icons.check_circle : Icons.info_outline,
                  color: state.isCorrect ? AppTheme.success : AppTheme.error,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    state.isCorrect
                        ? '✅ Correct! Well done.'
                        : '❌ Not quite.',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          color: state.isCorrect ? AppTheme.success : AppTheme.error,
                          fontSize: 16,
                        ),
                  ),
                ),
              ],
            ),
            if (state.feedbackHint != null && state.feedbackHint!.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(
                state.feedbackHint!,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppTheme.textSecondary,
                    ),
              ),
            ],
            if (!state.isCorrect &&
                state.correctOption != null &&
                state.correctOptionText != null) ...[
              const SizedBox(height: 10),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: AppTheme.success.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: AppTheme.success.withOpacity(0.3)),
                ),
                child: Row(
                  children: [
                    Text(
                      'Correct answer: ',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            fontWeight: FontWeight.w600,
                            color: AppTheme.success,
                          ),
                    ),
                    Text(
                      '${state.correctOption}. ${state.correctOptionText}',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: AppTheme.success,
                          ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  // ── Build ─────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final isMastered = _questions != null && _questions!.isEmpty;

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: Text('Practice: ${widget.title}'),
        bottom: (!_isLoading && _questions != null && _questions!.isNotEmpty)
            ? PreferredSize(
                preferredSize: const Size.fromHeight(6),
                child: _QuestionProgressBar(
                  current: _currentIndex,
                  total: _questions!.length,
                ),
              )
            : null,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _questions == null
              ? const Center(child: Text('Failed to load practice.'))
              : isMastered
                  ? _buildMasteredView()
                  : _buildQuestionView(),
    );
  }

  Widget _buildMasteredView() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.workspace_premium,
                size: 80, color: AppTheme.warning),
            const SizedBox(height: 24),
            Text('Topic Mastered!',
                style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 8),
            Text(
              'You have already mastered this topic. Keep up the great work!',
              style: Theme.of(context)
                  .textTheme
                  .bodyMedium
                  ?.copyWith(color: AppTheme.textSecondary),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Return Home'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuestionView() {
    final currentQ = _questions![_currentIndex];
    final options =
        (currentQ['options'] as Map<String, dynamic>? ?? {});
    final isLastQuestion = _currentIndex == _questions!.length - 1;
    final state = _questionStates[_currentIndex];
    final showPrev = _currentIndex > 0;

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(24, 20, 24, 40),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Score counter
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Question ${_currentIndex + 1} of ${_questions!.length}',
                style: Theme.of(context).textTheme.labelLarge?.copyWith(
                      color: AppTheme.textSecondary,
                    ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                decoration: BoxDecoration(
                  color: AppTheme.primaryLight,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  '✓ ${_questionStates.where((q) => q.isCorrect).length} correct',
                  style: Theme.of(context).textTheme.labelLarge?.copyWith(
                        color: AppTheme.primary,
                        fontSize: 12,
                      ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Question card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Text(
                currentQ['question_text'] ?? '',
                style: Theme.of(context).textTheme.titleLarge,
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Answer options
          ...options.entries
              .map((e) => _buildOptionButton(e.key, e.value.toString())),

          const SizedBox(height: 8),

          // Feedback
          _buildFeedback(),

          // Navigation and Action buttons
          Row(
            children: [
              if (showPrev) ...[
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _prevQuestion,
                    icon: const Icon(Icons.arrow_back_rounded, color: AppTheme.primary),
                    label: const Text('Back'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: AppTheme.primary,
                      side: const BorderSide(color: AppTheme.primary),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
              ],
              Expanded(
                flex: 2,
                child: !state.isAnswerLocked
                    ? ElevatedButton(
                        onPressed:
                            (state.selectedOption == null || _isSubmitting)
                                ? null
                                : _submitAnswer,
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                        child: _isSubmitting
                            ? const SizedBox(
                                height: 22,
                                width: 22,
                                child: CircularProgressIndicator(
                                    color: Colors.white, strokeWidth: 2),
                              )
                            : const Text('Submit Answer'),
                      )
                    : ElevatedButton.icon(
                        onPressed: _nextQuestion,
                        style: ElevatedButton.styleFrom(
                          backgroundColor:
                              state.isCorrect ? AppTheme.success : AppTheme.primary,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                        icon: Icon(
                          isLastQuestion
                              ? Icons.emoji_events_outlined
                              : Icons.arrow_forward_rounded,
                          color: Colors.white,
                        ),
                        label: Text(
                          isLastQuestion ? 'See Results' : 'Next Question',
                        ),
                      ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

// ── Question progress bar ─────────────────────────────────────────────────────

class _QuestionProgressBar extends StatelessWidget {
  final int current;
  final int total;

  const _QuestionProgressBar({required this.current, required this.total});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: List.generate(total, (i) {
        Color color;
        if (i < current) {
          color = AppTheme.success;
        } else if (i == current) {
          color = AppTheme.primary;
        } else {
          color = AppTheme.divider;
        }
        return Expanded(
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            height: 4,
            margin: const EdgeInsets.symmetric(horizontal: 2),
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
        );
      }),
    );
  }
}

// ── Score splash dialog ───────────────────────────────────────────────────────

class _ScoreSplashDialog extends StatefulWidget {
  final int correct;
  final int total;
  final int scorePercent;
  final bool mastered;
  final Future<void> dismissAfter;

  const _ScoreSplashDialog({
    required this.correct,
    required this.total,
    required this.scorePercent,
    required this.mastered,
    required this.dismissAfter,
  });

  @override
  State<_ScoreSplashDialog> createState() => _ScoreSplashDialogState();
}

class _ScoreSplashDialogState extends State<_ScoreSplashDialog>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnim;
  late Animation<double> _progressAnim;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 800));
    _scaleAnim =
        CurvedAnimation(parent: _controller, curve: Curves.elasticOut);
    _progressAnim = Tween<double>(begin: 0, end: widget.scorePercent / 100.0)
        .animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));
    _controller.forward();

    // Auto-dismiss
    widget.dismissAfter.then((_) {
      if (mounted) Navigator.of(context).pop();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final mastered = widget.mastered;

    return Center(
      child: ScaleTransition(
        scale: _scaleAnim,
        child: Container(
          margin: const EdgeInsets.all(32),
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 40),
          decoration: BoxDecoration(
            color: AppTheme.surface,
            borderRadius: BorderRadius.circular(28),
            boxShadow: [
              BoxShadow(
                color: (mastered ? AppTheme.success : AppTheme.primary)
                    .withOpacity(0.25),
                blurRadius: 40,
                spreadRadius: 4,
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Icon
              AnimatedBuilder(
                animation: _scaleAnim,
                builder: (_, __) => Transform.scale(
                  scale: _scaleAnim.value,
                  child: Icon(
                    mastered
                        ? Icons.emoji_events_rounded
                        : Icons.school_rounded,
                    size: 72,
                    color: mastered ? AppTheme.warning : AppTheme.primary,
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Score number
              AnimatedBuilder(
                animation: _progressAnim,
                builder: (_, __) => Text(
                  '${(_progressAnim.value * 100).round()}%',
                  style: Theme.of(context)
                      .textTheme
                      .headlineLarge
                      ?.copyWith(fontSize: 56, height: 1),
                ),
              ),
              const SizedBox(height: 8),

              Text(
                '${widget.correct} / ${widget.total} correct',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: AppTheme.textSecondary,
                    ),
              ),
              const SizedBox(height: 20),

              // Circular progress
              SizedBox(
                width: 100,
                height: 100,
                child: AnimatedBuilder(
                  animation: _progressAnim,
                  builder: (_, __) => CircularProgressIndicator(
                    value: _progressAnim.value,
                    strokeWidth: 10,
                    backgroundColor: AppTheme.divider,
                    color: mastered ? AppTheme.success : AppTheme.primary,
                    strokeCap: StrokeCap.round,
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Message
              Text(
                mastered
                    ? '🎉 Topic Mastered!'
                    : 'Keep practising — you\'ve got this!',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      color:
                          mastered ? AppTheme.success : AppTheme.textPrimary,
                    ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),

              Text(
                mastered
                    ? 'Your Journey progress has been updated.'
                    : 'Score ${widget.scorePercent}%. Need 70% to master.',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppTheme.textSecondary,
                    ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),

              // Auto-dismiss hint
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.timer_outlined,
                      size: 14, color: Colors.grey),
                  const SizedBox(width: 4),
                  Text(
                    'Returning in 3 seconds...',
                    style: Theme.of(context)
                        .textTheme
                        .bodyMedium
                        ?.copyWith(color: Colors.grey, fontSize: 12),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _QuestionProgressState {
  String? selectedOption;
  bool isAnswerLocked = false;
  bool isCorrect = false;
  String? feedbackHint;
  String? correctOption;
  String? correctOptionText;
}
