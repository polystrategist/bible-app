class Verse {
  final int bookNumber;
  final int chapter;
  final int verse;
  final String text;

  const Verse({
    required this.bookNumber,
    required this.chapter,
    required this.verse,
    required this.text,
  });

  factory Verse.fromMap(Map<String, dynamic> map) {
    return Verse(
      bookNumber: map['book_number'] as int,
      chapter: map['chapter'] as int,
      verse: map['verse'] as int,
      text: map['text'] as String? ?? '',
    );
  }
}
