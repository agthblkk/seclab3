import tkinter as tk
from tkinter import messagebox
import random

class PoemCipher:
    def __init__(self, poem):
        self.poem = poem
        self.grid = self.create_grid()

    def create_grid(self):
        lines = self.poem.split("\n")
        grid = []
        for line in lines:
            row = [char for char in line[:10]]  # Максимум 10 символів у рядку
            while len(row) < 10:
                row.append(" ")  # Додати пробіли, якщо рядок коротший за 10
            grid.append(row)
        return grid

    def encrypt(self, message):
        encrypted_message = []
        for char in message:
            # Находим все позиции символа в таблице
            positions = [(r, c) for r, row in enumerate(self.grid) for c, cell in enumerate(row) if cell == char]
            if not positions:
                # Если символ отсутствует, добавляем '??'
                encrypted_message.append("??")
            else:
                # Если символ найден, выбираем случайную позицию
                row, col = random.choice(positions)
                encrypted_message.append(f"{row + 1}/{col + 1}")
        return ", ".join(encrypted_message)

    def decrypt(self, encrypted_message):
        decrypted_message = ""
        codes = encrypted_message.split(", ")
        for code in codes:
            if code == "??":
                decrypted_message += "?"  # Символ, который отсутствовал
            else:
                try:
                    row, col = map(int, code.split("/"))
                    decrypted_message += self.grid[row - 1][col - 1]
                except (ValueError, IndexError):
                    decrypted_message += "?"
        return decrypted_message


class CipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Poem Cipher")

        self.language = tk.StringVar(value="uk")
        self.translations = {
            "uk": {
                "enter_poem": "Введіть вірш (ключ):",
                "enter_message": "Введіть повідомлення для шифрування:",
                "encrypt": "Зашифрувати",
                "cipher_text": "Шифрограма:",
                "decrypt": "Розшифрувати",
                "decrypted_message": "Розшифроване повідомлення:",
                "error": "Помилка",
                "enter_poem_error": "Будь ласка, введіть вірш.",
                "enter_message_error": "Будь ласка, введіть повідомлення.",
                "enter_cipher_error": "Будь ласка, введіть шифрограму."
            },
            "en": {
                "enter_poem": "Enter the poem (key):",
                "enter_message": "Enter the message to encrypt:",
                "encrypt": "Encrypt",
                "cipher_text": "Ciphertext:",
                "decrypt": "Decrypt",
                "decrypted_message": "Decrypted Message:",
                "error": "Error",
                "enter_poem_error": "Please enter a poem.",
                "enter_message_error": "Please enter a message.",
                "enter_cipher_error": "Please enter the ciphertext."
            }
        }

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text=self.translations[self.language.get()]["enter_poem"]).pack()
        self.poem_text = tk.Text(self.root, height=10, width=40)
        self.poem_text.pack()

        tk.Label(self.root, text=self.translations[self.language.get()]["enter_message"]).pack()
        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack()

        self.encrypt_button = tk.Button(self.root, text=self.translations[self.language.get()]["encrypt"], command=self.encrypt_message)
        self.encrypt_button.pack()

        tk.Label(self.root, text=self.translations[self.language.get()]["cipher_text"]).pack()
        self.encrypted_message = tk.Entry(self.root, width=50)
        self.encrypted_message.pack()

        self.decrypt_button = tk.Button(self.root, text=self.translations[self.language.get()]["decrypt"], command=self.decrypt_message)
        self.decrypt_button.pack()

        tk.Label(self.root, text=self.translations[self.language.get()]["decrypted_message"]).pack()
        self.decrypted_message = tk.Entry(self.root, width=50)
        self.decrypted_message.pack()

        tk.OptionMenu(self.root, self.language, "uk", "en", command=self.update_language).pack()

    def update_language(self, *args):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()

    def encrypt_message(self):
        poem = self.poem_text.get("1.0", tk.END).strip()
        if not poem:
            messagebox.showerror(self.translations[self.language.get()]["error"], self.translations[self.language.get()]["enter_poem_error"])
            return

        message = self.message_entry.get()
        if not message:
            messagebox.showerror(self.translations[self.language.get()]["error"], self.translations[self.language.get()]["enter_message_error"])
            return

        cipher = PoemCipher(poem)
        encrypted = cipher.encrypt(message)
        self.encrypted_message.delete(0, tk.END)
        self.encrypted_message.insert(0, encrypted)

    def decrypt_message(self):
        poem = self.poem_text.get("1.0", tk.END).strip()
        if not poem:
            messagebox.showerror(self.translations[self.language.get()]["error"], self.translations[self.language.get()]["enter_poem_error"])
            return

        encrypted_message = self.encrypted_message.get()
        if not encrypted_message:
            messagebox.showerror(self.translations[self.language.get()]["error"], self.translations[self.language.get()]["enter_cipher_error"])
            return

        cipher = PoemCipher(poem)
        decrypted = cipher.decrypt(encrypted_message)
        self.decrypted_message.delete(0, tk.END)
        self.decrypted_message.insert(0, decrypted)


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherGUI(root)
    root.mainloop()
