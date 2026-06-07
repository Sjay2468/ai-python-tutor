import 'package:flutter/material.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/dracula.dart';
import '../services/api_service.dart';

/// A lightweight in-app Python IDE widget.
/// Shows an editable code area pre-populated with [initialCode],
/// a Run button that executes the code via the backend sandbox,
/// and a terminal-style output panel.
class CodeEditorWidget extends StatefulWidget {
  final String initialCode;

  const CodeEditorWidget({super.key, required this.initialCode});

  @override
  State<CodeEditorWidget> createState() => _CodeEditorWidgetState();
}

class _CodeEditorWidgetState extends State<CodeEditorWidget> {
  final ApiService _api = ApiService();
  late TextEditingController _controller;
  bool _isRunning = false;
  String? _stdout;
  String? _stderr;
  bool _hasRun = false;
  bool _isEditing = false;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.initialCode);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _runCode() async {
    setState(() {
      _isRunning = true;
      _hasRun = false;
    });

    final result = await _api.runCode(_controller.text);

    if (mounted) {
      setState(() {
        _isRunning = false;
        _hasRun = true;
        _stdout = result?['stdout'] as String? ?? '';
        _stderr = result?['stderr'] as String? ?? '';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // ── Header bar ──────────────────────────────────────────────
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: BoxDecoration(
            color: const Color(0xFF282A36), // Dracula header
            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
          ),
          child: Row(
            children: [
              const Icon(Icons.code, color: Colors.white70, size: 18),
              const SizedBox(width: 8),
              const Text(
                'Python Playground',
                style: TextStyle(
                  color: Colors.white70,
                  fontFamily: 'monospace',
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const Spacer(),
              // Edit / Preview toggle
              GestureDetector(
                onTap: () => setState(() => _isEditing = !_isEditing),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.white12,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    _isEditing ? 'Preview' : 'Edit',
                    style: const TextStyle(
                      color: Colors.white70,
                      fontSize: 12,
                      fontFamily: 'monospace',
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              // Run button
              GestureDetector(
                onTap: _isRunning ? null : _runCode,
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                  decoration: BoxDecoration(
                    color: _isRunning
                        ? Colors.white24
                        : const Color(0xFF50FA7B), // Dracula green
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: _isRunning
                      ? const SizedBox(
                          width: 14,
                          height: 14,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.play_arrow_rounded,
                                color: Color(0xFF282A36), size: 16),
                            SizedBox(width: 4),
                            Text(
                              'Run',
                              style: TextStyle(
                                color: Color(0xFF282A36),
                                fontWeight: FontWeight.w700,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                ),
              ),
            ],
          ),
        ),

        // ── Code area ────────────────────────────────────────────────
        Container(
          constraints: const BoxConstraints(minHeight: 160, maxHeight: 300),
          decoration: const BoxDecoration(
            color: Color(0xFF282A36),
          ),
          child: _isEditing
              ? Scrollbar(
                  child: TextField(
                    controller: _controller,
                    maxLines: null,
                    expands: true,
                    style: const TextStyle(
                      fontFamily: 'monospace',
                      fontSize: 13.5,
                      color: Color(0xFFF8F8F2), // Dracula foreground
                      height: 1.6,
                    ),
                    decoration: const InputDecoration(
                      border: InputBorder.none,
                      contentPadding: EdgeInsets.all(16),
                      fillColor: Color(0xFF282A36),
                      filled: true,
                    ),
                    cursorColor: const Color(0xFFFF79C6),
                  ),
                )
              : SingleChildScrollView(
                  child: HighlightView(
                    _controller.text,
                    language: 'python',
                    theme: draculaTheme,
                    padding: const EdgeInsets.all(16),
                    textStyle: const TextStyle(
                      fontFamily: 'monospace',
                      fontSize: 13.5,
                      height: 1.6,
                    ),
                  ),
                ),
        ),

        // ── Output panel ─────────────────────────────────────────────
        AnimatedCrossFade(
          duration: const Duration(milliseconds: 300),
          crossFadeState:
              _hasRun ? CrossFadeState.showFirst : CrossFadeState.showSecond,
          firstChild: Container(
            constraints: const BoxConstraints(maxHeight: 200),
            decoration: BoxDecoration(
              color: const Color(0xFF1E1E2E), // Slightly darker
              borderRadius:
                  const BorderRadius.vertical(bottom: Radius.circular(16)),
              border: Border.all(color: const Color(0xFF44475A)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              mainAxisSize: MainAxisSize.min,
              children: [
                // Output header
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: const BoxDecoration(
                    color: Color(0xFF44475A),
                  ),
                  child: Row(
                    children: [
                      Icon(
                        (_stderr?.isNotEmpty == true)
                            ? Icons.error_outline
                            : Icons.check_circle_outline,
                        color: (_stderr?.isNotEmpty == true)
                            ? const Color(0xFFFF5555) // Dracula red
                            : const Color(0xFF50FA7B), // Dracula green
                        size: 16,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        (_stderr?.isNotEmpty == true) ? 'Output (with errors)' : 'Output',
                        style: const TextStyle(
                          color: Colors.white70,
                          fontFamily: 'monospace',
                          fontSize: 12,
                        ),
                      ),
                      const Spacer(),
                      GestureDetector(
                        onTap: () => setState(() => _hasRun = false),
                        child: const Icon(Icons.close,
                            color: Colors.white38, size: 16),
                      ),
                    ],
                  ),
                ),
                Flexible(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        if (_stdout?.isNotEmpty == true)
                          SelectableText(
                            _stdout!,
                            style: const TextStyle(
                              fontFamily: 'monospace',
                              fontSize: 13,
                              color: Color(0xFFF8F8F2),
                              height: 1.6,
                            ),
                          ),
                        if (_stderr?.isNotEmpty == true)
                          SelectableText(
                            _stderr!,
                            style: const TextStyle(
                              fontFamily: 'monospace',
                              fontSize: 13,
                              color: Color(0xFFFF5555),
                              height: 1.6,
                            ),
                          ),
                        if (_stdout?.isEmpty == true && _stderr?.isEmpty == true)
                          const Text(
                            '(no output)',
                            style: TextStyle(
                              fontFamily: 'monospace',
                              fontSize: 13,
                              color: Colors.white38,
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          secondChild: Container(
            decoration: const BoxDecoration(
              color: Color(0xFF1E1E2E),
              borderRadius: BorderRadius.vertical(bottom: Radius.circular(16)),
              border: Border(
                left: BorderSide(color: Color(0xFF44475A)),
                right: BorderSide(color: Color(0xFF44475A)),
                bottom: BorderSide(color: Color(0xFF44475A)),
              ),
            ),
            padding: const EdgeInsets.all(16),
            child: const Text(
              '▶  Press Run to execute your code',
              style: TextStyle(
                fontFamily: 'monospace',
                fontSize: 13,
                color: Colors.white38,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
