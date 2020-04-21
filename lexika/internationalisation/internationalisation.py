#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import gettext

langue_système = locale.getlocale()[0].split("_")[0] if locale.getlocale()[0] else "fr"
langue_préférée = gettext.translation("messages", localedir="internationalisation", languages=[langue_système], fallback=True)
langue_préférée.install()
