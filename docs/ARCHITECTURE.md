# Architecture – Simple Explanation

This project is a **fair decision helper**.

It helps decide **who should work which shift**, using clear rules and fairness, instead of guesswork.

It does **not replace people**.
It helps people **make better and fairer decisions**.

---

## What this is 

Imagine a place where people must take turns doing jobs.

Some jobs are:
- during the day
- during the night
- on weekends

Some people:
- can do nights
- cannot do nights
- are tired because they worked a lot already

This program is like a **fair teacher**.

The teacher:
1. Looks at the jobs that need to be done  
2. Looks at the people who can do them  
3. Follows rules to keep things fair  
4. Explains *why* a job was given or not given  

If no one can do a job, the teacher explains **why**, instead of hiding it.

---

## What problem this solves

In real life, rota planning often depends on:
- memory
- spreadsheets
- pressure
- last-minute judgement

This can lead to:
- the same people getting hard shifts
- unfair complaints
- unclear decisions
- stress for managers

This project explores how those decisions can be:
- **fairer**
- **consistent**
- **explainable**
- **reviewable**

---

## What goes IN and what comes OUT

### What goes IN (inputs)

Right now, the program reads:

1) **Rules** (from `config.json`)
   - one shift per day
   - maximum night shifts in a row
   - who can or cannot do nights
   - how fairness is measured

2) **Example data** (inside the Python file)
   - list of staff
   - list of shifts
   - list of required cover

This is done on purpose so the logic can be tested first.

Later, the same logic could read from:
- spreadsheets
- databases
- HR systems
- a website or app

---

### What comes OUT (outputs)

When the program runs, it produces:

- a generated rota
- a list of unfilled shifts (with reasons)
- a fairness summary per person
- CSV files for review
- an Excel file combining all results

Nothing is hidden.
Everything can be inspected.

---

## Why there is no API or website yet

An API or website is just a **door**.

Before building the door, you must build a **reliable brain**.

This project focuses on the **brain first**:
- decision logic
- fairness rules
- constraint handling
- explanation of outcomes
- override warnings

Once the brain is stable, adding:
- an API
- a frontend
- a database

becomes straightforward.

---

## Main parts of the system (high level)

### 1) Configuration
The rules live in a config file.
This allows changes without rewriting code.

---

### 2) Decision Engine
The engine:
- checks which staff are eligible
- scores staff based on fairness
- applies rules and limits
- chooses the best available option

---

### 3) Constraints
Rules include:
- one shift per person per day
- maximum consecutive nights
- maximum consecutive long days
- cannot do nights (non-overridable)

Some rules can be overridden.
Some rules cannot.

---

### 4) Fairness Tracking
The system tracks:
- hours worked
- night shifts
- weekend shifts

This prevents the same people being overloaded.

---

### 5) Unfilled Shifts & Suggestions
If a shift cannot be filled:
- it is recorded as unfilled
- the reason is saved
- possible cover options are suggested
- blocked rules are explained

This makes decision-making transparent.

---

## How this is tested (without APIs)

Instead of calling web endpoints, the logic is tested directly.

We run:
- demo scenarios
- rule-focused checks
- repeatable test cases

This is like testing a calculator:
- you give numbers in
- you check the answer
- no website needed

---

## How this project is expected to grow

Planned progression:
1) Strengthen decision logic
2) Add more real-world scenarios
3) Improve override tracking and auditing
4) Add an API wrapper
5) Add a simple UI

The foundation must be solid before moving up.

---

## Summary

This project is not about flashy interfaces.

It is about:
- fairness
- clarity
- accountability
- explainable decisions

The goal is to help people understand **why** a rota looks the way it does.
