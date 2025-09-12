# Time Integrator (TI) - Your Personal Science Instrument

> TI is not another productivity app. It's a toolkit for becoming the architect of your own behavioral change. It's a serious attempt to build a **personal science instrument** for the mind.

This project is for you if you believe:
*   Understanding **why** you act is more important than tracking **what** you do.
*   Your life isn't a to-do list to be cleared, but a **system** to be understood and harmonized.
*   The ultimate goal isn't just "more productivity," but a sustainable, self-aware, and meaningful life **flow**.

---

## Core Philosophy: The "Why"

TI is built on a single, powerful premise: **traditional time trackers are great at physics, but terrible at chemistry.**

*   **Behavioral Physics (The Old Way):** They tell you the *quantity* of your actions ("You worked for 3.2 hours"). This is like describing a painting by listing the percentages of its colors. It's accurate, but shallow.
*   **Behavioral Chemistry (The TI Way):** We believe true understanding comes from identifying the *relationships* and *reactions* between your actions. TI is designed to be a **behavioral chemist's lab kit**, helping you discover the "molecular structures" of your habits and the "chemical reactions" that lead to burnout or flow.

Our mission is to help you move from being a passive observer of your time to an active **architect of your personal learning environment**.

## Key Features: The "What"

TI is an evolving ecosystem. Here's what the foundational version can do right now:

### 1. High-Fidelity Capture Engine
The quality of insight depends on the quality of data. Our capture system is designed for speed and depth.

*   **Fast-Entry Syntax:** A simple, powerful shorthand notation (`10001100w Code: Refactored the parser`) allows you to log your time fragments with minimal friction, keeping you in the flow.
*   **The Data Trinity:** Every action (`ActionUnit`) is enriched with three core dimensions to enable deep analysis:
    *   **Action Type:** A simple classification (`work`, `rest`, `waste`).
    *   **(Coming Soon)** **Context:** The "stage" on which you act (`@office`, `@home`).
    *   **(Coming Soon)** **Task Stream:** The cognitive "role" you are playing (`Active Creation`, `Skill Acquisition`).

### 2. The Insight Engine (Analysis Page)
This is where raw data is forged into wisdom. The Analysis Page presents a daily report of automatically generated "Insight Cards."

*   **Fixed Cards:** Get a clear, quantitative overview of your day, such as the time distribution across `work`, `rest`, and `waste`.
*   **Conditional Cards:** This is TI's secret weapon. Using a powerful, user-configurable **Recipe System**, TI automatically detects specific behavioral patterns in your data. A card is only generated if a meaningful pattern is found.
    *   **Example:** A card that only appears if it detects you engaged in a `waste` activity immediately after a `meal`, revealing a "post-meal procrastination" pattern.

### 3. The Intervention Engine (In Development)
Insight is useless without action. This is TI's most ambitious module, designed to bridge the "knowing-doing gap."

*   **Behavioral Contracts:** Respond to an Insight Card by signing a "contract" with your future self to attempt a change.
*   **Just-in-Time Interventions:** When the system detects the *preconditions* of a negative pattern (e.g., you've just finished a meal), it can trigger a real-time, modal prompt to help you honor your contract.
*   **Learning Loop:** Log the success or failure of each intervention, creating a rich dataset to understand which change strategies actually work for you.

---

## System Architecture: The "How"

TI is built with professional software engineering principles to ensure long-term maintainability and extensibility.

*   **Core Pattern:** A clean, decoupled **Model-View-Presenter (MVP)** architecture.
*   **Modularity:** A **Plugin-based architecture** where core functionalities (like `Capture` and `Intervention`) are treated as independent, self-contained modules.
*   **Communication:** An **Event Bus** facilitates asynchronous, low-coupling communication between different parts of the system.
*   **Configuration:** The entire system is **Recipe-Driven**. All complex logic—from insight detection to intervention workflows—is defined in human-readable `YAML` files, not hard-coded. This makes TI infinitely customizable.
*   **Dependencies:** We use a centralized **Dependency Injection Container (`ServiceContainer`)** to manage the lifecycle and dependencies of all core services, ensuring the system is highly testable and easy to reason about.

## The Road Ahead: The "Where To"

The current version is just the foundation. Our vision is to build a complete "Behavioral Science Lab":

*   **The Observation Deck:** Enhance the analysis with historical comparisons, pattern evolution tracking, and goal alignment metrics.
*   **The Experiment Panel:** Introduce a visual designer for creating new, complex intervention strategies and habit-formation workflows.
*   **The Open Platform:** Expose a clean API to allow integration with other tools and enable community-developed plugins.

---

## Getting Involved

This is an ambitious solo project driven by a deep passion for understanding the self. If this philosophy resonates with you, I welcome contributions of all kinds—from code and testing to ideas and philosophical debate.

**(Link to your GitHub / Contribution Guide would go here)**

The expedition has just begun.