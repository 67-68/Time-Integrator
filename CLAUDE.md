# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Time Integrator (TI) is a PyQt6-based desktop application for personal behavioral analysis and time tracking. It follows a plugin-based architecture with Model-View-Presenter (MVP) pattern and dependency injection.

## Development Commands

### Running the Application
```bash
python main.py
```

### Testing
```bash
python test_register.py
```

## Architecture Overview

### Core Components
- **Main Entry**: `main.py` → `TimeIntegrator` class in `ti/core/App.py`
- **Service Container**: Centralized dependency injection in `ti/services/serviceContainer.py`
- **Event Bus**: Asynchronous communication via `ti/core/eventBus.py`
- **Plugin System**: Dynamic extension loading via `ti/core/extensionRegister.py`

### Key Services
- `DataService`: Core data management
- `EventBus`: Inter-component communication
- `PageFactory`: UI page creation
- `SymbolService`: Path and symbol registration
- `FunctionService`: Plugin function contributions

### Plugin Architecture
Plugins implement `ExtensionInterface` and are loaded by `DynamicExtensionLoader`. Core plugins include:
- `CapturePlugin`: Time entry and data capture
- `InsightPlugin`: Behavioral analysis and insights
- `InterventionPlugin`: Behavior change interventions
- `DetectorPlugin`: Pattern detection
- `MenuPlugin`: Navigation and UI controls

### Data Flow
1. User input → Capture plugin → DataService
2. DataService → Insight engine → Insight cards
3. Insight cards → Intervention system → Real-time monitoring

### File Organization
- `ti/core/`: Core infrastructure and interfaces
- `ti/services/`: Shared services and utilities
- `ti/features/`: Feature-specific implementations (plugins)
- `ti/model/`: Data models and domain objects
- `ti/view/`: UI components and Qt widgets
- `ti/presenters/`: Presentation logic and coordination



