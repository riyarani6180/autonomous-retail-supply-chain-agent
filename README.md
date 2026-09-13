# Autonomous Retail Supply Chain Recovery Agent

An AI-powered autonomous agent that monitors retail supply-chain conditions, detects disruptions, evaluates recovery options, uses **Google Gemini** for intelligent decision-making, executes recovery actions, verifies the results, and automatically replans when a recovery action fails.

---

##  Problem Statement

Retail supply chains can face unexpected disruptions such as:

* Low inventory or stockouts
*  Shipment delays
*  Vendor failures
* Route closures

These disruptions can lead to delayed deliveries, product shortages, increased costs, and poor customer experience.

The goal of this project is to build an **autonomous supply-chain recovery agent** that can identify these problems and take appropriate recovery actions with minimal human intervention.

---

## Solution

The system follows a closed-loop autonomous recovery process:

```text
Monitor
   ↓
Detect Disruption
   ↓
Investigate
   ↓
Find Recovery Options
   ↓
Optimize Options
   ↓
Gemini AI Decision
   ↓
Validate Decision
   ↓
Execute Action
   ↓
Verify Recovery
   ↓
Replan if Required
```

Instead of only informing the user about a disruption, the system attempts to **recover the supply chain automatically**.

---

##  Key Features

###  1. Disruption Detection

The system monitors:

* Inventory levels
* Shipment delays
* Supply-chain status

It identifies problems such as:

```text
Gaming Laptop stock is low
Shipment S001 is delayed
```

---

###  2. Gemini AI Decision Making

Google Gemini acts as the reasoning layer of the system.

It receives:

* Current disruption
* Available recovery options
* Cost
* Delivery time
* Carbon emissions
* Availability

Gemini selects the most suitable recovery option.

Example:

```json
{
    "action": "PURCHASE",
    "vendor_id": "V001",
    "route_id": null,
    "reason": "Best balance of cost, delivery time and carbon emissions.",
    "confidence": 0.92
}
```

---

### 3. Recovery Option Optimization

Before Gemini makes the final decision, available options are ranked using an optimization score based on:

*  Cost
*  Delivery time
*  Carbon emissions

The system calculates:

```text
Score =
Cost × 0.5
+
Delivery Time × 0.3
+
Carbon Emissions × 0.2
```

A lower score represents a better option.

---

###  4. Decision Validation

The system does not blindly execute Gemini's response.

It verifies that:

* The selected vendor exists.
* The selected route exists.
* The selected option is available.
* The action is valid.

This prevents invalid AI decisions from being executed.

---

###  5. Autonomous Action Execution

The agent can execute recovery actions such as:

#### Purchase from an alternative vendor

```text
Vendor selected
       ↓
Purchase inventory
       ↓
Update inventory
       ↓
Update vendor stock
```

#### Reroute a delayed shipment

```text
Route selected
       ↓
Reroute shipment
       ↓
Remove shipment delay
       ↓
Update shipment status
```

---

### 6. Recovery Verification

After executing an action, the system checks whether the disruption has actually been resolved.

For example:

```text
Stock = 20
Reorder Point = 10

20 >= 10

 Inventory recovery verified
```

---

###  7. Automatic Replanning

If the selected recovery action fails, the agent does not simply stop.

It automatically:

```text
Action Failed
     ↓
Find New Options
     ↓
Remove Unavailable Option
     ↓
Ask Gemini Again
     ↓
Select New Plan
     ↓
Execute
     ↓
Verify
```

This provides adaptive recovery during changing supply-chain conditions.

---

###  8. Disruption Simulation

The project includes a simulation environment for testing different scenarios.

Available simulations include:

* Shipment Delay
*  Vendor Failure
*  Stockout
*  Route Closure

This makes it possible to demonstrate the autonomous agent without requiring a real supply-chain system.

---

##  Project Architecture

```text
                    🚚 SUPPLY CHAIN
                           │
                           ▼
                ┌─────────────────────┐
                │ Disruption Detector │
                └──────────┬──────────┘
                           │
                           ▼
                     Investigation
                           │
                           ▼
                ┌─────────────────────┐
                │ Recovery Planner    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Optimizer        │
                │ Cost + Time + CO₂   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Gemini AI        │
                │ Decision Agent      │
                └──────────┬──────────┘
                           │
                           ▼
                      Validation
                           │
                           ▼
                ┌─────────────────────┐
                │   Action Executor   │
                └──────────┬──────────┘
                           │
                           ▼
                      Verification
                           │
                    ┌──────┴──────┐
                    │             │
                 SUCCESS        FAILED
                    │             │
                    ▼             ▼
               Recovered       Replan
```

---

##  Project Structure

```text
autonomous-supply-chain-agent/
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
├── agent/
│   ├── decision_agent.py
│   ├── disruption_detector.py
│   ├── recovery_planner.py
│   └── verifier.py
│
├── tools/
│   ├── inventory.py
│   ├── shipment.py
│   ├── vendors.py
│   ├── routes.py
│   ├── optimizer.py
│   └── actions.py
│
├── data/
│   ├── inventory.json
│   ├── shipments.json
│   ├── vendors.json
│   └── routes.json
│
└── simulation/
    ├── environment.py
    └── disruptions.py
```

---

##  Technology Stack

| Technology                   | Purpose                          |
| ---------------------------- | -------------------------------- |
|  Python                    | Core application logic           |
|  Streamlit                 | Interactive dashboard            |
|  Google Gemini API         | AI reasoning and decision-making |
| JSON                      | Supply-chain simulation data     |
|  Python Optimization Logic | Recovery option ranking          |
|  python-dotenv             | Secure API key management        |


# 🧪 How to Test

## Scenario 1: Inventory Stockout

1. Open the Streamlit dashboard.
2. Click ** Simulate Stockout**.
3. The Gaming Laptop inventory becomes unavailable.
4. The disruption detector identifies the problem.
5. Click ** Run Recovery Agent**.
6. The system finds available vendors.
7. The optimizer ranks the vendors.
8. Gemini selects a recovery option.
9. Validate the AI decision.
10. Click **Execute Purchase**.
11. Inventory is updated.
12. The verifier checks the new inventory.
13. The system reports successful recovery.

---

## Scenario 2: Shipment Delay

1. Click ** Simulate Shipment Delay**.
2. Shipment `S001` is delayed.
3. The disruption detector identifies the delay.
4. Click **🚀 Run Recovery Agent**.
5. The system finds available routes.
6. Routes are ranked according to cost, delivery time and carbon emissions.
7. Gemini selects a suitable route.
8. The decision is validated.
9. Click **🚚 Execute Reroute**.
10. Shipment status is updated.
11. The verifier confirms recovery.

---

##  Replanning Demo

The project can also demonstrate adaptive replanning.

The flow is:

```text
Gemini selects Option A
          ↓
Option A becomes unavailable
          ↓
Execution fails
          ↓
Agent detects failure
          ↓
New recovery options generated
          ↓
Gemini makes a new decision
          ↓
New action executed
          ↓
Recovery verified
```

This demonstrates that the system can adapt to changing conditions instead of following a fixed plan.

---

#  Example Recovery Decision

Suppose Gaming Laptop inventory is low.

Available vendors:

```text
TechSource
Price: ₹52,000
Delivery: 3 days
Carbon: 18

ElectroMart
Price: ₹54,000
Delivery: 2 days
Carbon: 12

QuickTech
Price: ₹56,000
Delivery: 1 day
Carbon: 25
```

The optimizer calculates scores for all feasible options.

Gemini then receives the disruption and ranked options and selects the most suitable recovery action.

Example result:

```json
{
    "action": "PURCHASE",
    "vendor_id": "V001",
    "reason": "Best overall balance of cost, delivery time and carbon emissions.",
    "confidence": 0.92
}
```

The selected vendor is then validated and the purchase can be executed.

---

#  Safety and Reliability

The project includes several safeguards around AI decision-making:

### 1. Constrained Decisions

Gemini is instructed to select only from the provided options.

### 2. Decision Validation

The application validates the returned vendor or route before execution.

### 3. Availability Checks

Unavailable vendors and routes are removed from the recovery options.

### 4. Execution Verification

Every recovery action is verified after execution.

### 5. Automatic Replanning

If an action fails, the agent searches for another feasible solution.

---

#  Why This Project Matters

Retail supply chains are dynamic systems where disruptions can occur unexpectedly.

A traditional system may:

```text
Detect problem
      ↓
Notify human
      ↓
Wait for decision
      ↓
Take action
```

Our system aims to:

```text
Detect
  ↓
Reason
  ↓
Decide
  ↓
Act
  ↓
Verify
  ↓
Adapt
```

This reduces the need for manual intervention and demonstrates how **AI agents can be used for real-world operational decision-making**.

---

#  Future Improvements

The current project uses simulated JSON data. It can be extended with:

*  Real-time inventory APIs
*  Real vendor APIs
*  Real-time shipment tracking
* Live route and traffic data
*  Demand forecasting
*  Dynamic pricing
* Advanced carbon optimization
* Database integration
*  Role-based access
*  Advanced analytics dashboard
*  Cloud deployment
*  Multi-agent supply-chain architecture


The key idea is:

> **Don't just predict the disruption — detect it, decide how to recover, take action, verify the result, and adapt when conditions change.**

---

##  Project Workflow

```text
 Monitor Supply Chain
        ↓
 Detect Disruption
        ↓
 Generate Recovery Options
        ↓
 Optimize Options
        ↓
Gemini Decision
        ↓
Validate Decision
        ↓
Execute Recovery
        ↓
Verify Result
        ↓
Replan if Required
```

**Autonomous Retail Supply Chain Recovery Agent — turning supply-chain disruptions into automated recovery decisions.**
