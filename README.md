# King & Slave Card Game

A strategic turn-based card game built with Pygame, where players choose between the King or Slave deck and battle against a computer opponent. The game features drag-and-drop card arrangement, animated battles, and a unique cyclical win condition.

---

## 🎮 Game Overview

In **King & Slave**, players select one of two asymmetric decks:

- **King Deck**: 1 King + 4 Soldiers
- **Slave Deck**: 1 Slave + 4 Soldiers

The computer receives the opposite deck. Each round, both sides reveal one card simultaneously. The game continues until a win condition is met or all cards are played.

---

## 🧠 Game Mechanics

### 🔹 Deck Construction

- Both player and computer decks contain 5 cards:
  - 1 main card (King or Slave)
  - 4 Soldiers
- Cards are arranged horizontally on screen.
- Computer deck is shuffled randomly.
- Player can drag and reorder cards before each round.

### 🔹 Card Arrangement

- During the **arrange phase**, players can:
  - Drag cards using the mouse
  - Reorder them freely
  - Press `Enter` to initiate battle

### 🔹 Battle Phase

- One card from each side is revealed per round.
- Animated flip effect displays both cards.
- Outcome is determined by the **cyclical win rule**.

### 🔹 Win Rule (Cyclical)

- If both cards are the same → Draw
- Otherwise:
  - King beats Soldier
  - Soldier beats Slave
  - Slave beats King

### 🔹 Victory Conditions

- First side to win a round is declared the winner.
- If all 5 rounds are played without a winner → Game ends in a **Draw**

### 🔹 Round Progression

- After each round:
  - Used cards are removed
  - Remaining cards are repositioned
  - Player re-enters **arrange phase** to reorder remaining cards
  - Game continues until a win or draw

---

## 🖱 Controls

| Action                  | Key / Mouse |
|-------------------------|-------------|
| Select King Deck        | `K`         |
| Select Slave Deck       | `S`         |
| Drag card               | Mouse click & move |
| Drop card               | Mouse release |
| Confirm arrangement     | `Enter`     |
| Quit game               | `Esc` or close window |

---

## 🔊 Audio Feedback

- Card flip sound on battle start
- Victory / Defeat / Draw sound effects
- Background music (optional)

---


# 🎮 King & Slave Game Demo

This is a prototype for a card-based battle game. Players can drag cards to reorder and initiate battles between characters from opposing factions.

---

## 🔄 Animated Demo

![Game Demo](assets/King&Slave_GameDemo.gif)

---

## 🖼️ Key Gameplay Screenshots

### 🏁 Faction Selection  
Players choose their allegiance before the battle begins.

![Faction Selection](assets/King&Slave_Screenshot_1.png)

---

### 🔢 Card Order Selection  
Players drag and reorder cards to determine battle sequence.

![Card Order Selection](assets/King&Slave_Screenshot_2.png)

---

### 👑 King Victory Scene  
The King wins the battle—celebration and outcome displayed.

![King Wins](assets/King&Slave_Screenshot_3.png)

---

### 🧎 Slave Victory Scene  
The Slave triumphs—alternate ending and visuals shown.

![Slave Wins](assets/King&Slave_Screenshot_4.png)

