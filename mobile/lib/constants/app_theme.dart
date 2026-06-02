import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Python Learning System — Soft Minimalism
/// Extracted from Stitch Design System
class AppTheme {
  // -- Color Palette --
  static const Color primary = Color(0xFF005DA7);       // Soft Blue
  static const Color primaryLight = Color(0xFFD4E3FF);  // Primary fixed
  static const Color accent = Color(0xFF674BB5);        // Light Purple
  static const Color success = Color(0xFF006B2D);       // Tertiary / Success
  static const Color warning = Color(0xFFF59E0B);       // Amber
  static const Color error = Color(0xFFBA1A1A);         // Error Red
  
  static const Color background = Color(0xFFF9F9FF);    // Off-white
  static const Color surface = Color(0xFFFFFFFF);       // Cards
  static const Color textPrimary = Color(0xFF121C2A);   // On-Surface
  static const Color textSecondary = Color(0xFF414751); // On-Surface-Variant
  static const Color divider = Color(0xFFC1C7D3);       // Outline-Variant

  // -- Code block --
  static const Color codeBackground = Color(0xFFEFF3FF); // Soft Gray/Blue
  static const Color codeText = Color(0xFF121C2A);

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: const ColorScheme.light(
        primary: primary,
        secondary: accent,
        surface: surface,
        error: error,
        onPrimary: Colors.white,
        onSecondary: Colors.white,
        onSurface: textPrimary,
      ),
      scaffoldBackgroundColor: background,
      appBarTheme: AppBarTheme(
        backgroundColor: background, // Keeps it seamless with background
        foregroundColor: textPrimary,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.plusJakartaSans(
          color: textPrimary,
          fontSize: 20,
          fontWeight: FontWeight.w600,
          letterSpacing: -0.01,
        ),
      ),
      cardTheme: CardThemeData(
        color: surface,
        elevation: 0, // Level 1 Card: 1px border, soft shadow (added via BoxShadow in widgets)
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: divider, width: 1),
        ),
        margin: EdgeInsets.zero,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          minimumSize: const Size(double.infinity, 52),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          textStyle: GoogleFonts.lexend(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
          elevation: 2, // Skeuomorphic hint
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: primary,
          minimumSize: const Size(double.infinity, 52),
          side: const BorderSide(color: primary),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          textStyle: GoogleFonts.lexend(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surface,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: const BorderSide(color: divider),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: const BorderSide(color: divider),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: const BorderSide(color: primary, width: 1.5),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: const BorderSide(color: error),
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        hintStyle: GoogleFonts.lexend(color: textSecondary, fontSize: 16),
        labelStyle: GoogleFonts.lexend(color: textSecondary, fontSize: 14),
      ),
      textTheme: TextTheme(
        headlineLarge: GoogleFonts.plusJakartaSans(
          fontSize: 30,
          fontWeight: FontWeight.w700,
          color: textPrimary,
          height: 38 / 30,
          letterSpacing: -0.02,
        ),
        headlineMedium: GoogleFonts.plusJakartaSans(
          fontSize: 24,
          fontWeight: FontWeight.w700,
          color: textPrimary,
          height: 30 / 24,
          letterSpacing: -0.01,
        ),
        titleLarge: GoogleFonts.plusJakartaSans(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: textPrimary,
        ),
        titleMedium: GoogleFonts.lexend(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: textPrimary,
        ),
        bodyLarge: GoogleFonts.lexend(
          fontSize: 18,
          color: textPrimary,
          height: 28 / 18,
        ),
        bodyMedium: GoogleFonts.lexend(
          fontSize: 16,
          color: textSecondary,
          height: 24 / 16,
        ),
        labelLarge: GoogleFonts.lexend(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: primary,
          letterSpacing: 0.02,
        ),
      ),
      dividerTheme: const DividerThemeData(
        color: divider,
        thickness: 1,
      ),
      chipTheme: ChipThemeData(
        backgroundColor: primaryLight,
        labelStyle: GoogleFonts.lexend(color: primary, fontSize: 14),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        side: BorderSide.none,
      ),
    );
  }
}
