from abc import ABC, abstractmethod

# ---------- Abstract domain layer ----------
class Vehicle(ABC):
    """Generic vehicle – riders never book this directly."""
    def __init__(self, vehicle_id: str, base_fare: float):
        self.vehicle_id = vehicle_id
        self.base_fare = base_fare

    @abstractmethod
    def calculate_fare(self, distance_km: float) -> float:
        """Every concrete vehicle must decide how fares are computed."""
        ...

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.vehicle_id})"


# ---------- Concrete specialisations (Inheritance + Polymorphism) ----------
class Car(Vehicle):
    def calculate_fare(self, distance_km):
        return self.base_fare + distance_km * 15    # ₹15/km

class Bike(Vehicle):
    def calculate_fare(self, distance_km):
        return self.base_fare + distance_km * 7     # ₹7/km

class Auto(Vehicle):
    def calculate_fare(self, distance_km):
        return self.base_fare + distance_km * 10    # ₹10/km


# ---------- People in the system ----------
class Person(ABC):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Rider(Person):
    """Wallet balance is private → Encapsulation."""
    def __init__(self, name: str):
        super().__init__(name)
        self.__wallet = 0.0       # double-underscore makes it 'pseudo‑private'

    def add_funds(self, amount: float):
        self.__wallet += amount
        print(f"{self.name}'s wallet balance: ₹{self.__wallet}")

    def _can_pay(self, amount: float) -> bool:
        return self.__wallet >= amount

    def pay(self, amount: float) -> bool:
        if self._can_pay(amount):
            self.__wallet -= amount
            print(f"₹{amount} deducted from {self.name}. Remaining: ₹{self.__wallet}")
            return True
        print("Insufficient balance!")
        return False

    def get_wallet_balance(self) -> float:
        return self.__wallet      # read‑only access from outside


class Driver(Person):
    def __init__(self, name: str, vehicle: Vehicle):
        super().__init__(name)
        self.vehicle = vehicle
        self.rating = 5.0         # could be refined later


# ---------- Ride lifecycle (Composition) ----------
class RideStatus:
    REQUESTED, ONGOING, COMPLETED, CANCELLED = range(4)


class Ride:
    """
    A Ride is *composed* of:
    - one Rider
    - one Driver (who owns a Vehicle)
    """
    def __init__(self, rider: Rider, driver: Driver, distance_km: float):
        self.rider = rider
        self.driver = driver
        self.distance = distance_km
        self.status = RideStatus.REQUESTED

        # Fare is private – outside code can only use get_fare()
        self.__fare = self.driver.vehicle.calculate_fare(distance_km)

    # ---------------- Ride actions ----------------
    def start(self):
        if self.status == RideStatus.REQUESTED:
            self.status = RideStatus.ONGOING
            print(f"Ride started with {self.driver} in {self.driver.vehicle}")

    def end(self):
        if self.status == RideStatus.ONGOING:
            self.status = RideStatus.COMPLETED
            print(
                f"Ride ended • Distance: {self.distance} km • Fare: ₹{self.__fare}"
            )
            if self.rider.pay(self.__fare):
                print("Payment succeeded ✅")
            else:
                print("Payment failed ❌")

    # ---------------- Safe accessors ----------------
    def get_fare(self) -> float:
        return self.__fare


# ---------- Quick demo / unit test ----------
if __name__ == "__main__":
    # Create a rider, top up wallet (encapsulation in action)
    rider = Rider("Anita")
    rider.add_funds(500)

    # Driver with a Car
    driver = Driver("Ravi", Car("KA‑01‑AB‑1234", base_fare=50))

    # Rider books the ride
    ride = Ride(rider, driver, distance_km=12.3)
    print(f"Calculated fare (safe accessor): ₹{ride.get_fare()}\n")

    # Lifecycle
    ride.start()
    ride.end()
