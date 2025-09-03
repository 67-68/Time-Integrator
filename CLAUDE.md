# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Time Integrator (TI) is a "Personal Science Instrument" built with PyQt6 that helps users track and analyze their time usage patterns through a unique "Behavioral Chemistry" approach. It's designed as a personal learning environment architect rather than just another productivity tool.

## Development Commands

### Running the Application
```bash
python main.py
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_translator.py

# Run with verbose output
pytest -v
```

### Dependencies
Install dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

## Architecture Overview

The codebase follows a strict **Model-View-Presenter (MVP)** pattern with dependency injection:

### Core Architecture Layers

1. **View Layer (`ti/UI/views/`)**: PyQt6 widgets responsible only for display and capturing user input
2. **Presenter/Controller Layer (`ti/UI/presenters/`, `ti/controller/`)**: Pure Python objects handling business logic and coordinating between views and services
3. **Model/Services Layer (`ti/services/`, `ti/dataAccess/`, `ti/engine/`)**: Core business logic, data persistence, and analysis

### Dependency Injection Container
- **ServiceContainer** (`ti/services/serviceContainer.py`): Creates and manages all core service instances
- Key services include:
  - `DataService` (DS): ActionUnit CRUD operations
  - `InsightEngine` (IE): Analysis execution
  - `InsightManager` (IM): Insight management and curation
  - `InsightCacheService` (ICS): Persistent insight storage
  - `RealTimeMonitor` (RTM): Real-time behavior monitoring

### Key Data Models
- **ActionUnit**: Core data model representing time blocks with start/end times, action names, categories (waste/work/rest), and metadata
- Stored in JSON format in `Data/` directory

## Code Organization

### Main Application Entry
- `main.py`: Application entry point
- `ti/UI/App.py`: Main application class (`TimeIntegrator`)

### UI Structure
- `ti/UI/rawUI/`: Qt Designer .ui files and generated Python UI classes
- `ti/UI/views/`: High-level view components
- `ti/UI/widgets/`: Reusable widget components
- `ti/UI/presenters/`: Business logic controllers

### Core Features
- **CapturePage**: Time data input using custom shorthand syntax
- **AnalysisPage**: Pattern analysis through insight cards
  - `conditional_card`: Cards that appear based on pattern matching
  - `fixed_card`: Always-present analysis cards

### Extension System
- `ti/features/intervention/`: Pluggable intervention system
- `ti/core/extensionRegister.py`: Dynamic extension loading
- Pattern-based detection system in `ti/domain/detector/`

## Development Patterns

### Testing Approach
- Uses pytest with custom fixtures defined in `conftest.py`
- Tests follow Given-When-Then pattern
- Integration tests for core workflows
- Test files use descriptive Chinese comments for business context

### Data Flow
- Unidirectional data flow enforced through service orchestration
- Event bus system for decoupled communication
- Clear separation between UI events and business logic

### Fast Entry Syntax
The application uses a custom shorthand syntax for time entry, e.g.:
`1600-1730 <@ProjectA> @ActiveCreation #Coding - Implemented the core logic`

### File Naming Conventions
- UI files: `raw*.ui` for Qt Designer files, `ui_*.py` for generated classes
- Test files: `test_*.py`
- Presenter/Controller files: `*Presenter.py`, `*Service.py`

## Important Development Notes

- The codebase is primarily documented in Chinese with English technical terms
- Uses dependency injection pattern extensively - avoid direct service instantiation
- UI components should never contain business logic
- All analysis logic is configurable through "recipe" files rather than hard-coded
- The project follows a philosophy of "Behavioral Chemistry" over simple time tracking metrics

## Data Storage
- JSON-based storage in `Data/` directory
- `actionList.json`: Available action types
- `dateData.json`: Time tracking data by date
- `insightCache.json`: Generated insights cache