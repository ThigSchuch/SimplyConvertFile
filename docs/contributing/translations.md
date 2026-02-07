---
layout: default
title: Translations
parent: Contributing
nav_order: 2
---

# Translations
{: .no_toc }

SimplyConvertFile supports multiple languages through gettext translations.

---

## Currently Supported Languages

| Language | Code |
|:---------|:-----|
| Basque | `eu` |
| Catalan | `ca` |
| Czech | `cs` |
| Danish | `da` |
| Dutch | `nl` |
| English | default |
| Finnish | `fi` |
| French | `fr` |
| Hungarian | `hu` |
| Icelandic | `is` |
| Italian | `it` |
| Japanese | `ja` |
| Portuguese | `pt` |
| Brazilian Portuguese | `pt_BR` |
| Spanish | `es` |
| Turkish | `tr` |
| Ukrainian | `uk` |
| Vietnamese | `vi` |

## Adding a New Language

1. Copy the template file:
   ```bash
   cp src/simplyconvertfile/po/simplyconvertfile.pot src/simplyconvertfile/po/your_language.po
   ```

2. Translate the strings in the new `.po` file

3. Submit a pull request
