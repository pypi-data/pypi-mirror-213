from devvio_util.primitives.address import Address
from devvio_util.primitives.signature import Signature
from devvio_util.primitives.utils import InputBuffer, set_uint64, set_uint8
from devvio_util.primitives.devv_sign import sign_binary, DevvHash
from devvio_util.primitives.transfer import Transfer
from devvio_util.primitives.devv_constants import kLEGACY_ENVELOPE_SIZE, kNODE_SIG_BUF_SIZE, kNODE_ADDR_BUF_SIZE, \
    kSIGNER_LENGTH_OFFSET, kUINT_SIZE, kMIN_PAYLOAD_SIZE, kFLAGS_OFFSET, kOPERATION_OFFSET, kLEGACY_OPERATION_OFFSET, \
    kENVELOPE_SIZE, OpType


class Transaction:
    """
    Holds a collection of Transfers and their corresponding signature.

    Note: serialization of legacy blocks not currently implemented
    """
    def __init__(self, raw_blk: InputBuffer = None, is_legacy: bool = None):
        self._tx_offset = None
        self._tx_size = None
        self._payload_size = None
        self._xfer_size = None
        self._signer_size = None
        self._signer = None
        self._is_legacy = None
        self._canonical = None
        self._sig = None
        if raw_blk:
            self.from_buffer(raw_blk, is_legacy)

    def from_buffer(self, buffer: InputBuffer, is_legacy: bool):
        """
        :param buffer: IO stream holding the Transaction binary
        :type buffer: InputBuffer
        :param is_legacy: if True, will follow canonical patterns for legacy blocks
        :type is_legacy: bool
        """
        self._tx_offset = buffer.tell()
        if is_legacy:
            self._xfer_size = buffer.get_next_uint64()
            self._payload_size = buffer.get_next_uint64()
            self._tx_size = kLEGACY_ENVELOPE_SIZE + self._xfer_size + self._payload_size + kNODE_SIG_BUF_SIZE
            self._signer_size = kNODE_ADDR_BUF_SIZE
        else:
            self._tx_size = buffer.get_next_uint64()
            self._xfer_size = buffer.get_next_uint64()
            self._payload_size = buffer.get_next_uint64()
            self._signer_size = buffer.get_int(self._tx_offset + kSIGNER_LENGTH_OFFSET, kUINT_SIZE) + 1
            self._signer = Address(buffer.get_bytes(self._tx_offset + kSIGNER_LENGTH_OFFSET, self._signer_size))

        if self._payload_size < kMIN_PAYLOAD_SIZE:
            raise Exception(f"Invalid Transaction: bad payload size {self._payload_size}")

        if not Address.is_valid_addr_size(self._signer_size):
            raise Exception(f"Invalid Transaction: bad signer size {self._signer_size}")

        if not is_legacy:
            flags = buffer.get_int(self._tx_offset + kFLAGS_OFFSET, kUINT_SIZE)
            if flags != 0:
                raise Exception("Invalid Transaction: unknown flags")
            oper = buffer.get_int(self._tx_offset + kOPERATION_OFFSET, kUINT_SIZE)
            if oper >= OpType.NUM_OPS:
                raise Exception("Invalid Transaction: invalid operation")
        else:
            oper = buffer.get_int(self._tx_offset + kLEGACY_OPERATION_OFFSET, kUINT_SIZE)
            if oper >= OpType.NUM_OPS:
                raise Exception("Invalid Transaction: invalid operation")
            self._is_legacy = True
        self._sig = self.get_sig_from_raw_blk(buffer)
        buffer.seek(self._tx_offset)
        self._canonical = buffer.get_next_bytes(self._tx_size)
        if not self._canonical:
            raise Exception(f"Invalid Transaction: buffer too small for tx (< {self._tx_size}")

    def get_sig_from_raw_blk(self, buffer: InputBuffer) -> Signature:
        """
        :param buffer: IO stream holding the Transaction binary
        :type buffer: InputBuffer
        :return: Signature object holding the sig for this transaction
        :rtype: Signature
        """
        if self._is_legacy:
            offset = self._tx_offset + kLEGACY_ENVELOPE_SIZE + self._payload_size + self._xfer_size + 1
        else:
            offset = kENVELOPE_SIZE + self._payload_size + self._xfer_size + self._signer_size
        sig_len = self._tx_size - offset
        return Signature(buffer.get_bytes(self._tx_offset + offset, sig_len))

    def get_sig(self) -> Signature:
        if self._sig:
            return self._sig
        if self._is_legacy:
            offset = kLEGACY_ENVELOPE_SIZE + self._payload_size + self._xfer_size + 1
        else:
            offset = kENVELOPE_SIZE + self._payload_size + self._xfer_size + self._signer_size
        raw_sig = self._canonical[offset:]
        if not raw_sig:
            return None
        return Signature(raw_sig)

    def get_payload(self) -> str:
        if self._is_legacy:
            offset = kNODE_ADDR_BUF_SIZE + self._xfer_size + self._signer_size
        else:
            offset = kENVELOPE_SIZE + self._xfer_size + self._signer_size
        return self.get_canonical()[offset:offset + self._payload_size].decode('utf-8')

    def get_canonical(self) -> bytes:
        return self._canonical

    def get_hex_str(self) -> str or None:
        if not self._canonical:
            return None
        return self._canonical.hex()

    def __str__(self):
        return self.get_hex_str()

    def __bool__(self):
        return self._sig is not None

    def __eq__(self, other):
        return self._sig == other.get_sig()

    def get_xfers_from_raw_blk(self, buffer: InputBuffer) -> list:
        """
        :param buffer: binary buffer holding the Transaction data
        :type buffer: InputBuffer
        :return: list of Transfer objects for this Transaction
        :rtype: list
        """
        if not self._is_legacy:
            start_offset = self._tx_offset + kENVELOPE_SIZE + self._signer_size
        else:
            start_offset = self._tx_offset + kLEGACY_ENVELOPE_SIZE
        return Transfer.get_xfers_from_buffer(buffer, start_offset, self._xfer_size)

    def get_xfers(self) -> list:
        """
        :return: list of Transfer objects for this transaction
        :rtype: list
        """
        buffer = InputBuffer(self._canonical)
        return Transfer.get_xfers_from_buffer(buffer, kENVELOPE_SIZE + self._signer_size, self._xfer_size)

    def get_message_digest(self) -> bytes:
        """
        :return: transaction binary, excluding the signature if one is present.
        :rtype: bytes
        """
        return self._canonical[:kENVELOPE_SIZE + self._signer_size + self._xfer_size + self._payload_size]

    def _pre_signature_init(self, oper: int, signer: Address, xfers: list, payload: bytes, flags: int,
                           timestamp: int):
        # TODO: accommodate serialization for legacy txs
        self._payload_size = len(payload)

        if self._payload_size < kMIN_PAYLOAD_SIZE:
            raise ValueError(f"Failed to serialize transaction, payload too small ({self._payload_size})")

        self._canonical = bytes()
        self._canonical += set_uint64(self._payload_size)

        if set_uint8(oper) >= OpType.NUM_OPS:
            raise ValueError(f"Invalid Transaction: bad OpType ({oper} >= {OpType.NUM_OPS})")
        self._canonical += set_uint8(oper)
        if flags != 0:
            raise ValueError("Invalid Transaction: unknown flags")
        self._canonical += set_uint8(flags)
        self._canonical += set_uint64(timestamp)
        self._canonical += signer.get_canonical()

        self._xfer_size = 0
        for xfer in xfers:
            self._xfer_size += xfer.get_size()
            self._canonical += xfer.get_canonical()

        self._signer_size = signer.get_size()
        self._tx_size = kENVELOPE_SIZE + self._signer_size + self._xfer_size + self._payload_size \
                        + signer.get_corresponding_sig_size()

        self._canonical = set_uint64(self._tx_size) + set_uint64(self._xfer_size) + self._canonical

    def serialize(self, oper: int, xfers: list, payload: str, flags: int,
                  timestamp: int, sig: Signature = None, is_legacy: bool = False):
        """
        Initialize Transaction attributes and generate canonical form.

        :param oper: operation type, as denoted in devv_constants.OpType
        :type oper: int
        :param xfers: list of Transfer objects
        :type xfers: list
        :param payload: Transaction payload
        :type payload: str
        :param flags: tx flags, to be stored as an uint8, typically zero
        :type flags: int
        :param timestamp: time of tx to be stored as an uint64
        :type timestamp: int
        :param sig: signature to assign to this transaction
        :type sig: Signature or str
        :param is_legacy: if True, will follow canonical patterns for legacy blocks
        :type is_legacy: bool
        """
        self._is_legacy = is_legacy
        self._pre_signature_init(oper, self._signer, xfers, payload, flags, timestamp)
        if sig:
            self.set_sig(sig)

    def set_sig(self, sig: Signature or str):
        """
        Add the given signature to the Transaction's current canonical form.
        If the Transaction is initialized with is_legacy = True, the signature size prefix will be excluded.

        :param sig: signature to assign to this transaction
        :type sig: Signature or str
        """
        if not isinstance(sig, Signature):
            self._sig = sig = Signature(sig)
        self._canonical += sig.get_canonical(legacy=self._is_legacy)

    def sign(self, pkey: str, aes_pass: str) -> Signature:
        """
        Signs a Transaction's current canonical form, and appends the signature to its binary data.
        If the Transaction is initialized with is_legacy = True, the signature size prefix will be excluded.

        :param pkey: str of private key, without PEM prefix/suffix or newlines
        :type pkey: str
        :param aes_pass: aes key to decrypt/encrypt the pkey with; this is required
        :type aes_pass: str
        :return: the new signature for the tx
        :rtype: Signature
        """
        digest = self.get_message_digest()
        self._sig = sign_binary(pkey=pkey, pub=self._signer, msg=DevvHash(digest), aes_pass=aes_pass)
        self._canonical = digest + self._sig.get_canonical(self._is_legacy)
        return self._sig

    def from_dict(self, props: dict):
        """
        Initializes a Transaction object from a dictionary. Expects the below keys:

        - 'xfers': list of dicts
            - 'coin': int
            - 'address': str or Address
            - 'amount': int
            - 'delay': int
        - 'op': int or str
        - 'payload': str
        - 'flags': int
        - 'timestamp': int
        - (optional) 'sig': str
        - (optional) 'legacy': bool

        :param props: dict of transaction properties
        :type props: dict
        """
        try:
            # construct xfers
            xfers = [Transfer(xfer) for xfer in props['xfers']]
            if not xfers:
                raise Exception('Invalid Transaction: failed to parse any xfers')
            self._signer = None
            for xfer in xfers:
                if xfer.get_amount() < 0:
                    self._signer = xfer.get_addr()
                    break
            if not self._signer:
                raise Exception('Invalid Transaction: one Transfer must have amount < 0')

            # get payload binary
            payload = bytes(props['payload'], 'utf-8')

            # check operation type
            if isinstance(props['op'], str):
                try:
                    op = OpType().__getattribute__(props['op'])
                except Exception as e:
                    raise Exception(f"Invalid Transaction: bad op string {props['op']}")
            elif props['op'] >= OpType.NUM_OPS:
                raise Exception(f"Invalid Transaction: bad op int {props['op']}")
            else:
                op = props['op']

            # initialize attributes and construct canonical
            self.serialize(op, xfers, payload, props['flags'], props['timestamp'],
                           sig=props.get('sig'), is_legacy=props.get('legacy'))
        except KeyError as ke:
            raise Exception(f"Invalid Transaction: failed to set property ({ke})")

    def get_signer(self) -> Address:
        return self._signer

