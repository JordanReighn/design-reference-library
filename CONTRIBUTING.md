# Contributing

Thanks for helping improve Design Reference Library.

## Before opening a pull request

1. Keep the plugin focused on selecting, synthesizing, and applying design references.
2. Preserve product identity, accessibility, and implementation verification as core guardrails.
3. Do not add proprietary fonts, logos, trademark assets, screenshots, or copyrighted artwork.
4. Keep brand references descriptive and clearly unaffiliated.
5. Use the sync script for vendored upstream references instead of editing generated files manually.

## Development setup

Clone the repository and add it as a local marketplace:

~~~powershell
codex plugin marketplace add .
codex plugin add design-reference-library@jordanreighn-design
~~~

Start a new Codex task after reinstalling the plugin.

For Claude Code, run these commands inside Claude Code:

~~~text
/plugin marketplace add .
/plugin install design-reference-library@jordanreighn-design
/reload-plugins
~~~

## Validation

From the repository root:

~~~powershell
python scripts/validate_manifests.py
python plugins/design-reference-library/skills/design-reference-library/scripts/validate_library.py
python -X utf8 path/to/skill-creator/scripts/quick_validate.py plugins/design-reference-library/skills/design-reference-library
python path/to/plugin-creator/scripts/validate_plugin.py plugins/design-reference-library
~~~

The final two validators ship with Codex's built-in creator skills; adjust their local paths for your installation. Contributors with Claude Code installed should also run:

~~~powershell
claude plugin validate . --strict
claude plugin validate ./plugins/design-reference-library --strict
~~~

## Updating upstream references

~~~powershell
python plugins/design-reference-library/skills/design-reference-library/scripts/sync_upstream.py
~~~

Review the resolved commit and generated catalog, run validation, and describe the upstream change in the pull request.

## Pull requests

- Keep changes narrowly scoped.
- Explain the user-facing behavior being improved.
- Include validation results.
- Update CHANGELOG.md for meaningful behavior or packaging changes.
