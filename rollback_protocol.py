from pydantic import BaseModel
from typing import List, Callable, Dict, Optional
from enum import Enum
from uuid import uuid4
import time

class ResourceType(str, Enum):
    DOCKER_CONTAINER = "docker_container"
    PORT_BINDING = "port_binding"
    VOLUME = "volume"
    NETWORK = "network"
    PROCESS = "process"

class ResourceAllocation(BaseModel):
    """Represents an allocated infrastructure resource with its compensation action"""
    resource_id: str
    resource_type: ResourceType
    metadata: Dict = {}
    created_at: float = time.time()
    compensation_action: Optional[Callable[[], None]] = None

    class Config:
        arbitrary_types_allowed = True

class RollbackSaga(BaseModel):
    """
    Compensation-based rollback using Saga pattern.
    Guarantees cleanup even on partial failures.
    """
    saga_id: str
    allocations: List[ResourceAllocation] = []
    status: str = "active"   # active, committed, rolled_back
    created_at: float = time.time()

    def register(self, allocation: ResourceAllocation):
        """Register a new resource that needs compensation on failure"""
        self.allocations.append(allocation)
        print(f"[Saga {self.saga_id}] Registered: {allocation.resource_type} → {allocation.resource_id}")

    def commit(self):
        """Mark saga as successfully completed (no rollback needed)"""
        self.status = "committed"
        print(f"[Saga {self.saga_id}] Committed successfully. No rollback required.")

    def rollback(self):
        """
        Execute compensation actions in reverse order (LIFO).
        This is the core of the graceful rollback protocol.
        """
        if self.status == "rolled_back":
            return

        print(f"[Saga {self.saga_id}] Starting rollback of {len(self.allocations)} resources...")

        # Reverse order = proper cleanup (containers before networks, etc.)
        for alloc in reversed(self.allocations):
            if alloc.compensation_action:
                try:
                    print(f"  → Rolling back {alloc.resource_type}: {alloc.resource_id}")
                    alloc.compensation_action()
                except Exception as e:
                    print(f"  ⚠️ Compensation failed for {alloc.resource_id}: {e}")

        self.status = "rolled_back"
        self.allocations.clear()
        print(f"[Saga {self.saga_id}] Rollback completed.")

    def get_status(self) -> Dict:
        return {
            "saga_id": self.saga_id,
            "status": self.status,
            "resources_allocated": len(self.allocations),
            "age_seconds": time.time() - self.created_at
        }


# Example usage for Docker + PostgreSQL failure scenario
def create_docker_saga_example():
    """Example of how to use the rollback protocol"""
    saga = RollbackSaga(saga_id=str(uuid4()))

    # Simulate registering a Docker container
    def mock_remove_container():
        print("   [Compensation] Docker container removed")

    saga.register(ResourceAllocation(
        resource_id="postgres_container_abc123",
        resource_type=ResourceType.DOCKER_CONTAINER,
        metadata={"image": "postgres:15", "port": 5432},
        compensation_action=mock_remove_container
    ))

    # Simulate port binding
    def mock_release_port():
        print("   [Compensation] Port 5432 released")

    saga.register(ResourceAllocation(
        resource_id="port_5432",
        resource_type=ResourceType.PORT_BINDING,
        metadata={"port": 5432},
        compensation_action=mock_release_port
    ))

    return saga
