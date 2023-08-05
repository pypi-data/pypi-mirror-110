from cfdp import logger
from cfdp.constants import MachineState, TransmissionMode, DeliveryCode,\
    ConditionCode, DirectiveCode, DirectiveSubTypeCode, TransactionStatus
from cfdp.event import EventType
from cfdp.pdu import NakPdu, AckPdu, FinishedPdu
from cfdp.meta import execute_filestore_requests
from .timer import InactivityTimer, AckTimer, NakTimer
from .base import Machine


class Receiver2(Machine):

    """Implementation of Class 2 (acknowledged transfer) receiver."""

    def __init__(self, kernel, transaction):
        super().__init__(kernel, transaction)
        self.transmission_mode = TransmissionMode.ACKNOWLEDGED
        self.state = MachineState.WAIT_FOR_EOF
        self.file_size = None

        # inactivity timer
        timeout = kernel.config.get(
            transaction.source_entity_id).transaction_inactivity_limit
        self.inactivity_timer = InactivityTimer(
            self, timeout, EventType.E27_INACTIVITY_TIMEOUT)

        # ack timer
        timeout = kernel.config.get(
            transaction.source_entity_id).positive_ack_timer_interval
        limit = kernel.config.get(
            transaction.source_entity_id).positive_ack_timer_expiration_limit
        self.ack_timer = AckTimer(
            self, timeout, EventType.E25_ACK_TIMEOUT, limit)

        # nak timer
        timeout = kernel.config.get(
            transaction.source_entity_id).nak_timer_interval
        limit = kernel.config.get(
            transaction.source_entity_id).nak_timer_expiration_limit
        self.nak_timer = NakTimer(
            self, timeout, EventType.E26_NAK_TIMEOUT, limit)

    def update_state(self, event, pdu=None):
        """ See state table given in CCSDS 720.2-G-3, Table 5-4 """
        logger.debug(
            "[{}] Event: {}, State: {}".format(
                event.transaction.id, event.type, self.state))

        if pdu:
            self._restart_inactivity_timer()  # as per CCSDS 720.2-G-3, 5.3.7

        if self.state == MachineState.WAIT_FOR_EOF:

            if event.type == EventType.E0_ENTERED_STATE:
                self._initialize()
                self._restart_inactivity_timer()

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
                self._resume_inactivity_timer()

            elif event.type == EventType.E10_RECEIVED_METADATA:
                self._reuse_senders_first_pdu_header(pdu)
                if not self.metadata_received:
                    self.metadata_received = True
                    self.file_size = pdu.file_size
                    self._issue_metadata_received_indication(pdu.file_size)
                    if self._is_file_transfer():
                        if not self.file_open:
                            self._open_temp_file()
                            self.file_open = True
                    self._update_nak_list(event, self.file_size)
                    self._process_metadata_options(pdu)

            elif event.type == EventType.E11_RECEIVED_FILEDATA:
                self._issue_filesegment_received_indication(
                    pdu.segment_offset, len(pdu.file_data))
                self._reuse_senders_first_pdu_header(pdu)
                if not self.file_open:
                    self._open_temp_file()
                    self.file_open = True
                self._store_file_data(pdu)
                self._update_received_file_size(pdu)
                self._update_nak_list(event, self.file_size)

            elif event.type == EventType.E12_RECEIVED_EOF_NO_ERROR:
                self._reuse_senders_first_pdu_header(pdu)
                self._update_nak_list(event, pdu.file_size)
                self._send_ack_eof()

                if self._is_file_size_error(pdu.file_size):
                    self._fault_file_size()

                self.received_file_checksum = pdu.file_checksum

                if self._is_nak_list_empty():
                    self.state = MachineState.SEND_FINISHED
                else:
                    self.state = MachineState.GET_MISSING_DATA
                self.trigger_event(EventType.E0_ENTERED_STATE)

            elif event.type == EventType.E13_RECEIVED_EOF_CANCEL:
                self._reuse_senders_first_pdu_header(pdu)
                self.condition_code = pdu.condition_code
                self._send_ack_eof()
                self._issue_transaction_finished_indication()
                self._shutdown()

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

        elif self.state == MachineState.GET_MISSING_DATA:

            if event.type == EventType.E0_ENTERED_STATE:
                if not self.suspended and not self.frozen:
                    self._send_nak()
                self._restart_nak_timer()

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
                self._restart_inactivity_timer()

            elif event.type == EventType.E10_RECEIVED_METADATA:
                if not self.metadata_received:
                    self.transaction.source_filename = pdu.source_filename
                    self.transaction.destination_filename =\
                        pdu.destination_filename
                    self.transaction.filestore_requests =\
                        pdu.filestore_requests
                    self.transaction.messages_to_user = pdu.messages_to_user

                    self.metadata_received = True
                    self.file_size = pdu.file_size
                    self._issue_metadata_received_indication(pdu.file_size)

                    if self._is_file_transfer():
                        if not self.file_open:
                            self._open_temp_file()
                            self.file_open = True
                    self._update_nak_list(event, self.file_size)
                    self._process_metadata_options(pdu)

            elif event.type == EventType.E11_RECEIVED_FILEDATA:
                if not self.file_open:
                    self._open_temp_file()
                    self.file_open = True
                self._store_file_data(pdu)
                self._update_received_file_size(pdu)
                self._update_nak_list(event, self.file_size)

            elif event.type == EventType.E12_RECEIVED_EOF_NO_ERROR:
                self._send_ack_eof()

            elif event.type == EventType.E13_RECEIVED_EOF_CANCEL:
                self.condition_code = pdu.condition_code
                self._send_ack_eof()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E26_NAK_TIMEOUT:
                self._restart_nak_timer()
                if self._is_nak_list_empty():
                    self.state = MachineState.SEND_FINISHED
                    self.trigger_event(EventType.E0_ENTERED_STATE)
                elif not self.suspended and not self.frozen:
                    if self.nak_timer.is_limit_reached():
                        self._fault_nak_limit()
                    self._send_nak()

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

        elif self.state == MachineState.SEND_FINISHED:

            if event.type == EventType.E0_ENTERED_STATE:
                self.delivery_code = DeliveryCode.DATA_COMPLETE
                self._cancel_nak_timer()

                if self._is_file_transfer():
                    if self._is_file_checksum_failure(
                            self.received_file_checksum):
                        self._fault_file_checksum()
                    self._copy_temp_file_to_dest_file()
                    self._close_temp_file()

                if self.transaction.filestore_requests:
                    execute_filestore_requests(
                        self.kernel, self.transaction.filestore_requests)

                self._send_finished()
                self._restart_ack_timer()

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
                self._suspend_ack_timer()

            elif event.type == EventType.E6_RESUME_TIMERS:
                self._restart_inactivity_timer()
                self._resume_ack_timer()

            elif event.type == EventType.E12_RECEIVED_EOF_NO_ERROR:
                self._send_ack_eof()

            elif event.type == EventType.E13_RECEIVED_EOF_CANCEL:
                self.condition_code = pdu.condition_code
                self._send_ack_eof()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E18_RECEIVED_ACK_FINISHED:
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E25_ACK_TIMEOUT:
                self._restart_ack_timer()
                if self.ack_timer.is_limit_reached():
                    self._fault_ack_limit()
                self._send_finished()

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
                self._send_finished()
                self._restart_ack_timer()

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
                self._restart_inactivity_timer()
                self._resume_ack_timer()

            elif event.type == EventType.E13_RECEIVED_EOF_CANCEL:
                self.condition_code = pdu.condition_code
                self._send_ack_eof()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E18_RECEIVED_ACK_FINISHED:
                if self.condition_code != ConditionCode.NO_ERROR:
                    self._issue_transaction_finished_indication()
                    self._shutdown()

            elif event.type == EventType.E25_ACK_TIMEOUT:
                self._restart_ack_timer()
                if self.ack_timer.is_limit_reached():
                    self.trigger_event(EventType.E2_ABANDON_TRANSACTION)
                else:
                    self.condition_code = ConditionCode.CANCEL_REQUEST_RECEIVED
                    self._send_finished()

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
        self.nak_timer.shutdown()

    def _send_nak(self):
        logger.debug("[{}] Send Nak".format(self.transaction.id))
        segment_requests = self._get_segment_requests()
        pdu = NakPdu(
            direction=self.first_pdu_header.direction,
            transmission_mode=self.first_pdu_header.transmission_mode,
            source_entity_id=self.first_pdu_header.source_entity_id,
            transaction_seq_number=self.first_pdu_header.transaction_seq_number,
            destination_entity_id=self.first_pdu_header.destination_entity_id,
            #
            start_of_scope=0,
            end_of_scope=self.received_file_size,
            segment_requests=segment_requests)
        address = self.kernel.config.get(
            self.first_pdu_header.source_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)

    def _send_ack_eof(self):
        logger.debug("[{}] Send Ack EOF".format(self.transaction.id))
        pdu = AckPdu(
            direction=self.first_pdu_header.direction,
            transmission_mode=self.first_pdu_header.transmission_mode,
            source_entity_id=self.first_pdu_header.source_entity_id,
            transaction_seq_number=self.first_pdu_header.transaction_seq_number,
            destination_entity_id=self.first_pdu_header.destination_entity_id,
            #
            directive_code_ack=DirectiveCode.EOF,
            directive_subtype_code=DirectiveSubTypeCode.ACK_OTHERS,
            condition_code=self.condition_code,
            transaction_status=TransactionStatus.UNDEFINED)
        address = self.kernel.config.get(
            self.first_pdu_header.source_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)

    def _send_finished(self):
        logger.debug("[{}] Send Finished".format(self.transaction.id))
        pdu = FinishedPdu(
            direction=self.first_pdu_header.direction,
            transmission_mode=self.first_pdu_header.transmission_mode,
            source_entity_id=self.first_pdu_header.source_entity_id,
            transaction_seq_number=self.first_pdu_header.transaction_seq_number,
            destination_entity_id=self.first_pdu_header.destination_entity_id,
            #
            condition_code=self.condition_code,
            delivery_code=self.delivery_code,
            file_status=self.file_status,
            filestore_responses=self.filestore_responses,
            fault_location=None)
        address = self.kernel.config.get(
            self.first_pdu_header.source_entity_id).ut_address
        self.kernel.transport.request(pdu.to_bytes(), address)
