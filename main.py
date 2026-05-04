import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# Путь к файлу истории в папке рядом с main.py
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

# Предопределённый список цитат
quotes = [
    {
        "text": "Жизнь как вождение велосипеда – чтобы сохранить равновесие, ты должен двигаться.",
        "author": "Альберт Эйнштейн",
        "topic": "Жизнь"
    },
    {
        "text": "Счастье не в счастье, а только в его достижении.",
        "author": "Фёдор Достоевский",
        "topic": "Счастье"
    },
    {
        "text": "Делай, что можешь, с тем, что у тебя есть, там, где ты есть.",
        "author": "Теодор Рузвельт",
        "topic": "Мотивация"
    }
    # Можно добавить больше цитат
]

# Загрузка истории из файла
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# Сохранение истории в файл
def save_history(history):
    with open(HISTORY_FILE, "w", encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.history = load_history()

        # Поля фильтрации
        self.author_var = tk.StringVar()
        self.topic_var = tk.StringVar()

        # UI компоненты для фильтров
        tk.Label(root, text="Фильтр по автору:").grid(row=0, column=0, sticky='w')
        tk.Entry(root, textvariable=self.author_var, width=20).grid(row=0, column=1, padx=5)
        tk.Label(root, text="Фильтр по теме:").grid(row=0, column=2, sticky='w')
        tk.Entry(root, textvariable=self.topic_var, width=20).grid(row=0, column=3, padx=5)
        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5)

        # Цитата
        self.quote_label = tk.Label(root, text="Нажмите 'Сгенерировать цитату'", wraplength=400, justify="left", font=('Arial', 12))
        self.quote_label.grid(row=1, column=0, columnspan=5, pady=10)

        # Кнопки
        tk.Button(root, text="Сгенерировать цитату", command=self.generate_quote).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Добавить новую цитату", command=self.add_quote).grid(row=2, column=2, columnspan=2, pady=5)

        # История
        tk.Label(root, text="История:").grid(row=3, column=0, columnspan=5, sticky='w')
        self.history_listbox = tk.Listbox(root, width=80, height=10)
        self.history_listbox.grid(row=4, column=0, columnspan=5, padx=5, pady=5)
        self.update_history_listbox()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def apply_filter(self):
        # применяется фильтр, ничего не меняет, только обновляет
        self.update_history_listbox()

    def generate_quote(self):
        author_filter = self.author_var.get().strip().lower()
        topic_filter = self.topic_var.get().strip().lower()

        filtered = [
            q for q in quotes
            if (not author_filter or author_filter in q['author'].lower()) and
               (not topic_filter or topic_filter in q['topic'].lower())
        ]

        if not filtered:
            messagebox.showinfo("Цитата", "Нет цитат по данным фильтрам.")
            return

        quote = random.choice(filtered)
        display_text = f'"{quote["text"]}"\n— {quote["author"]} [{quote["topic"]}]'
        self.quote_label["text"] = display_text
        self.history.append(quote)
        self.update_history_listbox()

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for q in self.history:
            text = f'"{q["text"]}" — {q["author"]} [{q["topic"]}]'
            self.history_listbox.insert(tk.END, text)

    def add_quote(self):
        text = simpledialog.askstring("Добавить цитату", "Текст цитаты:")
        if not text or not text.strip():
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        author = simpledialog.askstring("Добавить цитату", "Автор:")
        if not author or not author.strip():
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        topic = simpledialog.askstring("Добавить цитату", "Тема:")
        if not topic or not topic.strip():
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return
        quote = {"text": text.strip(), "author": author.strip(), "topic": topic.strip()}
        quotes.append(quote)
        messagebox.showinfo("Успех", "Цитата добавлена!")

    def on_closing(self):
        save_history(self.history)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
