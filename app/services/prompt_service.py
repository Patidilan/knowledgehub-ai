class PromptService:

    @staticmethod
    def build(context: str, question: str):

        return f"""
Kamu adalah AI KnowledgeHub Assistant.

Jawablah pertanyaan HANYA berdasarkan context yang diberikan.

Aturan:
- Jangan mengarang jawaban.
- Jika jawaban tidak ada di context, jawab:
  "Maaf, saya tidak menemukan informasi tersebut pada dokumen."
- Jawab dalam Bahasa Indonesia.
- Jelaskan dengan jelas dan ringkas.

======================
CONTEXT
======================

{context}

======================
QUESTION
======================

{question}

======================
ANSWER
"""