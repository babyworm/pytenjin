# pyTenjin User's Guide

release: 1.0.0

> **NOTE:**
>
> - pyTenjin now supports indent-free syntax since version 1.0.0. See [Basic Examples](guide/02-basic-examples.md#render-template) for details.
> - New embedded notation (`{=...=}` and `{==...==}`) is available since version 1.0.0. See [Basic Examples](guide/02-basic-examples.md#render-template) for details.
> - Since 1.1.0, it is possible to include pair of `{` and `}` inside of `${...}` or `#{...}`. See [Basic Examples](guide/02-basic-examples.md#template-syntax).

## Table of Contents

### [1. Overview](guide/01-overview.md)
- Features
- Install
- Benchmark

### [2. Basic Examples](guide/02-basic-examples.md)
- Template Syntax
- Render Template
- Show Converted Source Code
- Layout Template
- Context Variables
- Template Arguments
- Include Partial Template
- Template Short Name
- Template Encoding
- Helper Functions (tenjin.helpers, tenjin.escaped, tenjin.html)

### [3. Advanced Features](guide/03-advanced-features.md)
- Auto-escaping
- Nested Layout Template
- Trace Templates
- Capturing
- Template Cache
- Fragment Cache
- Logging
- Google App Engine Support *(legacy)*
- M17N Page

### [4. Preprocessing](guide/04-preprocessing.md)
- What is Preprocessing?
- TrimPreprocessor
- PrefixedLinePreprocessor
- JavaScriptPreprocessor
- TemplatePreprocessor (Loop Expansion, Parameters)

### [5. Tips](guide/05-tips.md)
- Specify Function Names of escape() and to_str()
- Webext
- Template Inheritance
- Template File Suffix

### [6. `pytenjin` Command](guide/06-command.md)
- Syntax Check
- Convert Template into Python Script
- Retrieve Embedded Code
- Execute Template File
- Context Data

### [7. Troubleshooting](guide/07-troubleshooting.md)
- SyntaxError exception
- Encoding declaration in Unicode string *(Python 2.x)*
- UnicodeDecodeError *(Python 2.x)*
- NameError: global name not defined

### [8. Customization Examples](guide/08-customization.md)
- Template Encoding
- Escaping Function
- Change Behaviour of to_str()
- Embedded Notation
- Custom Safe Template
- Custom Html Helper Function
- Switch Default Template Class
- Change Template Loader
- Change Template Cache Storage
- Change Fragment Cache Store
