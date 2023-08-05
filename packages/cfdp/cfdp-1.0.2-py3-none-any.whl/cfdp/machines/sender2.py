from cfdp import logger
from cfdp.constants import MachineState, ConditionCode, Direction,\
    DirectiveCode, TransactionStatus, TransmissionMode, DirectiveSubTypeCode
from cfdp.event import EventType
from cfdp.pdu import MetadataPdu, FiledataPdu, EofPdu, AckPdu
from .timer import InactivityTimer, AckTimer
from .base import Machine


class Sender2(Machine):

    """Implementation of Class 2 (acknowledged transfer) sender."""

    def __init__(self, kernel, transaction):
        super().__init__(kernel, transaction)
        self.transmission_mode = TransmissionMode.ACKNOWLEDGED
        self.state = MachineState.SEND_METADATA

        # inactivity timer
        timeout = kernel.config.get(
            transaction.destination_entity_id).transaction_inactivity_limit
        self.inactivity_timer = InactivityTimer(
            self, timeout, EventType.E27_INACTIVITY_TIMEOUT)

        # ack timer
        timeout = kernel.config.get(
            transaction.destination_entity_id).positive_ack_timer_interval
        limit = kernel.config.get(transaction.destination_entity_id)\
            .positive_ack_timer_expiration_limit
        self.ack_timer = AckTimer(
            self, timeout, EventType.E25_ACK_TIMEOUT, limit)

    def update_state(self, event, pdu=None):
        """ See state table given in CCSDS 720.2-G-3, Table 5-3 """
        logger.debug(
            "[{}] Event: {}, State: {}".format(
                event.transaction.id, event.type, self.state))

        if pdu:
            self._restart_inactivity_timer()  # as per CCSDS 720.2-G-3, 5.3.7

        if self.state == MachineState.SEND_METADATA:

            if event.type == EventType.E0_ENTERED_STATE:
                self._initialize()

            elif event.type == EventType.E30_RECEIVED_PUT_REQUEST:
                self._issue_transaction_indication()
                self._send_metadata()
                if self._is_file_transfer():
                    self.state = MachineState.SEND_FILE
                else:
                    self.state = MachineState.SEND_EOF
                self.trigger_event(EventType.E0_ENTERED_STATE)

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

        elif self.state == MachineState.SEND_FILE:

            if event.type == EventType.E0_ENTERED_STATE:
                self._open_source_file()
                self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E1_SEND_FILE_DATA:
                if not self.frozen\
                        and not self.suspended:
                    if self._is_comm_layer_ready():
                        self._send_file_data()
                        if self._is_entire_file_sent():
                            self.state = MachineState.SEND_EOF
                            self.trigger_event(EventType.E0_ENTERED_STATE)
                    self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E2_ABANDON_TRANSACTION:
                self._issue_abandoned_indication()
                self._shutdown()

            elif event.type == EventType.E3_NOTICE_OF_CANCELLATION:
                self.state = MachineState.TRANSACTION_CANCELLED
                self.trigger_event(EventType.E0_ENTERED_STATE)

            elif event.type == EventType.E4_NOTICE_OF_SUSPENSION:
                if not self.suspended:
                    self._issue_suspended_indication()
                    self.suspended = True
                    if not self.frozen:
                        self.trigger_event(EventType.E5_SUSPEND_TIMERS)

            elif event.type == EventType.E5_SUSPEND_TIMERS:
                self._suspend_inactivity_timer()

            elif event.type == EventType.E6_RESUME_TIMERS:
                self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E15_RECEIVED_NAK:
                if not self.suspended and not self.frozen:
                    self._queue_nakked_data(pdu)

            elif event.type == EventType.E17_RECEIVED_FINISHED_CANCEL:
                self.condition_code = pdu.condition_code
                self._send_ack_finished()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E31_RECEIVED_SUSPEND_REQUEST:
                self.trigger_event(EventType.E4_NOTICE_OF_SUSPENSION)

            elif event.type == EventType.E32_RECEIVED_RESUME_REQUEST:
                if self.suspended:
                    self._issue_resumed_indication()
                    self.suspended = False
                    if not self.frozen:
                        self.trigger_event(EventType.E6_RESUME_TIMERS)

            elif event.type == EventType.E33_RECEIVED_CANCEL_REQUEST:
                self.condition_code = ConditionCode.CANCEL_REQUEST_RECEIVED
                self.trigger_event(EventType.E3_NOTICE_OF_CANCELLATION)

            elif event.type == EventType.E34_RECEIVED_REPORT_REQUEST:
                self._issue_report_indication()

            elif event.type == EventType.E40_RECEIVED_FREEZE:
                if not self.frozen:
                    self.frozen = True
                    if not self.suspended:
                        self.trigger_event(EventType.E5_SUSPEND_TIMERS)

            elif event.type == EventType.E41_RECEIVED_THAW:
                if self.frozen:
                    self.frozen = False
                    if not self.suspended:
                        self.trigger_event(EventType.E6_RESUME_TIMERS)

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

        elif self.state == MachineState.SEND_EOF:

            if event.type == EventType.E0_ENTERED_STATE:
                self._send_eof()
                self._issue_eof_sent_indication()
                self._restart_ack_timer()
                self._restart_inactivity_timer()

            elif event.type == EventType.E1_SEND_FILE_DATA:
                if not self.suspended and not self.frozen:
                    if self._is_file_data_queued():
                        if self._is_comm_layer_ready():
                            self._send_missing_file_data()
                        self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E2_ABANDON_TRANSACTION:
                self._issue_abandoned_indication()
                self._shutdown()

            elif event.type == EventType.E3_NOTICE_OF_CANCELLATION:
                self.state = MachineState.TRANSACTION_CANCELLED
                self.trigger_event(EventType.E0_ENTERED_STATE)

            elif event.type == EventType.E4_NOTICE_OF_SUSPENSION:
                if not self.suspended:
                    self._issue_suspended_indication()
                    self.suspended = True
                    if not self.frozen:
                        self.trigger_event(EventType.E5_SUSPEND_TIMERS)

            elif event.type == EventType.E5_SUSPEND_TIMERS:
                self._suspend_inactivity_timer()
                if self._is_ack_timer_running():
                    self._suspend_ack_timer()

            elif event.type == EventType.E6_RESUME_TIMERS:
                self._resume_inactivity_timer()
                if self._is_ack_timer_suspended():
                    self._resume_ack_timer()
                self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E14_RECEIVED_ACK_EOF:
                self._cancel_ack_timer()

            elif event.type == EventType.E15_RECEIVED_NAK:
                if not self.suspended and not self.frozen:
                    self._queue_nakked_data(pdu)
                    self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E16_RECEIVED_FINISHED_NO_ERROR:
                self._send_ack_finished()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E17_RECEIVED_FINISHED_CANCEL:
                self.condition_code = pdu.condition_code
                self._send_ack_finished()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E25_ACK_TIMEOUT:
                self._restart_ack_timer()
                if self._is_ack_limit_reached():
                    self._fault_ack_limit()
                self._send_eof()

            elif event.type == EventType.E27_INACTIVITY_TIMEOUT:
                self._fault_inactivity()

            elif event.type == EventType.E31_RECEIVED_SUSPEND_REQUEST:
                self.trigger_event(EventType.E4_NOTICE_OF_SUSPENSION)

            elif event.type == EventType.E32_RECEIVED_RESUME_REQUEST:
                if self.suspended:
                    self._issue_resumed_indication()
                    self.suspended = False
                    if not self.frozen:
                        self.trigger_event(EventType.E6_RESUME_TIMERS)

            elif event.type == EventType.E33_RECEIVED_CANCEL_REQUEST:
                self.condition_code = ConditionCode.CANCEL_REQUEST_RECEIVED
                self.trigger_event(EventType.E3_NOTICE_OF_CANCELLATION)

            elif event.type == EventType.E34_RECEIVED_REPORT_REQUEST:
                self._issue_report_indication()

            elif event.type == EventType.E40_RECEIVED_FREEZE:
                if not self.frozen:
                    self.frozen = True
                    if not self.suspended:
                        self.trigger_event(EventType.E5_SUSPEND_TIMERS)

            elif event.type == EventType.E41_RECEIVED_THAW:
                if self.frozen:
                    self.frozen = False
                    if not self.suspended:
                        self.trigger_event(EventType.E6_RESUME_TIMERS)

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

        elif self.state == MachineState.TRANSACTION_CANCELLED:

            if event.type == EventType.E0_ENTERED_STATE:
                self.suspended = False
                self.condition_code = ConditionCode.CANCEL_REQUEST_RECEIVED
                self._send_eof()
                self._issue_eof_sent_indication()
                self._restart_ack_timer()
                self._restart_inactivity_timer()

            elif event.type == EventType.E2_ABANDON_TRANSACTION:
                self._issue_abandoned_indication()
                self._shutdown()

            elif event.type == EventType.E4_NOTICE_OF_SUSPENSION:
                if not self.suspended:
                    self._issue_suspended_indication()
                    self.suspended = True
                    if not self.frozen:
                        self.trigger_event(EventType.E5_SUSPEND_TIMERS)

            elif event.type == EventType.E5_SUSPEND_TIMERS:
                self._suspend_inactivity_timer()
                self._suspend_ack_timer()

            elif event.type == EventType.E6_RESUME_TIMERS:
                self._resume_inactivity_timer()
                self._resume_ack_timer()

            elif event.type == EventType.E14_RECEIVED_ACK_EOF:
                if self.condition_code != ConditionCode.NO_ERROR:
                    self._issue_transaction_finished_indication()
                    self._shutdown()

            elif event.type == EventType.E17_RECEIVED_FINISHED_CANCEL:
                self.condition_code = pdu.condition_code
                self._send_ack_finished()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E25_ACK_TIMEOUT:
                self._restart_ack_timer()
                if self._is_ack_limit_reached():
                    self.trigger_event(EventType.E2_ABANDON_TRANSACTION)
                else:
                    self._send_eof()

            elif event.type == EventType.E27_INACTIVITY_TIMEOUT:
                self._issue_abandoned_indication()
                self._shutdown()

            elif event.type == EventType.E31_RECEIVED_SUSPEND_REQUEST:
                self.trigger_event(EventType.E4_NOTICE_OF_SUSPENSION)

            elif event.type == EventType.E32_RECEIVED_RESUME_REQUEST:
                if self.suspended:
                    self._issue_resumed_indication()
                    self.suspended = False
                    if not self.frozen:
                        self.trigger_event(EventType.E6_RESUME_TIMERS)

            elif event.type == EventType.E34_RECEIVED_REPORT_REQUEST:
                self._issue_report_indication()

            elif event.type == EventType.E40_RECEIVED_FREEZE:
                if not self.frozen:
                    self.frozen = True
                    if not self.suspended:
                        self.trigger_event(EventType.E5_SUSPEND_TIMERS)

            elif event.type == EventType.E41_RECEIVED_THAW:
                if self.frozen:
                    self.frozen = False
                    if not self.suspended:
                        self.trigger_event(EventType.E6_RESUME_TIMERS)

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

    def _shutdown(self):
        super()._shutdown()
        self.inactivity_timer.shutdown()
        self.ack_timer.shutdown()

    def _send_metadata(self):
        logger.debug("[{}] Send Metadata".format(self.transaction.id))
        pdu = MetadataPdu(
            direction=Direction.TOWARD_RECEIVER,
            transmission_mode=self.transmission_mode,
            source_entity_id=self.transaction.source_entity_id,
            transaction_seq_number=self.transaction.seq_number,
            destination_entity_id=self.transaction.destination_entity_id,
            file_size=self.transaction.get_file_size(),
            source_filename=self.transaction.source_filename,
            destination_filename=self.transaction.destination_filename,
            filestore_requests=self.transaction.filestore_requests,
            messages_to_user=self.transaction.messages_to_user)
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)

    def _send_file_data(self):
        logger.debug("[{}] Send Filedata".format(self.transaction.id))
        offset, data = self.transaction.get_file_segment()
        pdu = FiledataPdu(
            direction=Direction.TOWARD_RECEIVER,
            transmission_mode=self.transmission_mode,
            source_entity_id=self.transaction.source_entity_id,
            transaction_seq_number=self.transaction.seq_number,
            destination_entity_id=self.transaction.destination_entity_id,
            segment_offset=offset,
            file_data=data)
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)

    def _send_eof(self):
        logger.debug("[{}] Send EOF".format(self.transaction.id))
        pdu = EofPdu(
            direction=Direction.TOWARD_RECEIVER,
            transmission_mode=self.transmission_mode,
            source_entity_id=self.transaction.source_entity_id,
            transaction_seq_number=self.transaction.seq_number,
            destination_entity_id=self.transaction.destination_entity_id,
            condition_code=self.condition_code,
            file_checksum=self.transaction.get_file_checksum(),
            file_size=self.transaction.get_file_size())
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)

    def _send_missing_file_data(self):
        logger.debug("[{}] Send Missing Filedata".format(self.transaction.id))
        start, end = self.nak_list.pop(0)
        length = end - start

        if start == 0 and length == 0:
            pdu = MetadataPdu(
                direction=Direction.TOWARD_RECEIVER,
                transmission_mode=self.transmission_mode,
                source_entity_id=self.transaction.source_entity_id,
                transaction_seq_number=self.transaction.seq_number,
                destination_entity_id=self.transaction.destination_entity_id,
                file_size=self.transaction.get_file_size(),
                source_filename=self.transaction.source_filename,
                destination_filename=self.transaction.destination_filename,
                filestore_requests=self.transaction.filestore_requests,
                messages_to_user=self.transaction.messages_to_user)
        else:
            _, file_data = self.transaction.get_file_segment(start, length)
            pdu = FiledataPdu(
                direction=Direction.TOWARD_RECEIVER,
                transmission_mode=self.transmission_mode,
                source_entity_id=self.transaction.source_entity_id,
                transaction_seq_number=self.transaction.seq_number,
                destination_entity_id=self.transaction.destination_entity_id,
                #
                segment_offset=start,
                file_data=file_data)
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)

    def _send_ack_finished(self):
        logger.debug("[{}] Send Ack Finished".format(self.transaction.id))
        pdu = AckPdu(
            direction=Direction.TOWARD_RECEIVER,
            transmission_mode=self.transmission_mode,
            source_entity_id=self.transaction.source_entity_id,
            transaction_seq_number=self.transaction.seq_number,
            destination_entity_id=self.transaction.destination_entity_id,
            #
            directive_code_ack=DirectiveCode.FINISHED,
            directive_subtype_code=DirectiveSubTypeCode.ACK_FINISHED,
            condition_code=self.condition_code,
            transaction_status=TransactionStatus.UNDEFINED)
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)
