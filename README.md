# AI-Powered HR Interview Simulator

## Overview

This repository contains a Streamlit-based web application designed to simulate behavioral HR interviews. It dynamically injects user-provided metadata (experience, skills, targeted company, and role seniority) into an OpenAI GPT-4o system prompt to conduct a structured 5-turn interactive simulation, concluding with automated performance grading and feedback generation.

## Technical Architecture and State Flow

### 1. Session State Initialization

To handle Streamlit's structural top-to-bottom rerun model execution upon user interaction, state persistence is enforced via `st.session_state` flags:

* `setup_completed`: Controls conditional rendering between the metadata collection form and the active chat interface.
* `user_message_count`: Monitored integer counter used to cap the active interaction at exactly 5 turns.
* `messages`: Appends sequential chat payloads following the OpenAI chat completions schema.
* `chat_completed`: Hard stop condition evaluated when `user_message_count >= 5`.
* `feedback_shown`: Handles lazy evaluation and rendering of the final evaluation pipeline.

### 2. Multi-Prompt Pipeline Execution

To optimize token consumption and prevent multi-task prompt dilution, the application decouples runtime components into two distinct contexts:

* **The Interactivity Context:** Injects form inputs directly into a persistent `system` role schema (`gpt-4o`). It executes token rendering asynchronously utilizing `st.write_stream` with parameter `stream=True`.
* **The Evaluation Context:** Triggers exclusively post-simulation. It abstracts the historical runtime conversation array, string-formats the history payload to eliminate structural overhead, and forwards it to an isolated endpoint evaluation model. It enforces structural integrity by constraining token production parameters to strict schema formatting requirements (`Overall Score:` and `Feedback:`).

### 3. Native Environment Purge

State clearing and application restarts bypass standard caching pitfalls by triggering a full client-side tab reload. This is achieved via custom JS evaluation execution inside the parent window layout tree through the `streamlit_js_eval` DOM bridge.

## Dependencies and Environment Variables

The codebase requires an authenticated connection handler pointing to an active OpenAI API platform project allocation.

### Local Secret Management

Store your API credentials in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = ""

```

### Installation

Ensure your deployment runtime contains the specified modules:

```bash
pip install streamlit openai streamlit-js-eval

```

## Running the Application

Execute the execution entry point from your root directory terminal:

```bash
streamlit run app.py

```