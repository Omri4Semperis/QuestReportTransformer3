# Git Commit Guidelines
## Purpose
These guidelines are designed to create a clear, readable, and consistent Git history. Following this format helps everyone on the team, including AI assistants, understand the purpose of each change.

## Commit Message Structure
Every commit message should follow the Conventional Commits specification. It consists of a header, an optional body, and an optional footer, structured as follows:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### 1\. Header (Mandatory)
The header is the most important part of the commit message.

  * **`<type>`**: Describes the kind of change being made.
  * **`<scope>`** (Optional): Specifies the part of the codebase affected (e.g., api, ui, auth, docs).
  * **`<subject>`**: A short summary of the change.
      * Keep it under 50 characters.
      * Use the imperative present tense (e.g., "add feature," not "added feature").
      * Do not capitalize the first letter.
      * Do not end with a period.

#### Common Types:
  * **feat**: A new feature for the user.
  * **fix**: A bug fix for the user.
  * **docs**: Changes to documentation only.
  * **style**: Formatting or code style changes that do not affect logic (e.g., whitespace).
  * **refactor**: A code change that neither fixes a bug nor adds a feature.
  * **perf**: A code change that improves performance.
  * **test**: Adding new tests or correcting existing ones.
  * **chore**: Routine tasks, maintenance, or dependency updates.
  * **build**: Changes affecting the build system or external dependencies.
  * **ci**: Changes to CI/CD configuration files and scripts.

### 2\. Body (Optional)
  * Use the body to explain the "what" and "why" of your change, not the "how".
  * Separate the body from the header with a blank line.
  * Wrap all lines at 72 characters for readability.
  * You can also list side effects, performance notes, or other key details.

### 3\. Footer (Optional)
  * **Referencing Issues**: Use keywords like `Closes`, `Fixes`, or `Resolves` to automatically link and close issues (e.g., `Closes #123`).
  * **Breaking Changes**: Start the footer with `BREAKING CHANGE:` followed by a description of the change, its justification, and any migration notes for other developers.
  * **Co-authoring**: If a commit has multiple authors, add `Co-authored-by:` lines.

## Strict Commit Message Format
To ensure consistency and clarity, all commit messages must strictly adhere to the following format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Rules for Each Section

#### Header (Mandatory)
* **`<type>`**: Must be one of the predefined types (e.g., feat, fix, docs, style, refactor, perf, test, chore, build, ci).
* **`<scope>`**: Must specify the affected part of the codebase (e.g., api, ui, auth, docs). Use lowercase and hyphen-separated words.
* **`<subject>`**: Must be a concise summary of the change:
  * Maximum 50 characters.
  * Imperative present tense (e.g., "add feature," not "added feature").
  * No capitalization of the first letter.
  * No ending punctuation.

#### Body (Optional)
* Must explain the "what" and "why" of the change.
* Separate from the header with a blank line.
* Wrap lines at 72 characters.
* Include side effects, performance notes, or other key details.

#### Footer (Optional)
* **Referencing Issues**: Use keywords like `Closes`, `Fixes`, or `Resolves` followed by the issue number (e.g., `Closes #123`).
* **Breaking Changes**: Start with `BREAKING CHANGE:` followed by a detailed description and migration notes.
* **Co-authoring**: Use `Co-authored-by:` for multiple authors.

## Best Practices
  * **Focused Commits**: Each commit should represent a single logical unit of work. Stage only related changes before committing.
  * **Commit Frequency**: Commit early and often. Avoid commits that break the build.
  * **Be Descriptive**: Avoid vague words like "update," "change," or "stuff."
  * **Pre-Commit Checks**:
      * Run tests before committing, if they exist.
      * Review your changes with `git diff --staged`.
      * Proofread for spelling and correct file or function names.
  * **Multiple Changes**: If a commit includes multiple types of changes, use the most significant one or split it into separate commits.

## Using with AI Assistants (e.g., GitHub Copilot)
You can ask an AI assistant to generate a commit message based on your staged changes.
1.  Stage all related changes for the commit.
2.  In the commit message box, you can use a prompt like: "Write a conventional commit message for the staged changes."
3.  Always read and edit the AI's suggestion carefully to ensure it is accurate and follows these guidelines.

## Examples
#### A Simple Fix
```
fix(auth): correct password validation regex
```

#### A New Feature with a Scope
```
feat(parser): support JSON input

Add JSON input handling to ReportConverter so users can migrate
existing JSON reports without first converting to XML.

Closes #45
```

#### A Breaking Change
```
refactor(api): rename user ID field from `uid` to `userId`

BREAKING CHANGE: The `uid` field in the user object has been
renamed to `userId` to improve consistency across the API.
All clients must be updated to use the new field name.
```

#### Adding a requirements.txt File
```
chore(dependencies): add requirements.txt file

Add a requirements.txt file to manage Python dependencies.
This file includes all necessary packages for the project.
```