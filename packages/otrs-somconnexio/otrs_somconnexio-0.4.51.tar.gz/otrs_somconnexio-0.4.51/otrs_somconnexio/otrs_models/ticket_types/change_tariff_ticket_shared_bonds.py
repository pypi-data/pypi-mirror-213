from otrs_somconnexio.client import OTRSClient
from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket import (
    ChangeTariffTicket,
)


class ChangeTariffTicketSharedBond:
    def __init__(
        self,
        username,
        customer_code,
        fields_dict,
        override_ticket_ids=[],
        # TODO: Can we remove this field?
        fallback_path="/tmp/tickets/",
    ):
        self.username = username
        self.customer_code = customer_code
        self.fields = fields_dict

    def create(self):
        fields = self.fields
        phone_numbers = fields.pop("phone_numbers")

        otrs_client = OTRSClient()

        ticket_creator = self._create_ticket(fields, phone_numbers.pop(0))
        for phone_number in phone_numbers:
            ticket = self._create_ticket(fields, phone_number)
            otrs_client.link_tickets(
                ticket_creator.tid, ticket.tid, link_type="ParentChild"
            )

    def _create_ticket(self, fields, phone_number):
        fields["phone_number"] = phone_number
        return ChangeTariffTicket(
            self.username,
            self.customer_code,
            fields,
        ).create()
