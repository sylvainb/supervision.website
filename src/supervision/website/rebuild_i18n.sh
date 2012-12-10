#!/bin/sh

# Synchronise the .pot with the templates.
i18ndude rebuild-pot --pot locales/supervision.website.pot --merge locales/manual.pot --create supervision.website .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/supervision.website.pot locales/*/LC_MESSAGES/supervision.website.po