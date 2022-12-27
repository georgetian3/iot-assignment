# most of the block comments in this project originate from the Bluetooth Core standard version 5.3

'''

6.1.1 Basic Rate


==================
Entity      Bits
------------------
Access code 68/72
Header      54
Payload     0-2790
==================

A packet may consist of:
• the shortened access code only (see Section 6.5.1.1)
• the access code and the packet header
• the access code, the packet header and the payload.

6.2 Bit ordering

The bit ordering when defining packets and messages in the Baseband
Specification, follows the little-endian format. The following rules apply:
• The least significant bit (LSB) corresponds to ;
• The LSB is the first bit sent over the air;
• In illustrations, the LSB is shown on the left side;
Furthermore, data fields generated internally at Baseband level, such as the
packet header fields and payload header length, shall be transmitted with the
LSB first. For instance, a 3-bit parameter X=3 is sent as:
over the air where 1 is sent first and 0 is sent last.




'''

class BluetoothPacket:
    def __init__(self, data, bd_addr):
        self.bits = self.generate_access_code(bd_addr) + self.generate_packet_header() + self.generate_payload(data)


    def generate_access_code(self, bd_addr):
        """
        6.3 ACCESS CODE
        - Every packet starts with an access code.
        - If a packet header follows, the access code is 72 bits long, otherwise the access code is 68 bits long and is known as a shortened access code.
        - The shortened access code does not contain a trailer.
        - This access code is used for synchronization, DC offset compensation and identification.
        - The access code identifies all packets exchanged on a physical channel: all packets sent in the same physical channel are preceded by the same access code.
        - In the receiver of the device, a sliding correlator correlates against the access code and triggers when a threshold is exceeded. This trigger signal is used to determine the receive timing.
        - The shortened access code is used in paging and inquiry. In this case, the access code itself is used as a signaling message and neither a header nor a payload is present.
        - The access code consists of a preamble, a sync word, and possibly a trailer

        Entity      Bits
        Preamble    4
        Sync word   64
        Trailer     4
        """

        ######################################################################

        # TODO: complete sync_word

        """
        6.3.3 Sync word
        The sync word is a 64-bit code word derived from a 24 bit address (LAP)

        The information sequence is generated by appending 6 bits to the 24 bit LAP
        (step 1). The appended bits are 001101 if the MSB of the LAP equals 0. If the
        MSB of the LAP is 1 the appended bits are 110010 .
        """
        lap = bd_addr[:24]
        information_sequence = lap + ('001101' if lap[-1] == 0 else '110010')

        """
        In step 2 the information is pre-scrambled by XORing it with the bits
        p 34 ...p 63 of the PN sequence (defined in Section 6.3.3.2)
        """

        sync_word = '1' * 64

        """
        6.3.2 Preamble
        The preamble is a fixed zero-one pattern of 4 symbols used to facilitate DC
        compensation. The sequence is either ‘1010’ or ‘0101’ (in transmission order),
        depending on whether the LSB of the following sync word is 1 or 0,
        respectively.
        """

        #####################################################################

        preamble = '1010' if sync_word[0] == 1 else '0101'

        """
        6.3.4 Trailer
        The trailer sequence is either ‘1010’ or ‘0101’ (in transmission order) depending on
        whether the MSB of the sync word is 0 or 1, respectively. 
        """

        trailer = '1010' if sync_word[-1] == '0' else '0101'

        access_code = preamble + sync_word + trailer

        return access_code

    def generate_packet_header(self):

        """
        6.4 PACKET HEADER
        The header contains link control (LC) information and consists of 6 fields:
        • LT_ADDR: 3-bit logical transport address
        • TYPE: 4-bit type code
        • FLOW: 1-bit flow control
        • ARQN: 1-bit acknowledge indication
        • SEQN: 1-bit sequence number
        • HEC: 8-bit header error check
        The total header, including the HEC, consists of 18 bits, see Figure 6.8, and is
        encoded with a rate 1/3 FEC (not shown but described in Section 7.4) resulting
        in a 54-bit header. The LT_ADDR and TYPE fields shall be sent LSB first.
        """

        """
        6.4.1 LT_ADDR
        The 3-bit LT_ADDR field contains the logical transport address for the packet
        (see Section 4.2). 
        """

        lt_addr = '111'

        """
        6.4.2 TYPE
        Sixteen different types of packets can be distinguished. The 4-bit TYPE code
        specifies which packet type is used. The interpretation of the TYPE code
        depends on the logical transport address in the packet. First, it shall be
        determined whether the packet is sent on a SCO logical transport, an eSCO
        logical transport, an ACL logical transport, or a CPB logical transport. Second,
        it shall be determined whether Enhanced Data Rate has been enabled for the
        logical transport (ACL or eSCO) indicated by LT_ADDR. It can then be
        determined which type of SCO packet, eSCO packet, or ACL packet has been
        received. The TYPE code determines how many slots the current packet will
        occupy (see the slot occupancy column in Table 6.2). This allows the non-
        addressed receivers to refrain from listening to the channel for the duration of
        the remaining slots. In Section 6.5, each packet type is described in more
        detail.
        """

        type = '1111111111111111'

        """
        6.4.3 FLOW
        The FLOW bit is used for flow control of packets over the ACL logical transport.
        When the RX buffer for the ACL logical transport in the recipient is full, a STOP
        indication (FLOW=0) shall be returned to stop the other device from
        transmitting data temporarily. The STOP signal only affects ACL packets.
        Packets including only link control information (POLL and NULL packets), SCO
        packets or eSCO packets can still be received. When the RX buffer can accept
        data, a GO indication (FLOW=1) shall be returned. When no packet is
        received, or the received header is in error, a GO shall be assumed implicitly. In
        this case, the Peripheral can receive a new packet with CRC although its RX
        buffer is still not emptied. The Peripheral shall then return a NAK in response to
        this packet even if the packet passed the CRC check.
        The FLOW bit is not used on the eSCO logical transport and shall be set to one
        on transmission and ignored upon receipt. The FLOW bit is reserved for future
        use on the CPB logical transport.
        """

        flow = '1'

        """
        6.4.4 ARQN
        The 1-bit acknowledgment indication ARQN is used to inform the source of a
        successful transfer of payload data with CRC, and can be positive
        acknowledge ACK or negative acknowledge NAK. See Section 7.6 for
        initialization and usage of this bit.
        The ARQN bit is reserved for future use on the CPB logical transport.
        """

        arqn = '0'


        """
        6.4.5 SEQN
        The SEQN bit provides a sequential numbering scheme to order the data
        packet stream. See Section 7.6.2 for initialization and usage of the SEQN bit.
        For Active Peripheral Broadcast packets, a modified sequencing method is
        used, see Section 7.6.5.
        The SEQN bit is reserved for future use on the CPB logical transport.
        """

        seqn = '0'

        """
        6.4.6 HEC
        Each header has a header-error-check to check the header integrity. The HEC
        is an 8-bit word (generation of the HEC is specified in Section 7.1.1). Before
        generating the HEC, the HEC generator is initialized with an 8-bit value. For
        FHS packets sent in Central Response substate, the Peripheral upper address
        part (UAP) shall be used. For FHS packets and extended inquiry response
        packets sent in Inquiry Response substate, the default check initialization (DCI,
        see Section 1.2.1) shall be used. In all other cases, the UAP of the Central
        shall be used.
        After the initialization, a HEC shall be calculated for the 10 header bits. Before
        checking the HEC, the receiver shall initialize the HEC check circuitry with the
        proper 8-bit UAP (or DCI). If the HEC does not check, the entire packet shall be
        discarded. More information can be found in Section 7.1.
        """

        hec = '11111111'

        packet_header = lt_addr + type + flow + arqn + seqn + hec

        return packet_header

    def generate_payload(self, data):
        MAX_LEN = 2 ** 10 - 1
        assert(len(data) <= MAX_LEN)
        llid = '11'
        flow = '1'
        length = str(bin(len(data)))[2:][::-1]


        payload_header =  llid + flow + length

        data = data.encode('utf8')
        payload = payload_header + data

        return payload