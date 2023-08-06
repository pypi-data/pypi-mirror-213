from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket_shared_bonds import (
    ChangeTariffTicketSharedBond,
)


class TestCaseChangeTariffTicketSharedBonds:
    def test_create(self, mocker):
        username = "7456787G"
        customer_code = "1234"
        ticket_creator_id = "1"
        ticket_id = "2"

        OTRSClientMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket_shared_bonds.OTRSClient",
            return_value=mocker.Mock(),
        )

        ticket_mock = mocker.Mock(spec=["create"])
        ticket_mock.create.return_value = mocker.Mock(spec=["tid"])
        ticket_mock.create.return_value.tid = ticket_id
        ticket_creator_mock = mocker.Mock(spec=["create"])
        ticket_creator_mock.create.return_value = mocker.Mock(spec=["tid"])
        ticket_creator_mock.create.return_value.tid = ticket_creator_id

        def side_effect(uname, customer_c, fields):
            if fields.get("phone_number") == "666666666":
                return ticket_creator_mock
            elif fields.get("phone_number") == "777777777":
                return ticket_mock

        ChangeTariffTicketSharedBondMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket_shared_bonds.ChangeTariffTicket",
            side_effect=side_effect,
        )

        fields_dict = {
            "phone_numbers": ["666666666", "777777777"],
            "other_fields": "other_values",
        }

        ChangeTariffTicketSharedBond(username, customer_code, fields_dict).create()

        assert ChangeTariffTicketSharedBondMock.call_count == 2
        ticket_mock.create.assert_called()
        ticket_creator_mock.create.assert_called()
        OTRSClientMock.return_value.link_tickets.assert_called_once_with(
            ticket_creator_id,
            ticket_id,
            link_type="ParentChild",
        )
