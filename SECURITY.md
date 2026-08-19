# Security policy

## Supported versions

Security fixes are applied to the latest version on the default branch.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting feature for this repository. Do not include secrets, private source code, access tokens, or personal data in a public issue.

## Scope

This plugin is primarily a local skill and reference package. It does not require authentication or transmit project files by itself. The optional upstream sync script connects to the configured Git repository and replaces only its documented vendored reference files.

When using the plugin, review any generated code and external links before deployment.
