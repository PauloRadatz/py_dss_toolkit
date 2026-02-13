# py_dss_toolkit Architecture Diagrams

This directory contains PlantUML diagrams documenting the architecture of py_dss_toolkit.

## 📁 Diagram Files

### 1. `ClassDiagram.puml` - Main Overview
**Purpose**: High-level architecture showing the overall system structure

**Shows**:
- Study hierarchy (StudyBase → StudySnapShotPowerFlow, StudyTimeSeriesPowerFlow)
- Model hierarchy (ModelBase and its mixins)
- Results hierarchy (SnapShotPowerFlowResults, TimeSeriesPowerFlowResults)
- View hierarchy (DSS, Static, Interactive views)
- Voltage Profile and Monitor components
- Circuit plotting (high-level reference)

**Best for**: Understanding the overall system architecture and how major components fit together

---

### 2. `CircuitModule.puml` - Circuit Module Details
**Purpose**: Detailed architecture of the interactive circuit plotting functionality

**Shows**:
- **Circuit Classes**: CircuitBase, Circuit, CircuitPlot, CircuitGeoPlot
- **Strategy Pattern**: 9 plot parameter strategies (ActivePower, Voltage, Distance, etc.)
- **Settings Classes**: 8 different settings types with inheritance
- **Composition Pattern**: How Circuit delegates to specialized plotting classes
- **Dependency Injection**: CircuitSettingsContainer for sharing configuration

**Design Patterns**:
- Strategy Pattern (PlotParameterStrategy and subclasses)
- Composition (Circuit contains CircuitPlot and CircuitGeoPlot)
- Dependency Injection (CircuitSettingsContainer)
- Template Method (CircuitBase provides shared logic)

**Best for**: Understanding circuit plotting implementation, extending with new plot parameters, modifying settings

---

### 3. `SettingsHierarchy.puml` - Settings Quick Reference
**Purpose**: Quick reference for all settings classes and their attributes

**Shows**:
- **Numerical Settings**: BaseSettingsNumerical and its subclasses
  - ActivePowerSettings
  - VoltageSettings
  - DistanceSettings
  - UserDefinedNumericalSettings
- **Categorical Settings**: Standalone classes with color maps
  - PhasesSettings
  - ThermalViolationSettings
  - VoltageViolationSettings
  - UserDefinedCategoricalSettings

**Best for**: Quickly checking available settings, understanding inheritance, configuring plot appearance

---

## 🚀 Viewing Diagrams

### Option 1: PlantUML Web Server
Visit [PlantUML Online](http://www.plantuml.com/plantuml/uml/) and paste the content

### Option 2: VS Code / Cursor Extension
1. Install "PlantUML" extension
2. Open any `.puml` file
3. Press `Alt+D` (or right-click → "Preview Current Diagram")

### Option 3: Local PlantUML
```bash
# Install PlantUML
brew install plantuml  # macOS
# or download from https://plantuml.com/download

# Generate PNG
plantuml ClassDiagram.puml

# Generate SVG (scalable, better for docs)
plantuml -tsvg CircuitModule.puml
```

---

## 📚 Diagram Reading Guide

### Relationship Symbols
- `<|--` : Inheritance (e.g., `CircuitBase <|-- Circuit` means Circuit inherits from CircuitBase)
- `*--` : Composition (strong ownership, e.g., `Circuit *-- CircuitPlot`)
- `o--` : Aggregation (weak ownership, e.g., `CircuitBase o-- PlotParameterStrategy`)
- `--` : Association (general relationship)

### Multiplicity
- `"1"` : Exactly one
- `"*"` : Zero or many
- `"1" *-- "1"` : One-to-one composition

### Visibility
- `+` : Public
- `-` : Private
- `#` : Protected

---

## 🔄 Keeping Diagrams Updated

When making significant architectural changes:

1. **Update the relevant diagram(s)**
   - Small changes → update specific diagram only
   - New major component → update main diagram + create detailed diagram if needed

2. **Verify consistency**
   - Class names match actual code
   - Relationships are accurate
   - Method signatures are current (keep high-level, not every parameter)

3. **Test rendering**
   - Ensure PlantUML can parse and render
   - Check that layout is readable

---

## 🎯 Architecture Highlights

### Circuit Module (Detailed in `CircuitModule.puml`)

**Key Features**:
- **9 Plot Parameters**: Active power, reactive power, voltage, distance, phases, thermal violations, voltage violations, user-defined numerical/categorical
- **2 Plot Types**: Regular (X/Y coordinates) and Geographic (lat/lon on maps)
- **Extensible Design**: Add new plot parameters by creating a new Strategy class
- **Shared Settings**: All settings managed through CircuitSettingsContainer
- **Performance Optimized**: 
  - Single-pass data preparation with O(1) bus lookups
  - Batch DataFrame creation (no concat in loops)
  - Shared helper methods for common operations

**Adding a New Plot Parameter**:
1. Create a Settings class (inherit from BaseSettingsNumerical if numerical)
2. Create a Strategy class (inherit from PlotParameterStrategy)
3. Add strategy to `_parameter_strategies` dict in CircuitBase
4. Add setting to CircuitSettingsContainer

---

## 📝 Notes

- Diagrams are maintained manually - they don't auto-generate from code
- Focus on architectural clarity over implementation details
- Include notes in diagrams to explain design decisions
- Keep method signatures high-level (main parameters only)

---

## 🤝 Contributing

When adding new features:
1. Update the relevant diagram(s) as part of your changes
2. Add explanatory notes if the design pattern isn't obvious
3. Consider if a new detailed diagram is needed for complex additions
