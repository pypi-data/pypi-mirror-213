# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         26/02/23 15:31
# Project:      CFHL Transactional Backend
# Module Name:  states
# Description:
# ****************************************************************
from django.utils.translation import gettext_lazy as _


class OasisChoices:
    # Modified for notifications at 2023/06/10 - jgonzalez
    states = {"A": _("Active"), "P": _("Processed"), "X": _("Canceled")}
    status = {"P": _("Pending"), "D": _("Dispatched"), "T": _("Finished"), "R": _("For sign"), "X": _("Canceled")}
