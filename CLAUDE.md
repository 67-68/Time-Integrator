# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Time Integrator (TI) is a PyQt6-based personal science instrument and cognitive co-pilot application focused on behavioral chemistry analysis rather than traditional productivity tracking.

## Key Architecture

- **MVP Pattern**: Model-View-Presenter architecture with strict separation of concerns
- **Service Container**: Dependency injection container manages all core services
- **Core Services**: DataService, CardGenerationService, InsightEngine, InsightManager, InsightCacheService
- **Data Model**: ActionUnit JSON objects with start/end times, categories, and metadata

## Development Commands

### Testing
- Run all tests: `python3 -m pytest`
- Run specific test file: `python3 -m pytest tests/test_file.py`
- Run with verbose output: `python3 -m pytest -v`

### Application Execution
- Start main application: `python3 main.py`

### Code Quality
- Check imports and basic syntax: `python3 -m py_compile main.py`

## Directory Structure

- `ti/core/` - Core application logic and coordination
- `ti/features/` - Feature-specific implementations (capture, intervention)
- `ti/model/` - Data models and repositories
- `ti/presenters/` - MVP presenters for different features
- `ti/services/` - Business logic and data services
- `ti/view/` - PyQt6 UI components
- `tests/` - Test suite

## Key Files

- `main.py` - Application entry point
- `ti/core/App.py` - Main TimeIntegrator class
- `ti/core/mainCoordinator.py` - Application coordinator
- `ti/services/serviceContainer.py` - Dependency injection container
- `ti/features/capture/` - Time capture functionality
- `ti/features/intervention/` - Analysis and intervention features

## Data Storage
- JSON-based storage in `ti/model/data/`
- Action units stored with UUIDs and timestamps
- Categories: waste, work, rest with importance/urgency metadata

## Testing Philosophy
- Blueprint-driven testing with UML as reference
- Integration tests for service interactions
- Unit tests for individual components
- Test paths configured in `pytest.ini`

## Development Notes
- Uses PyQt6 for UI
- JSON-based data persistence
- Service-oriented architecture
- Focus on behavioral pattern analysis rather than time tracking