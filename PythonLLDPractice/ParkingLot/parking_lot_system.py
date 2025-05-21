# Enums and Vehicle
from enum import Enum
from datetime import datetime
from typing import List, Optional
import heapq
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger('parking_system')
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'parking_system.log')

    # File handler with rotation (max 5MB per file, keep 3 backup files)
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create simplified formatter with only date, time, function name, and message
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(message)s')

    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = None


class VehicleType(Enum):
    TwoWheeler = 1
    FourWheeler = 2


class Vehicle:
    def __init__(self, vehicle_no: int, vehicle_type: VehicleType):
        logger.info(f"Creating vehicle with number {vehicle_no} of type {vehicle_type.name}")
        self.vehicle_no = vehicle_no
        self.vehicle_type = vehicle_type


# Parking Spot
class ParkingSpot:
    def __init__(self, spot_id: int, price: int):
        logger.info(f"Creating parking spot with ID {spot_id} and price {price}")
        self.id = spot_id
        self.price = price
        self.vehicle: Optional[Vehicle] = None

    def is_empty(self) -> bool:
        logger.info(f"Checking if spot {self.id} is empty")
        return self.vehicle is None

    def park_vehicle(self, vehicle: Vehicle):
        logger.info(f"Parking vehicle {vehicle.vehicle_no} in spot {self.id}")
        self.vehicle = vehicle

    def remove_vehicle(self):
        if self.vehicle:
            logger.info(f"Removing vehicle {self.vehicle.vehicle_no} from spot {self.id}")
        else:
            logger.warning(f"Attempting to remove vehicle from empty spot {self.id}")
        self.vehicle = None

    def __lt__(self, other):
        # Add logging for comparisons
        logger.debug(f"Comparing spot {self.id} with spot {other.id}")
        return self.id < other.id


# Abstract Spot Manager with heapq (Strategy + DI + Template pattern)
class ParkingSpotManager:
    def __init__(self, spots: List[ParkingSpot]):
        logger.info(f"Initializing with {len(spots)} spots")
        self.spot_heap = [spot for spot in spots if spot.is_empty()]
        heapq.heapify(self.spot_heap)
        self.spots = spots
        logger.info(f"Initialized with {len(self.spot_heap)} available spots")

    def find_parking_space(self) -> Optional[ParkingSpot]:
        logger.info(f" finding parking space ...")
        while self.spot_heap:
            spot = heapq.heappop(self.spot_heap)
            if spot.is_empty():
                logger.info(f"found empty spot {spot.id}")
                return spot
        logger.warning(f"no parking spots available!")
        return None

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        logger.info(f"Attempting to park vehicle {vehicle.vehicle_no}")
        spot = self.find_parking_space()
        if spot:
            spot.park_vehicle(vehicle)
            logger.info(f"Successfully parked vehicle {vehicle.vehicle_no} in spot {spot.id}")
        else:
            logger.warning(f"Failed to park vehicle {vehicle.vehicle_no}, no spots available")
        return spot

    def remove_vehicle(self, vehicle: Vehicle):
        logger.info(f"Removing vehicle {vehicle.vehicle_no}")
        removed = False
        for spot in self.spots:
            if spot.vehicle and spot.vehicle.vehicle_no == vehicle.vehicle_no:
                spot.remove_vehicle()
                heapq.heappush(self.spot_heap, spot)
                logger.info(f"Vehicle {vehicle.vehicle_no} removed from spot {spot.id}")
                removed = True
                break

        if not removed:
            logger.warning(f"Vehicle {vehicle.vehicle_no} not found in any spot")


class TwoWheelerManager(ParkingSpotManager):
    def __init__(self, spots: List[ParkingSpot]):
        logger.info("Creating TwoWheelerManager")
        super().__init__(spots)


class FourWheelerManager(ParkingSpotManager):
    def __init__(self, spots: List[ParkingSpot]):
        logger.info("Creating FourWheelerManager")
        super().__init__(spots)


# Factory pattern
class ParkingSpotManagerFactory:
    def get_manager(self, vehicle_type: VehicleType, spots: List[ParkingSpot]) -> ParkingSpotManager:
        logger.info(f"Factory creating manager for {vehicle_type.name}")
        if vehicle_type == VehicleType.TwoWheeler:
            return TwoWheelerManager(spots)
        else:
            return FourWheelerManager(spots)


# Ticket and Billing
class Ticket:
    def __init__(self, vehicle: Vehicle, parking_spot: ParkingSpot):
        logger.info(f"Creating ticket for vehicle {vehicle.vehicle_no} at spot {parking_spot.id}")
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.entry_time = datetime.now()
        self.exit_time: Optional[datetime] = None
        logger.info(f"Ticket issued for vehicle {vehicle.vehicle_no} at {self.entry_time}")

    def close_ticket(self):
        self.exit_time = datetime.now()
        duration = self.exit_time - self.entry_time
        hours = duration.total_seconds() / 3600
        logger.info(f"Ticket closed for vehicle {self.vehicle.vehicle_no}. Duration: {hours:.2f} hours")


class BillingService:
    def calculate_fees(self, ticket: Ticket) -> int:
        logger.info(f"Calculating fees for vehicle {ticket.vehicle.vehicle_no}")
        ticket.close_ticket()
        duration_hours = max(1, int((ticket.exit_time - ticket.entry_time).total_seconds() // 3600))
        fees = duration_hours * ticket.parking_spot.price
        logger.info(
            f"Fees for vehicle {ticket.vehicle.vehicle_no}: {fees} (duration: {duration_hours} hours, rate: {ticket.parking_spot.price})")
        return fees


# Ticket Service
class TicketService:
    def __init__(self):
        logger.info("Initializing TicketService")
        self.active_tickets = {}

    def generate_ticket(self, vehicle: Vehicle, spot: ParkingSpot) -> Ticket:
        logger.info(f"Generating ticket for vehicle {vehicle.vehicle_no}")
        ticket = Ticket(vehicle, spot)
        self.active_tickets[vehicle.vehicle_no] = ticket
        logger.info(f"Active tickets count: {len(self.active_tickets)}")
        return ticket

    def close_ticket(self, vehicle_no: int) -> Optional[Ticket]:
        logger.info(f"Closing ticket for vehicle {vehicle_no}")
        ticket = self.active_tickets.pop(vehicle_no, None)
        if ticket:
            logger.info(f"Ticket found and closed for vehicle {vehicle_no}")
        else:
            logger.warning(f"No active ticket found for vehicle {vehicle_no}")
        logger.info(f"Remaining active tickets: {len(self.active_tickets)}")
        return ticket


# Entrance and Exit Gate (uses DI)
class EntranceGate:
    def __init__(self, factory: ParkingSpotManagerFactory, ticket_service: TicketService):
        logger.info("Initializing EntranceGate")
        self.factory = factory
        self.ticket_service = ticket_service

    def allow_entry(self, vehicle: Vehicle, spots: List[ParkingSpot]) -> Optional[Ticket]:
        logger.info(f"EntranceGate processing entry for vehicle {vehicle.vehicle_no}")
        manager = self.factory.get_manager(vehicle.vehicle_type, spots)
        spot = manager.park_vehicle(vehicle)
        if not spot:
            logger.warning(f"EntranceGate denied entry to vehicle {vehicle.vehicle_no} - no spot available")
            return None

        ticket = self.ticket_service.generate_ticket(vehicle, spot)
        logger.info(f"EntranceGate allowed entry to vehicle {vehicle.vehicle_no} at spot {spot.id}")
        return ticket


class ExitGate:
    def __init__(self, factory: ParkingSpotManagerFactory, billing_service: BillingService,
                 ticket_service: TicketService):
        logger.info("Initializing ExitGate")
        self.factory = factory
        self.billing_service = billing_service
        self.ticket_service = ticket_service

    def process_exit(self, vehicle: Vehicle, spots: List[ParkingSpot]) -> Optional[int]:
        logger.info(f"ExitGate processing exit for vehicle {vehicle.vehicle_no}")
        ticket = self.ticket_service.close_ticket(vehicle.vehicle_no)
        if not ticket:
            logger.warning(f"ExitGate denied exit to vehicle {vehicle.vehicle_no} - no active ticket found")
            return None

        manager = self.factory.get_manager(vehicle.vehicle_type, spots)
        manager.remove_vehicle(vehicle)

        fees = self.billing_service.calculate_fees(ticket)
        logger.info(f"ExitGate allowed exit to vehicle {vehicle.vehicle_no} with fees {fees}")
        return fees


# Parking Lot Aggregator (Facade pattern)
class ParkingLot:
    def __init__(self, two_wheeler_spots: List[ParkingSpot], four_wheeler_spots: List[ParkingSpot]):
        logger.info(
            f"Initializing ParkingLot with {len(two_wheeler_spots)} two-wheeler spots and {len(four_wheeler_spots)} four-wheeler spots")
        self.two_wheeler_spots = two_wheeler_spots
        self.four_wheeler_spots = four_wheeler_spots
        self.factory = ParkingSpotManagerFactory()
        self.ticket_service = TicketService()
        self.billing_service = BillingService()
        self.entrance_gate = EntranceGate(self.factory, self.ticket_service)
        self.exit_gate = ExitGate(self.factory, self.billing_service, self.ticket_service)
        logger.info("ParkingLot system initialized and ready")

    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        logger.info(f"ParkingLot processing parking request for vehicle {vehicle.vehicle_no}")
        if vehicle.vehicle_type == VehicleType.TwoWheeler:
            logger.info(f"Routing two-wheeler {vehicle.vehicle_no} to two-wheeler spots")
            return self.entrance_gate.allow_entry(vehicle, self.two_wheeler_spots)
        logger.info(f"Routing four-wheeler {vehicle.vehicle_no} to four-wheeler spots")
        return self.entrance_gate.allow_entry(vehicle, self.four_wheeler_spots)

    def release_vehicle(self, vehicle: Vehicle) -> Optional[int]:
        logger.info(f"ParkingLot processing exit request for vehicle {vehicle.vehicle_no}")
        if vehicle.vehicle_type == VehicleType.TwoWheeler:
            logger.info(f"Processing two-wheeler {vehicle.vehicle_no} exit")
            return self.exit_gate.process_exit(vehicle, self.two_wheeler_spots)
        logger.info(f"Processing four-wheeler {vehicle.vehicle_no} exit")
        return self.exit_gate.process_exit(vehicle, self.four_wheeler_spots)


# Example Usage
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Starting parking lot application")
    logger.info("Creating parking spots")

    two_wheeler_spots = [ParkingSpot(i, 10) for i in range(1, 11)]
    print(f"two_wheeler_spots: {two_wheeler_spots}")
    four_wheeler_spots = [ParkingSpot(i, 20) for i in range(11, 21)]
    print(f"four_wheeler_spots: {four_wheeler_spots}")

    logger.info("Setting up parking lot")
    lot = ParkingLot(two_wheeler_spots, four_wheeler_spots)

    logger.info("Creating test vehicles")
    v1 = Vehicle(101, VehicleType.TwoWheeler)
    v2 = Vehicle(202, VehicleType.FourWheeler)

    logger.info("Testing parking")
    ticket1 = lot.park_vehicle(v1)
    ticket2 = lot.park_vehicle(v2)

    logger.info("Simulating time passing")
    import time

    time.sleep(2)

    logger.info("Testing vehicle release")
    fees1 = lot.release_vehicle(v1)
    fees2 = lot.release_vehicle(v2)

    logger.info(f"Vehicle 101 fees: {fees1}")
    logger.info(f"Vehicle 202 fees: {fees2}")

    logger.info("Application test completed")