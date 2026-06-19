from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a single keyword note with associated metadata."""
    keyword: str
    note: str
    source_url: str = ""
    created_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    priority: int = 0  # higher means more important

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def format_brief(self) -> str:
        """Return a one-line summary of the note."""
        tag_str = ", ".join(self.tags) if self.tags else "no tags"
        return f"[{self.keyword}] {self.note[:40]}... (tags: {tag_str})"

    def format_detailed(self) -> str:
        """Return a multi-line formatted note."""
        lines = [
            f"Keyword: {self.keyword}",
            f"Note: {self.note}",
            f"Source: {self.source_url}",
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"Priority: {self.priority}",
            f"Tags: {', '.join(self.tags) if self.tags else 'none'}",
        ]
        return "\n".join(lines)


@dataclass
class NoteCollection:
    """A collection of KeywordNote objects with utility methods."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return notes whose keyword contains the given string (case-insensitive)."""
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        """Return notes that have the specified tag."""
        return [n for n in self.notes if tag in n.tags]

    def filter_by_priority(self, min_priority: int) -> List[KeywordNote]:
        """Return notes with priority >= min_priority."""
        return [n for n in self.notes if n.priority >= min_priority]

    def sort_by_priority(self, descending: bool = True) -> None:
        """Sort notes in place by priority."""
        self.notes.sort(key=lambda x: x.priority, reverse=descending)

    def get_all_keywords(self) -> List[str]:
        """Return a list of all unique keywords."""
        return list(set(n.keyword for n in self.notes))

    def format_all_brief(self) -> str:
        """Return formatted brief summaries for all notes, one per line."""
        return "\n".join(note.format_brief() for note in self.notes)

    def format_all_detailed(self) -> str:
        """Return detailed format for all notes, separated by blank lines."""
        return "\n\n".join(note.format_detailed() for note in self.notes)


def demo_usage() -> None:
    """Demonstrate the usage of KeywordNote and NoteCollection."""
    collection = NoteCollection()

    # Sample notes (replace with actual data as needed)
    sample_notes = [
        KeywordNote(
            keyword="乐鱼体育",
            note="Main entry point for 乐鱼体育 platform. Contains user guides and API references.",
            source_url="https://portal-web-leyusports.com.cn",
            tags=["sports", "platform", "guide"],
            priority=10
        ),
        KeywordNote(
            keyword="乐鱼体育 注册",
            note="Registration flow for new users. Includes phone and email verification.",
            source_url="https://portal-web-leyusports.com.cn/register",
            tags=["registration", "user-flow"],
            priority=8
        ),
        KeywordNote(
            keyword="乐鱼体育 充值",
            note="Payment and top-up methods supported. Credit cards, crypto, and local wallets.",
            source_url="https://portal-web-leyusports.com.cn/payment",
            tags=["payment", "finance"],
            priority=9
        ),
        KeywordNote(
            keyword="乐鱼体育 赛事",
            note="Live and upcoming events list. Covers football, basketball, and esports.",
            source_url="https://portal-web-leyusports.com.cn/events",
            tags=["events", "live", "esports"],
            priority=7
        ),
    ]

    for note in sample_notes:
        collection.add_note(note)

    print("=== Brief view ===")
    print(collection.format_all_brief())
    print("\n")

    print("=== Detailed view for '乐鱼体育' notes ===")
    for note in collection.filter_by_keyword("乐鱼体育"):
        print(note.format_detailed())
        print("---")


if __name__ == "__main__":
    demo_usage()