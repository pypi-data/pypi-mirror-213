# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         6/03/23 16:24
# Project:      CFHL Transactional Backend
# Module Name:  offer_state_machine
# Description:
# ****************************************************************

from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import DatabaseError
from django.utils.translation import gettext_lazy as _
from oasis.models import Operation, Company
from oasis.models import StateMachine
from zibanu.django.repository.lib.utils import DocumentGenerator
from zibanu.django.utils import Email
from oasis.coffee_offers.lib.choices import OasisChoices
from num2words import num2words
from zibanu.django.repository.models import Document


class OfferStateMachine:
    PREFIX = "coffee_offers"

    def __init__(self, offer, operation):
        user_model = get_user_model()
        self.__offer = offer
        self.__operation = operation
        self.__from_status = offer.status
        try:
            self.__user = user_model.objects.get(pk=offer.user_id)
        except user_model.DoesNotExists as exc:
            raise ValueError(_("User associated to offer does not exists."))

    def __execute_flags(self, state: StateMachine):
        """
        Execute tasks from state flags
        :return: None
        """
        # Modified for notifications at 2023/06/10 - jgonzalez
        default_company = settings.OASIS_DEFAULT_COMPANY
        company_data = Company.objects.get_by_company_id(default_company).first()
        title_state = OasisChoices.states.get(state.oasis_state, None)
        title_status = OasisChoices.status.get(state.oasis_status, None)
        total_offer = self.__offer.kg_offered * self.__offer.price
        total_offer_words = num2words(total_offer, lang="es_CO")
        factor = settings.COFFEE_OFFERS_FACTOR

        # Modified for notifications at 2023/05/31 - Macercha
        template_list = [
            (_("Coffee Offer"), settings.COFFEE_OFFERS_OFFER_TEMPLATE),
            (_("Coffee Offer Contract"), settings.COFFEE_OFFERS_CONTRACT_TEMPLATE),
            (_("Promise"), settings.COFFEE_OFFERS_PROMISE_TEMPLATE),
            (_("Intention Letter"), settings.COFFEE_OFFERS_INTENTION_LETTER_TEMPLATE)
        ]
        print(template_list[0][0])
        # Set email targets based on flags
        mail_recipients = []
        if state.notify_user:
            mail_recipients.append(self.__user.email)
        if state.notify_legal_area:
            tmp_email = getattr(settings, "COFFEE_OFFERS_LEGAL_AREA_EMAIL", None)
            if tmp_email is not None:
                mail_recipients.append(tmp_email)
        if state.notify_coffee_area:
            tmp_email = getattr(settings, "COFFEE_OFFERS_COFFEE_AREA_EMAIL", None)
            if tmp_email is not None:
                mail_recipients.append(tmp_email)

        # If exists mail_recipients
        file_list = []
        if len(mail_recipients) > 0:
            template_context = {
                "user": self.__user,
                "offer": self.__offer,
                "total_offer": total_offer,
                "total_offer_words": total_offer_words,
                "company": company_data,
                "from_status": state.get_from_state_display(),
                "new_status": state.get_state_display(),
                "title_state": title_state,
                "title_status": title_status,
                "factor": factor,
                "file_list": file_list
            }
            attachments = []
            if state.send_contract:
                email_template = settings.COFFEE_OFFERS_REMITTANCE_EMAIL_TEMPLATE
                doc_generator = DocumentGenerator(self.PREFIX)
                index = 0
                for template in template_list:
                    document_id = doc_generator.generate_from_template(template_name=template[1],
                                                                       context=template_context, user=self.__user,
                                                                       description=template[0])
                    document_file = doc_generator.get_file(user=self.__user, uuid=document_id)

                    file_list.append({"name": document_id, "description": template_list[index][0]})
                    attachments.append(document_file)
                    index += 1
            else:
                email_template = settings.COFFEE_OFFERS_NOTIFICATION_EMAIL_TEMPLATE
            # Create emails
            email = Email(subject=_("Coffee Offer Notification"), to=mail_recipients, body=_("Coffee Offer"),
                          context=template_context)
            email.set_html_template(template=email_template)
            for attachment_file in attachments:
                email.attach_file(attachment_file)
            email.send()

    def run(self) -> None:
        """
        Run a machine state to get and assign next state value.
        :return:
        """
        # TODO: Unify run and set methods.
        oasis_state = self.__operation.state
        oasis_status = self.__operation.status
        state = StateMachine.objects.get_next_state(from_state=self.__from_status, oasis_state=oasis_state,
                                                    oasis_status=oasis_status)
        if state is not None:
            self.__offer.status = state.state

            # Change kg received
            if self.__offer.kg_received != self.__operation.quantity:
                self.__offer.kg_received = self.__operation.quantity

            if state.is_changed:
                # Change kg offered
                if self.__offer.kg_offered != self.__operation.otherif:
                    self.__offer.kg_offered = self.__operation.otherif
                # Change delivery date
                if self.__offer.delivery_date != self.__operation.finaldate:
                    self.__offer.delivery_date = self.__operation.finaldate

            self.__offer.save()
            self.__execute_flags(state)

    def set(self, new_state: int) -> None:
        """
        Set a new state and assign state and status in oasis operation entity
        :param new_state: new state value
        :return:
        """
        state = StateMachine.objects.get_next_oasis_status(from_state=self.__offer.status, new_state=new_state)

        if state is not None:
            if Operation.objects.update_status(location_id=self.__operation.locationid,
                                               document_id=self.__operation.documentid,
                                               number_id=self.__operation.numberid, state=state.oasis_state,
                                               status=state.oasis_status):
                self.__offer.status = new_state
                self.__offer.save()
                self.__execute_flags(state)
            else:
                raise DatabaseError(_("Error updating operation record"))

    def validate_timeout(self) -> None:
        """
        Validate a state timeout and set a new state.
        :return:
        """
        now = timezone.now()
        state = StateMachine.objects.get_current_state(current_state=self.__offer.status,
                                                       oasis_state=self.__operation.state,
                                                       oasis_status=self.__operation.status)
        if state is not None and state.timeout > 0:
            if (now - self.__offer.modified_at) > timedelta(hours=state.timeout):
                self.set(state.state_at_timeout)
