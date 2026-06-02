"""
reset_and_reseed.py
====================
Clears the lessons and practice_questions tables, then re-seeds all
9 lessons with the updated hierarchical content from seed_batch1.py
and seed_batch2.py.

WARNING: This will DELETE all existing lesson content.
         User accounts and progress records are preserved.

Usage (from backend/ folder):
    .\\venv\\Scripts\\python reset_and_reseed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import Lesson, PracticeQuestion

# Import the seed functions
from seed_batch1 import seed_lessons_batch1
from seed_batch2 import seed_batch2

app = create_app()


def reset_lesson_tables():
    """Delete all rows from practice_questions then lessons (order matters for FK)."""
    with app.app_context():
        q_count = PracticeQuestion.query.count()
        l_count  = Lesson.query.count()

        PracticeQuestion.query.delete()
        db.session.commit()
        print(f"[OK] Cleared {q_count} practice questions.")

        Lesson.query.delete()
        db.session.commit()
        print(f"[OK] Cleared {l_count} lessons.")


if __name__ == "__main__":
    print("=" * 60)
    print("  RESETTING AND RESEEDING LESSON DATABASE")
    print("  (User accounts and progress records are kept)")
    print("=" * 60)

    # Step 1 — Clear existing lesson data
    reset_lesson_tables()

    # Step 2 — Re-seed Amateur tier (L01, L02, L03)
    print("\n[1/2] Seeding Amateur tier (L01-L03)...")
    seed_lessons_batch1()

    # Step 3 — Re-seed Intermediate & Pro tiers (L04-L09)
    print("\n[2/2] Seeding Intermediate & Pro tiers (L04-L09)...")
    seed_batch2()

    print("\n" + "=" * 60)
    print("  ALL DONE! 9 lessons and 45 questions seeded.")
    print("  Restart the Flask server to serve the new content.")
    print("=" * 60)
