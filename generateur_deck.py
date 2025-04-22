import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from tkinter.font import Font
import json
import os
from pathlib import Path
from PIL import Image, ImageTk

class DeckGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur de Deck")
        self.root.geometry("650x900")
        self.root.configure(bg="#2E3440")

        # Initialiser les variables avant load_data()
        self.master_rank_var = tk.StringVar(value="1")
        self.current_rank = None

        # Charger les données sauvegardées
        self.load_data()

        # Configuration des rangs et couleurs
        self.ranks = {
            "Débutant 1": {"points": 0, "color": "#D8DEE9"},
            "Débutant 2": {"points": 20, "color": "#D8DEE9"},
            "Débutant 3": {"points": 50, "color": "#D8DEE9"},
            "Débutant 4": {"points": 95, "color": "#D8DEE9"},
            "Poké Ball 1": {"points": 145, "color": "#BF616A"},
            "Poké Ball 2": {"points": 195, "color": "#BF616A"},
            "Poké Ball 3": {"points": 245, "color": "#BF616A"},
            "Poké Ball 4": {"points": 300, "color": "#BF616A"},
            "Super Ball 1": {"points": 355, "color": "#5E81AC"},
            "Super Ball 2": {"points": 420, "color": "#5E81AC"},
            "Super Ball 3": {"points": 490, "color": "#5E81AC"},
            "Super Ball 4": {"points": 600, "color": "#5E81AC"},
            "Hyper Ball 1": {"points": 710, "color": "#D08770"},
            "Hyper Ball 2": {"points": 860, "color": "#D08770"},
            "Hyper Ball 3": {"points": 1010, "color": "#D08770"},
            "Hyper Ball 4": {"points": 1225, "color": "#D08770"},
            "Master Ball": {"points": 1450, "color": "#B48EAD"}
        }

        # Charger les images
        self.load_ball_images()

        # Polices
        self.title_font = Font(family="Helvetica", size=20, weight="bold")
        self.deck_font = Font(family="Helvetica", size=16, weight="bold")
        self.button_font = Font(family="Helvetica", size=12)
        self.feedback_font = Font(family="Helvetica", size=12, weight="bold")
        self.small_font = Font(family="Helvetica", size=11)
        self.rank_font = Font(family="Helvetica", size=13, weight="bold")

        # Variables
        self.current_deck = tk.StringVar()
        self.score_var = tk.StringVar(value=str(self.score))
        self.battles_var = tk.StringVar(value=f"{self.battles} combats ({self.wins}V/{self.losses}D)")
        self.feedback_var = tk.StringVar()
        self.current_points_var = tk.StringVar(value=str(self.current_points))
        self.remaining_points_var = tk.StringVar(value=str(self.remaining_points))
        self.remaining_var = tk.StringVar()
        self.current_rank_var = tk.StringVar(value="Rang actuel : Non défini")

        # Cadre principal
        self.main_frame = tk.Frame(root, bg="#2E3440", padx=20, pady=15)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Titre avec bouton gestion
        title_frame = tk.Frame(self.main_frame, bg="#3B4252")
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            title_frame, 
            text="GÉNÉRATEUR DE DECK", 
            font=self.title_font, 
            fg="#ECEFF4", 
            bg="#3B4252",
            padx=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True)
        
        # Bouton Gérer les Decks (icône molette)
        tk.Button(
            title_frame,
            text="⚙",
            font=Font(size=14),
            bg="#4C566A",
            fg="#ECEFF4",
            bd=0,
            relief=tk.FLAT,
            command=self.manage_decks
        ).pack(side=tk.RIGHT, padx=5)

        # Bouton Générer
        tk.Button(
            self.main_frame,
            text="GÉNÉRER UN DECK",
            font=self.button_font,
            bg="#5E81AC",
            fg="#ECEFF4",
            activebackground="#81A1C1",
            relief=tk.FLAT,
            command=self.generate_deck,
            padx=15,
            pady=10
        ).pack(fill=tk.X, pady=5)

        # Affichage du deck
        deck_frame = tk.Frame(self.main_frame, bg="#434C5E")
        deck_frame.pack(fill=tk.X, pady=10)
        self.deck_label = tk.Label(
            deck_frame,
            textvariable=self.current_deck,
            font=self.deck_font,
            fg="#88C0D0",
            bg="#434C5E",
            padx=15,
            pady=15,
            wraplength=400
        )
        self.deck_label.pack(fill=tk.X)

        # Bouton Continuer
        self.continue_button = tk.Button(
            self.main_frame,
            text="CONTINUER",
            font=self.button_font,
            bg="#4C566A",
            fg="#ECEFF4",
            state=tk.DISABLED,
            relief=tk.FLAT,
            command=self.show_result_buttons,
            padx=15,
            pady=8
        )
        self.continue_button.pack(fill=tk.X, pady=5)

        # Feedback
        self.feedback_label = tk.Label(
            self.main_frame,
            textvariable=self.feedback_var,
            font=self.feedback_font,
            bg="#2E3440",
            pady=8
        )
        self.feedback_label.pack()

        # Boutons Résultat
        self.result_frame = tk.Frame(self.main_frame, bg="#2E3440")
        self.win_button = tk.Button(
            self.result_frame,
            text="GAGNÉ +10",
            font=self.button_font,
            bg="#A3BE8C",
            fg="#2E3440",
            relief=tk.FLAT,
            command=self.win,
            padx=10
        )
        self.win_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
        self.lose_button = tk.Button(
            self.result_frame,
            text="PERDU -7",
            font=self.button_font,
            bg="#BF616A",
            fg="#ECEFF4",
            relief=tk.FLAT,
            command=self.lose,
            padx=10
        )
        self.lose_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        # Stats
        stats_frame = tk.Frame(self.main_frame, bg="#2E3440")
        stats_frame.pack(pady=10)
        
        tk.Label(
            stats_frame,
            text="Score:",
            font=self.small_font,
            fg="#D8DEE9",
            bg="#2E3440"
        ).grid(row=0, column=0, sticky="w")
        
        tk.Label(
            stats_frame,
            textvariable=self.score_var,
            font=self.small_font,
            fg="#ECEFF4",
            bg="#2E3440"
        ).grid(row=0, column=1, padx=10, sticky="w")
        
        tk.Label(
            stats_frame,
            textvariable=self.battles_var,
            font=self.small_font,
            fg="#D8DEE9",
            bg="#2E3440"
        ).grid(row=0, column=2, sticky="e")

        # Bouton Reset Stats
        tk.Button(
            stats_frame,
            text="Reset Stats",
            font=self.small_font,
            bg="#D08770",
            fg="#2E3440",
            relief=tk.FLAT,
            command=self.reset_stats,
            padx=5
        ).grid(row=0, column=3, padx=(10, 0))

        # Nouveau cadre pour le rang avec image
        self.rank_frame = tk.Frame(self.main_frame, bg="#3B4252")
        self.rank_frame.pack(fill=tk.X, pady=5)
        
        # Image du rang
        self.rank_image_label = tk.Label(self.rank_frame, bg="#3B4252")
        self.rank_image_label.pack(side=tk.LEFT, padx=10)
        
        # Texte du rang
        self.rank_text = tk.Label(
            self.rank_frame,
            textvariable=self.current_rank_var,
            font=self.rank_font,
            bg="#3B4252",
            fg="#D8DEE9"
        )
        self.rank_text.pack(side=tk.LEFT)
        
        # Bouton pour sélectionner le rang
        self.select_rank_btn = tk.Button(
            self.rank_frame,
            image=self.rank_icon,
            bg="#4C566A",
            relief=tk.FLAT,
            command=self.select_rank
        )
        self.select_rank_btn.pack(side=tk.RIGHT, padx=10)
        
        # Classement Master Ball (caché par défaut)
        self.master_rank_frame = tk.Frame(self.main_frame, bg="#3B4252")
        
        tk.Label(
            self.master_rank_frame,
            text="Classement:",
            font=self.small_font,
            bg="#3B4252",
            fg="#D8DEE9"
        ).pack(side=tk.LEFT, padx=(10,5))
        
        tk.Entry(
            self.master_rank_frame,
            textvariable=self.master_rank_var,
            font=self.small_font,
            width=5,
            bg="#4C566A",
            fg="#ECEFF4",
            relief=tk.FLAT
        ).pack(side=tk.LEFT)

        # Points et Reset
        points_frame = tk.Frame(self.main_frame, bg="#2E3440")
        points_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            points_frame,
            text="Points actuels:",
            font=self.small_font,
            fg="#D8DEE9",
            bg="#2E3440"
        ).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        tk.Entry(
            points_frame,
            textvariable=self.current_points_var,
            font=self.small_font,
            width=10,
            bg="#4C566A",
            fg="#ECEFF4",
            relief=tk.FLAT
        ).grid(row=0, column=1, padx=5)
        
        tk.Label(
            points_frame,
            text="Objectif:",
            font=self.small_font,
            fg="#D8DEE9",
            bg="#2E3440"
        ).grid(row=0, column=2, sticky="w", padx=(10, 5))
        
        tk.Entry(
            points_frame,
            textvariable=self.remaining_points_var,
            font=self.small_font,
            width=10,
            bg="#4C566A",
            fg="#ECEFF4",
            relief=tk.FLAT
        ).grid(row=0, column=3, padx=5)
        
        # Bouton Reset sur la même ligne
        tk.Button(
            points_frame,
            text="Reset Points",
            font=self.small_font,
            bg="#BF616A",
            fg="#ECEFF4",
            relief=tk.FLAT,
            command=self.reset_points,
            padx=10
        ).grid(row=0, column=4, padx=(10, 0))

        # Info palier
        self.rank_info_frame = tk.Frame(self.main_frame, bg="#3B4252", padx=15, pady=10)
        self.rank_info_frame.pack(fill=tk.X, pady=10)
        
        self.rank_info_label = tk.Label(
            self.rank_info_frame,
            textvariable=self.remaining_var,
            font=self.small_font,
            fg="#ECEFF4",
            bg="#3B4252",
            justify=tk.LEFT,
            wraplength=450
        )
        self.rank_info_label.pack(anchor="w")

        # Bouton Mettre à jour
        tk.Button(
            self.main_frame,
            text="METTRE À JOUR LES PALIERS",
            font=self.small_font,
            bg="#5E81AC",
            fg="#ECEFF4",
            relief=tk.FLAT,
            command=self.update_rank_info,
            pady=5
        ).pack(fill=tk.X)

        # Initialisation
        self.update_rank_info()
        self.update_rank_display()
        
        # Lier les événements
        self.current_points_var.trace_add("write", lambda *_: self.save_data())
        self.remaining_points_var.trace_add("write", lambda *_: self.save_data())
        self.master_rank_var.trace_add("write", lambda *_: self.save_data())

    def load_image(self, path):
        """Charge une image avec gestion des erreurs"""
        try:
            return ImageTk.PhotoImage(Image.open(path).resize((40,40)))
        except Exception as e:
            print(f"Erreur chargement image {path}: {e}")
            # Retourne une image vide si l'image n'est pas trouvée
            return ImageTk.PhotoImage(Image.new('RGBA', (40, 40), (0, 0, 0, 0)))

    def load_ball_images(self):
        """Charge toutes les images nécessaires"""
        try:
            # Essayer plusieurs chemins possibles pour les images
            img_paths = [
                os.path.join(os.path.dirname(__file__), "img/"),
                "img/",
                "C:\\Users\\damie\\Desktop\\combat pokemon\\img\\"
            ]
            
            img_path = None
            for path in img_paths:
                if os.path.exists(path):
                    img_path = path
                    break
            
            if img_path is None:
                raise FileNotFoundError("Dossier img introuvable")
            
            self.ball_images = {
                "Débutant": self.load_image(img_path + "ball.png"),
                "Poké Ball": self.load_image(img_path + "pokeball.png"),
                "Super Ball": self.load_image(img_path + "superball.png"),
                "Hyper Ball": self.load_image(img_path + "hyperball.png"),
                "Master Ball": self.load_image(img_path + "masterball.png")
            }
            self.rank_icon = self.load_image(img_path + "rang.png")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les images: {e}")
            self.root.destroy()

    def load_data(self):
        """Charge les données sauvegardées"""
        self.save_path = Path.home() / "AppData" / "Local" / "PokemonDeckGenerator"
        self.save_file = self.save_path / "save.json"
        
        # Valeurs par défaut
        self.decks = [
            "Gallame/Lucario",
            "Tortank",
            "Giratina/Mewtwo",
            "Miascarade",
            "Terraiste/Tag-Tag",
            "Dracaufeu/Sulfura",
            "Magnezone/Airmure"
        ]
        self.score = 0
        self.wins = 0
        self.losses = 0
        self.battles = 0
        self.current_points = 0
        self.remaining_points = 0
        self.master_rank = 1

        try:
            self.save_path.mkdir(exist_ok=True)
            if self.save_file.exists():
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.decks = data.get("decks", self.decks)
                    self.score = data.get("score", 0)
                    self.wins = data.get("wins", 0)
                    self.losses = data.get("losses", 0)
                    self.battles = data.get("battles", 0)
                    self.current_points = data.get("current_points", 0)
                    self.remaining_points = data.get("remaining_points", 0)
                    self.current_rank = data.get("current_rank")
                    self.master_rank = data.get("master_rank", 1)
                    self.master_rank_var.set(str(self.master_rank))
        except Exception as e:
            print(f"Erreur chargement données: {e}")

    def save_data(self):
        """Sauvegarde toutes les données"""
        try:
            data = {
                "decks": self.decks,
                "score": self.score,
                "wins": self.wins,
                "losses": self.losses,
                "battles": self.battles,
                "current_points": int(self.current_points_var.get() or 0),
                "remaining_points": int(self.remaining_points_var.get() or 0),
                "current_rank": self.current_rank,
                "master_rank": int(self.master_rank_var.get() or 1)
            }
            with open(self.save_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Erreur sauvegarde: {e}")

    def reset_stats(self):
        """Réinitialise les statistiques de combat"""
        self.wins = 0
        self.losses = 0
        self.battles = 0
        self.score = 0
        self.update_stats()
        self.feedback_var.set("Stats et score réinitialisés")
        self.feedback_label.config(fg="#D8DEE9")
        self.save_data()

    def reset_points(self):
        """Réinitialise les points et le rang"""
        self.current_points_var.set("0")
        self.remaining_points_var.set("0")
        self.current_rank = None
        self.master_rank_var.set("1")  # Reset aussi le classement MB
        self.rank_image_label.config(image=self.rank_icon)
        self.current_rank_var.set("Rang actuel : Non défini")
        self.master_rank_frame.pack_forget()
        self.update_rank_info()
        self.save_data()

    def generate_deck(self):
        if not self.decks:
            messagebox.showwarning("Aucun deck", "Ajoutez d'abord des decks dans la gestion des decks")
            return
            
        deck = random.choice(self.decks)
        self.current_deck.set(deck)
        self.continue_button.config(state=tk.NORMAL, bg="#5E81AC")
        self.feedback_var.set("")
    
    def show_result_buttons(self):
        self.continue_button.config(state=tk.DISABLED, bg="#4C566A")
        self.result_frame.pack(fill=tk.X, pady=5)
    
    def win(self):
        self.score += 10
        self.wins += 1
        self.battles += 1
        
        current = int(self.current_points_var.get() or 0)
        self.current_points_var.set(str(current + 10))
        
        self.update_stats()
        self.feedback_var.set("Bien joué ! +10 points !")
        self.feedback_label.config(fg="#A3BE8C")
        self.result_frame.pack_forget()
        self.update_rank_info()
        self.save_data()
    
    def lose(self):
        self.score -= 7
        self.losses += 1
        self.battles += 1
        
        current = int(self.current_points_var.get() or 0)
        self.current_points_var.set(str(current - 7))
        
        self.update_stats()
        self.feedback_var.set("Dommage... -7 points")
        self.feedback_label.config(fg="#BF616A")
        self.result_frame.pack_forget()
        self.update_rank_info()
        self.save_data()
    
    def update_stats(self):
        self.score_var.set(str(self.score))
        self.battles_var.set(f"{self.battles} combats ({self.wins}V/{self.losses}D)")
    
    def select_rank(self):
        """Fenêtre de sélection du rang"""
        self.rank_selection_window = tk.Toplevel(self.root)  # Stocker la référence
        self.rank_selection_window.title("Sélectionner votre rang")
        self.rank_selection_window.geometry("400x300")
        self.rank_selection_window.configure(bg="#3B4252")
        self.rank_selection_window.resizable(False, False)
        
        tk.Label(
            self.rank_selection_window,
            text="CHOISISSEZ VOTRE RANG",
            font=self.title_font,
            fg="#ECEFF4",
            bg="#3B4252",
            pady=10
        ).pack()
        
        # Frame pour les boutons de rang
        balls_frame = tk.Frame(self.rank_selection_window, bg="#3B4252")
        balls_frame.pack(pady=20)
        
        # Boutons pour chaque type de balle
        for i, (rank_name, img) in enumerate(self.ball_images.items()):
            btn = tk.Button(
                balls_frame,
                image=img,
                text=rank_name,
                compound=tk.TOP,
                font=self.small_font,
                bg="#4C566A",
                fg="#ECEFF4",
                relief=tk.FLAT,
                command=lambda r=rank_name: self.set_rank(r)
            )
            btn.grid(row=i//3, column=i%3, padx=10, pady=5)
            
    def set_rank(self, rank_name):
        """Définit le rang sélectionné"""
        if rank_name == "Master Ball":
            position = simpledialog.askinteger("Classement", "Quelle est votre position en Master Ball ?", 
                                            parent=self.root, minvalue=1, maxvalue=999)
            if position:
                self.current_rank = "Master Ball"
                self.master_rank_var.set(str(position))
                self.current_points_var.set("1450")
                if hasattr(self, 'rank_selection_window'):
                    self.rank_selection_window.destroy()
                self.update_rank_display()
                self.update_rank_info()
        else:
            # Nouvelle interface pour sélectionner le niveau
            level_window = tk.Toplevel(self.root)
            level_window.title(f"Niveau {rank_name}")
            level_window.geometry("200x150")
            level_window.configure(bg="#3B4252")
            
            # Fermer la fenêtre de sélection de rang
            if hasattr(self, 'rank_selection_window'):
                self.rank_selection_window.destroy()
            
            tk.Label(
                level_window,
                text=f"Sélectionnez le niveau:",
                font=self.small_font,
                bg="#3B4252",
                fg="#ECEFF4"
            ).pack(pady=(10,5))
            
            # Frame pour la grille de boutons
            grid_frame = tk.Frame(level_window, bg="#3B4252")
            grid_frame.pack()
            
            # Configuration des boutons
            btn_config = {
                'font': self.button_font,
                'bg': "#5E81AC",
                'fg': "#ECEFF4",
                'width': 5,
                'relief': tk.FLAT
            }
            
            # Ligne 1
            tk.Button(grid_frame, text="1", **btn_config,
                    command=lambda: self.set_rank_level(rank_name, 1, level_window))\
                .grid(row=0, column=0, padx=5, pady=5)
                
            tk.Button(grid_frame, text="2", **btn_config,
                    command=lambda: self.set_rank_level(rank_name, 2, level_window))\
                .grid(row=0, column=1, padx=5, pady=5)
            
            # Ligne 2
            tk.Button(grid_frame, text="3", **btn_config,
                    command=lambda: self.set_rank_level(rank_name, 3, level_window))\
                .grid(row=1, column=0, padx=5, pady=5)
                
            tk.Button(grid_frame, text="4", **btn_config,
                    command=lambda: self.set_rank_level(rank_name, 4, level_window))\
                .grid(row=1, column=1, padx=5, pady=5)

    def set_rank_level(self, rank_name, level, window):
        """Définit le niveau du rang"""
        rank_full = f"{rank_name} {level}"
        self.current_rank = rank_full
        
        # Trouver les points correspondants à ce rang
        for rank, data in self.ranks.items():
            if rank == rank_full:
                self.current_points_var.set(str(data["points"]))
                break
        
        window.destroy()
        self.update_rank_display()
        self.update_rank_info()
                
    def update_rank_display(self):
        """Met à jour l'affichage du rang"""
        if not self.current_rank:
            self.rank_image_label.config(image=self.rank_icon)
            self.current_rank_var.set("Rang actuel : Non défini")
            self.master_rank_frame.pack_forget()
            return
        
        # Modification ici pour mieux gérer les noms de rangs
        rank_base = self.current_rank.split()[0]  # "Poké Ball 2" -> "Poké Ball"
        
        # Correspondance entre les noms dans l'image et les noms des rangs
        image_keys = {
            "Débutant": "Débutant",
            "Poké": "Poké Ball",
            "Super": "Super Ball",
            "Hyper": "Hyper Ball",
            "Master": "Master Ball"
        }
        
        # Trouver la bonne image
        for key in image_keys:
            if key in rank_base:
                self.rank_image_label.config(image=self.ball_images[image_keys[key]])
                break
        else:
            self.rank_image_label.config(image=self.rank_icon)
        
        self.current_rank_var.set(f"Rang actuel : {self.current_rank}")
        
        if "Master Ball" in self.current_rank:
            self.master_rank_frame.pack(fill=tk.X, pady=5)
        else:
            self.master_rank_frame.pack_forget()
            
        self.save_data()
    
    def update_rank_info(self, *args):
        try:
            current = int(self.current_points_var.get() or 0)
            remaining = int(self.remaining_points_var.get() or 0)
            target = current + remaining
            
            current_rank = "Débutant 1"
            next_rank = None
            next_points = None
            
            for rank, data in self.ranks.items():
                if current >= data["points"]:
                    current_rank = rank
                elif next_rank is None:
                    next_rank = rank
                    next_points = data["points"]
            
            # Mise à jour automatique si le rang a changé via les points
            if not self.current_rank or current_rank != self.current_rank:
                self.current_rank = current_rank
                self.update_rank_display()
            
            if target >= 1450:
                self.remaining_var.set("🎉 OBJECTIF MASTER BALL ATTEINT ! 🎉")
            elif next_rank:
                needed = max(0, next_points - current)
                denominator = next_points - self.ranks[current_rank]["points"]
                if denominator > 0:
                    progress = min(100, int((current - self.ranks[current_rank]["points"]) / denominator * 100))
                    progress_text = f"Progression jusqu'au prochain rang : {progress}%\n"
                else:
                    progress_text = ""
                
                self.remaining_var.set(
                    f"Prochain palier : {next_rank} ({next_points} pts)\n"
                    f"{progress_text}"
                    f"Points nécessaires : {needed}\n"
                    f"Objectif total : {target} pts"
                )
            else:
                self.remaining_var.set("Vous avez atteint le rang maximum !")
                
        except ValueError:
            self.remaining_var.set("Entrez des nombres valides")
    
    def manage_decks(self):
        """Ouvre la fenêtre de gestion des decks"""
        deck_window = tk.Toplevel(self.root)
        deck_window.title("Gestion des Decks")
        deck_window.geometry("450x400")
        deck_window.configure(bg="#2E3440")
        
        main_frame = tk.Frame(deck_window, bg="#2E3440", padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(
            main_frame,
            text="GESTION DES DECKS",
            font=self.button_font,
            fg="#ECEFF4",
            bg="#2E3440",
            pady=10
        ).pack(fill=tk.X)

        list_frame = tk.Frame(main_frame, bg="#3B4252")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.deck_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg="#4C566A",
            fg="#ECEFF4",
            selectbackground="#5E81AC",
            font=self.small_font,
            height=10
        )
        self.deck_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.deck_listbox.yview)
        
        for deck in self.decks:
            self.deck_listbox.insert(tk.END, deck)
        
        controls_frame = tk.Frame(main_frame, bg="#2E3440")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.new_deck_var = tk.StringVar()
        tk.Entry(
            controls_frame,
            textvariable=self.new_deck_var,
            font=self.small_font,
            bg="#4C566A",
            fg="#ECEFF4",
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=(0, 10))

        btn_frame = tk.Frame(controls_frame, bg="#2E3440")
        btn_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_frame,
            text="Ajouter",
            font=self.small_font,
            bg="#A3BE8C",
            fg="#2E3440",
            relief=tk.FLAT,
            command=self.add_deck
        ).pack(side=tk.LEFT, expand=True, padx=2)
        
        tk.Button(
            btn_frame,
            text="Supprimer",
            font=self.small_font,
            bg="#BF616A",
            fg="#ECEFF4",
            relief=tk.FLAT,
            command=self.remove_deck
        ).pack(side=tk.LEFT, expand=True, padx=2)
        
        tk.Button(
            btn_frame,
            text="Tout supprimer",
            font=self.small_font,
            bg="#D08770",
            fg="#2E3440",
            relief=tk.FLAT,
            command=self.clear_all_decks
        ).pack(side=tk.LEFT, expand=True, padx=2)
    
    def add_deck(self):
        new_deck = self.new_deck_var.get().strip()
        if new_deck:
            if new_deck not in self.decks:
                self.decks.append(new_deck)
                self.deck_listbox.insert(tk.END, new_deck)
                self.new_deck_var.set("")
                self.save_data()
            else:
                messagebox.showwarning("Doublon", "Ce deck existe déjà dans la liste")
    
    def remove_deck(self):
        selection = self.deck_listbox.curselection()
        if selection:
            index = selection[0]
            self.deck_listbox.delete(index)
            self.decks.pop(index)
            self.save_data()
    
    def clear_all_decks(self):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer tous les decks ?"):
            self.deck_listbox.delete(0, tk.END)
            self.decks.clear()
            self.save_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckGeneratorApp(root)
    root.mainloop()