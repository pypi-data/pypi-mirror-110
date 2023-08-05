"""
Implements a Static Priority (SP) server.
"""

from collections import defaultdict as dd

import simpy
from ns.packet.packet import Packet


class SPServer:
    """
    Parameters
    ----------
    env: simpy.Environment
        The simulation environment.
    rate: float
        The bit rate of the port.
    priorities: list
        A list of priorities for each possible flow_id. We assume a simple assignment
        of flow ids to priorities, i.e., flow_id = 0 corresponds to priorities[0], etc.
    zero_buffer: bool
        Does this server have a zero-length buffer? This is useful when multiple
        basic elements need to be put together to construct a more complex element
        with a unified buffer.
    zero_downstream_buffer: bool
        Does this server's downstream element has a zero-length buffer? If so, packets
        may queue up in this element's own buffer rather than be forwarded to the
        next-hop element.
    debug: bool
        Print more verbose debug information.
    """
    def __init__(self,
                 env,
                 rate,
                 priorities,
                 zero_buffer=False,
                 zero_downstream_buffer=False,
                 debug=False) -> None:
        self.env = env
        self.rate = rate
        self.prio = priorities

        self.stores = {}
        self.prio_queue_count = [0 for i in range(len(priorities))]

        self.packets_available = simpy.Store(self.env)

        self.current_packet = None

        self.byte_sizes = dd(lambda: 0)

        self.packets_received = 0
        self.out = None
        self.upstream_updates = {}
        self.upstream_stores = {}
        self.zero_buffer = zero_buffer
        self.zero_downstream_buffer = zero_downstream_buffer
        if self.zero_downstream_buffer:
            self.downstream_stores = {}

        self.debug = debug
        self.action = env.process(self.run())

    def update(self, packet):
        """The packet has just been retrieved from this element's own buffer, so
        update internal housekeeping states accordingly."""
        if self.zero_buffer:
            self.upstream_stores[packet].get()
            del self.upstream_stores[packet]
            self.upstream_updates[packet](packet)
            del self.upstream_updates[packet]

        if self.debug:
            print(f"Sent out packet {packet.id} of priority {packet.prio}")

        self.prio_queue_count[packet.prio] -= 1

        if packet.flow_id in self.byte_sizes:
            self.byte_sizes[packet.flow_id] -= packet.size
        else:
            raise ValueError("Error: the packet is from an unrecorded flow.")

    def packet_in_service(self) -> Packet:
        """Returns the packet that is currently being sent to the downstream element.
        Used by a ServerMonitor.
        """
        return self.current_packet

    def byte_size(self, flow_id) -> int:
        """Returns the size of the queue for a particular flow_id, in bytes.
        Used by a ServerMonitor.
        """
        if flow_id in self.byte_sizes:
            return self.byte_sizes[flow_id]
        else:
            return 0

    def size(self, flow_id) -> int:
        """Returns the size of the queue for a particular flow_id, in the
        number of packets. Used by a ServerMonitor.
        """
        if flow_id in self.stores:
            return len(self.stores[flow_id].items)
        else:
            return 0

    def run(self):
        """The generator function used in simulations."""
        while True:
            for prio, count in enumerate(self.prio_queue_count):
                if count > 0:
                    if self.zero_downstream_buffer:
                        ds_store = self.downstream_stores[prio]
                        packet = yield ds_store.get()
                        packet.prio = prio

                        self.current_packet = packet
                        yield self.env.timeout(packet.size * 8.0 / self.rate)

                        self.out.put(packet,
                                     upstream_update=self.update,
                                     upstream_store=self.stores[prio])
                        self.current_packet = None
                    else:
                        store = self.stores[prio]
                        packet = yield store.get()
                        packet.prio = prio
                        self.update(packet)

                        self.current_packet = packet
                        yield self.env.timeout(packet.size * 8.0 / self.rate)
                        self.out.put(packet)
                        self.current_packet = None

                    break

            if sum(self.prio_queue_count) == 0:
                yield self.packets_available.get()

    def put(self, packet, upstream_update=None, upstream_store=None):
        """ Sends the packet 'pkt' to this element. """
        self.packets_received += 1
        self.byte_sizes[packet.flow_id] += packet.size

        if sum(self.prio_queue_count) == 0:
            self.packets_available.put(True)

        prio = self.prio[packet.flow_id]
        self.prio_queue_count[prio] += 1

        if self.debug:
            print(
                f"Time {self.env.now}, flow_id {packet.flow_id}, packet_id {packet.id}"
            )

        if not prio in self.stores:
            self.stores[prio] = simpy.Store(self.env)

            if self.zero_downstream_buffer:
                self.downstream_stores[prio] = simpy.Store(self.env)

        if self.zero_buffer and upstream_update is not None and upstream_store is not None:
            self.upstream_stores[packet] = upstream_store
            self.upstream_updates[packet] = upstream_update

        if self.zero_downstream_buffer:
            self.downstream_stores[prio].put(packet)

        return self.stores[prio].put(packet)
