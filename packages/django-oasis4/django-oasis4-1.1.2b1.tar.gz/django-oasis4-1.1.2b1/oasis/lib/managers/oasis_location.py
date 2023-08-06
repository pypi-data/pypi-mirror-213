# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         23/02/23 9:16
# Project:      CFHL Transactional Backend
# Module Name:  oasis_location
# Description:
# ****************************************************************
from oasis import models as oasis_models
from zibanu.django.db import models
from zibanu.django.db.models import Subquery, OuterRef


class OasisLocation(models.Manager):
    """
    Manager class of Location class entity
    """

    def get_coffe_ware_houses(self):
        # Se incorpora el nombre del municipio donde se encuentra la bodega.
        # qs = self.get_queryset().filter(businessid__exact=1, level__exact=2, pointofsales__exact=1)
        qs = self.annotate(
            city=Subquery(
                oasis_models.GeographicLocation.objects.filter(
                    geographiclocationid__exact=OuterRef("geographiclocationid")).values(
                    "geographiclocationname")[:1]
            )
        ).filter(businessid__exact=1, level__exact=2, pointofsales__exact=1).values("locationid", "locationname",
                                                                                    "city")
        return qs
