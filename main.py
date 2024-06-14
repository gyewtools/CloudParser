import os
import shutil
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class TelegramExtractorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Telegram, Discord, Steam, and Passwords Extractor")
        self.geometry("600x500")

        self.path_entry = ctk.CTkEntry(self, width=300)
        self.path_entry.grid(row=0, column=0, padx=20, pady=20)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_path)
        self.browse_button.grid(row=0, column=1, padx=10, pady=20)

        self.start_telegram_button = ctk.CTkButton(self, text="Start Telegram Search", command=lambda: self.start_search('telegram'))
        self.start_telegram_button.grid(row=2, column=0, padx=10, pady=10)

        self.start_discord_button = ctk.CTkButton(self, text="Start Discord Search", command=lambda: self.start_search('discord'))
        self.start_discord_button.grid(row=2, column=1, padx=10, pady=10)

        self.start_steam_button = ctk.CTkButton(self, text="Start Steam Search", command=lambda: self.start_search('steam'))
        self.start_steam_button.grid(row=2, column=2, padx=10, pady=10)

        self.start_password_button = ctk.CTkButton(self, text="Start Passwords Search", command=lambda: self.start_search('passwords'))
        self.start_password_button.grid(row=2, column=3, padx=10, pady=10)

        self.result_label = ctk.CTkLabel(self, text="Located Folders:")
        self.result_label.grid(row=3, column=0, padx=20, pady=20, sticky="w")

        self.result_textbox = ctk.CTkTextbox(self, width=500, height=200)
        self.result_textbox.grid(row=4, column=0, columnspan=4, padx=20, pady=10)
        self.result_textbox.configure(state='disabled')

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def start_search(self, search_type):
        base_path = self.path_entry.get()
        if not base_path:
            messagebox.showerror("Error", "Please enter a path")
            return

        self.result_textbox.configure(state='normal')
        self.result_textbox.delete(1.0, tk.END)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.setup_directories(script_dir)

        for root, dirs, files in os.walk(base_path):
            self.update_results(f"Searching in: {root}\n")
            if root == base_path:
                self.process_directory(root, dirs, files, search_type)
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    if os.path.isdir(dir_path):
                        subdirs = os.listdir(dir_path)
                        subfiles = [f for f in subdirs if os.path.isfile(os.path.join(dir_path, f))]
                        self.process_directory(dir_path, subdirs, subfiles, search_type)
                break

        self.result_textbox.configure(state='disabled')

    def setup_directories(self, script_dir):
        paths = ["teles", "discord", "steam", "passwords"]
        for path in paths:
            full_path = os.path.join(script_dir, path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)

    def update_results(self, result):
        self.result_textbox.insert(tk.END, result)
        self.result_textbox.yview(tk.END)
        self.update_idletasks()

    def process_directory(self, root, dirs, files, search_type):
        if search_type == 'telegram':
            result = self.search_telegram(root, dirs)
        elif search_type == 'discord':
            result = self.search_discord(root, dirs)
        elif search_type == 'steam':
            result = self.search_steam(root, dirs)
        elif search_type == 'passwords':
            result = self.search_passwords(root, files)

        if result:
            self.update_results(result)

    def search_telegram(self, root, dirs):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        tele_path = os.path.join(script_dir, "teles")
        tele_counter = len(os.listdir(tele_path)) + 1

        if "Telegram" in dirs:
            tdata_path = os.path.join(root, "Telegram", "tdata")
            if os.path.exists(tdata_path):
                try:
                    new_folder_name = f"tele_{tele_counter}"
                    new_path = os.path.join(tele_path, new_folder_name)
                    shutil.copytree(tdata_path, new_path)
                    return f"Located tdata: {new_path}\n"
                except Exception as e:
                    return f"Error copying Telegram data: {e}\n"
        return None

    def search_discord(self, root, dirs):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        discord_path = os.path.join(script_dir, "discord")
        token_list = []

        if "Discord" in dirs:
            discord_root = os.path.join(root, "Discord")
            for dirpath, dirnames, filenames in os.walk(discord_root):
                for filename in filenames:
                    if filename.endswith(".txt"):
                        txt_path = os.path.join(dirpath, filename)
                        try:
                            with open(txt_path, 'r') as file:
                                token_list.append(file.read())
                        except Exception as e:
                            return f"Error reading Discord token file: {e}\n"

        if token_list:
            tokens_file_path = os.path.join(discord_path, "tokens.txt")
            try:
                with open(tokens_file_path, 'a') as tokens_file:
                    for token in token_list:
                        tokens_file.write(token + "\n")
                return f"Collected tokens saved to: {tokens_file_path}\n"
            except Exception as e:
                return f"Error saving Discord tokens: {e}\n"
        return None

    def search_steam(self, root, dirs):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        steam_path = os.path.join(script_dir, "steam")
        token_list = []

        if "Steam" in dirs:
            steam_root = os.path.join(root, "Steam")
            for dirpath, dirnames, filenames in os.walk(steam_root):
                for filename in filenames:
                    if filename.endswith(".txt"):
                        txt_path = os.path.join(dirpath, filename)
                        try:
                            with open(txt_path, 'r') as file:
                                token_list.append(file.read())
                        except Exception as e:
                            return f"Error reading Steam token file: {e}\n"

        if token_list:
            tokens_file_path = os.path.join(steam_path, "tokens.txt")
            try:
                with open(tokens_file_path, 'a') as tokens_file:
                    for token in token_list:
                        tokens_file.write(token + "\n")
                return f"Collected Steam tokens saved to: {tokens_file_path}\n"
            except Exception as e:
                return f"Error saving Steam tokens: {e}\n"
        return None

    def search_passwords(self, root, files):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        passwords_path = os.path.join(script_dir, "passwords")
        passwords_list = []

        for filename in files:
            if filename == "passwords.txt":
                txt_path = os.path.join(root, filename)
                try:
                    with open(txt_path, 'r') as file:
                        passwords_list.append(file.read())
                except Exception as e:
                    return f"Error reading passwords file: {e}\n"

        if passwords_list:
            passwords_file_path = os.path.join(passwords_path, "passwords.txt")
            try:
                with open(passwords_file_path, 'a') as passwords_file:
                    for passwords in passwords_list:
                        passwords_file.write(passwords + "\n")
                return f"Collected passwords saved to: {passwords_file_path}\n"
            except Exception as e:
                return f"Error saving passwords: {e}\n"
        return None

if __name__ == "__main__":
    app = TelegramExtractorApp()
    app.mainloop()
