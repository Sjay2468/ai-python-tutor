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

class _PracticeScreenState extends State<PracticeScreen> {
  final ApiService _api = ApiService();
  bool _isLoading = true;
  List<dynamic>? _questions;
  int _currentIndex = 0;
  int _attemptNumber = 1;
  int _correctCount = 0;
  
  String? _selectedOption;
  bool _isSubmitting = false;
  
  // Feedback state
  bool _showFeedback = false;
  bool _isCorrect = false;
  String? _hint;
  Map<String, Color> _optionColors = {};

  @override
  void initState() {
    super.initState();
    _loadQuestion();
  }

  Future<void> _loadQuestion() async {
    setState(() {
      _isLoading = true;
      _showFeedback = false;
      _selectedOption = null;
      _hint = null;
      _optionColors = {};
      _attemptNumber = 1;
    });

    final data = await _api.getPracticeQuestion(widget.topicId);
    if (mounted) {
      setState(() {
        if (data != null && data.containsKey('questions')) {
          _questions = data['questions'];
        } else if (data != null && data.containsKey('message')) {
          // Mastered
          _questions = []; 
        } else {
          _questions = null;
        }
        _isLoading = false;
      });
    }
  }

  Future<void> _submitAnswer() async {
    if (_selectedOption == null) return;
    
    setState(() => _isSubmitting = true);
    
    final currentQuestion = _questions![_currentIndex];
    final questionId = currentQuestion['id'].toString();
    final result = await _api.submitAnswer(widget.topicId, questionId, _selectedOption!, _attemptNumber);
    
    if (!mounted) return;

    if (result != null) {
      setState(() {
        _showFeedback = true;
        _isCorrect = result['correct'] ?? false;
        
        if (_isCorrect) {
          _optionColors[_selectedOption!] = AppTheme.success;
          _hint = "Great job! That's the correct answer.";
          _correctCount++;
        } else {
          _optionColors[_selectedOption!] = AppTheme.error;
          _hint = result['hint'] ?? "Incorrect. Try again!";
          _attemptNumber++;
        }
      });
    }
    
    setState(() => _isSubmitting = false);
  }

  void _nextQuestion() {
    if (_currentIndex < _questions!.length - 1) {
      setState(() {
        _currentIndex++;
        _showFeedback = false;
        _selectedOption = null;
        _hint = null;
        _optionColors = {};
        _attemptNumber = 1;
      });
    } else {
      // Completed all questions
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Practice complete! Score: $_correctCount/${_questions!.length}')),
      );
      Navigator.pop(context);
    }
  }

  Widget _buildOptionButton(String key, String text) {
    Color bgColor = AppTheme.surface;
    Color borderColor = AppTheme.divider;
    Color textColor = AppTheme.textPrimary;

    if (_optionColors.containsKey(key)) {
      bgColor = _optionColors[key]!.withOpacity(0.1);
      borderColor = _optionColors[key]!;
      textColor = _optionColors[key]!;
    } else if (_selectedOption == key && !_showFeedback) {
      bgColor = AppTheme.primaryLight;
      borderColor = AppTheme.primary;
      textColor = AppTheme.primary;
    }

    return GestureDetector(
      onTap: _showFeedback && _isCorrect ? null : () {
        setState(() {
          _selectedOption = key;
          _showFeedback = false; // Reset feedback if changing answer
          _optionColors.remove(key); // Clear error state if retrying this option
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        width: double.infinity,
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: borderColor, width: _selectedOption == key ? 2 : 1),
        ),
        child: Row(
          children: [
            Container(
              width: 32,
              height: 32,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: borderColor),
                color: _selectedOption == key ? borderColor : Colors.transparent,
              ),
              child: Text(
                key.toUpperCase(),
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: _selectedOption == key ? Colors.white : textColor,
                ),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                text,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: textColor,
                      fontWeight: _selectedOption == key ? FontWeight.w600 : FontWeight.normal,
                    ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Check if the topic is fully mastered
    final isMastered = _questions != null && _questions!.isEmpty;

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: Text('Practice: ${widget.title}'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _questions == null
              ? const Center(child: Text('Failed to load practice.'))
              : isMastered
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.workspace_premium, size: 80, color: AppTheme.warning),
                          const SizedBox(height: 24),
                          Text(
                            'Topic Mastered!',
                            style: Theme.of(context).textTheme.headlineMedium,
                          ),
                          const SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: () => Navigator.pop(context),
                            child: const Text('Return Home'),
                          ),
                        ],
                      ),
                    )
                  : SingleChildScrollView(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          // Question Card
                          Card(
                            child: Padding(
                              padding: const EdgeInsets.all(20.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Question ${_currentIndex + 1} of ${_questions!.length}',
                                    style: Theme.of(context).textTheme.labelLarge?.copyWith(
                                          color: AppTheme.textSecondary,
                                        ),
                                  ),
                                  const SizedBox(height: 12),
                                  Text(
                                    _questions![_currentIndex]['question_text'] ?? '',
                                    style: Theme.of(context).textTheme.titleLarge,
                                  ),
                                ],
                              ),
                            ),
                          ),
                          const SizedBox(height: 32),

                          // Options List
                          if (_questions![_currentIndex]['options'] != null)
                            ...(_questions![_currentIndex]['options'] as Map<String, dynamic>).entries.map(
                                  (e) => _buildOptionButton(e.key, e.value.toString()),
                                ),

                          const SizedBox(height: 24),

                          // Feedback Area
                          if (_showFeedback && _hint != null)
                            Container(
                              padding: const EdgeInsets.all(16),
                              margin: const EdgeInsets.only(bottom: 24),
                              decoration: BoxDecoration(
                                color: _isCorrect 
                                    ? AppTheme.success.withOpacity(0.1) 
                                    : AppTheme.error.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(16),
                                border: Border.all(
                                  color: _isCorrect ? AppTheme.success : AppTheme.error,
                                ),
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Icon(
                                    _isCorrect ? Icons.check_circle : Icons.error,
                                    color: _isCorrect ? AppTheme.success : AppTheme.error,
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Text(
                                      _hint!,
                                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                            color: _isCorrect ? AppTheme.success : AppTheme.error,
                                          ),
                                    ),
                                  ),
                                ],
                              ),
                            ),

                          // Action Button
                          if (_isCorrect)
                            ElevatedButton(
                              onPressed: _nextQuestion,
                              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.success),
                              child: const Text('Next Question'),
                            )
                          else
                            ElevatedButton(
                              onPressed: _selectedOption == null || _isSubmitting ? null : _submitAnswer,
                              child: _isSubmitting
                                  ? const SizedBox(
                                      height: 24,
                                      width: 24,
                                      child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                                    )
                                  : const Text('Submit Answer'),
                            ),
                        ],
                      ),
                    ),
    );
  }
}
