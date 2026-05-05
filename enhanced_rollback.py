"""
Enhanced Rollback Management using Saga Pattern (Vector 3)
Provides safe infrastructure management with automatic cleanup on failure.
"""

from rollback_protocol import RollbackSaga, ResourceAllocation, ResourceType
from typing import Optional, Callable, Dict
from uuid import uuid4

active_sagas: Dict[str, RollbackSaga] = {}

def create_saga() -> RollbackSaga:
    """Create a new rollback saga for infrastructure operations"""
    saga = RollbackSaga(saga_id=str(uuid4()))
    active_sagas[saga.saga_id] = saga
    return saga

def register_docker_container(
    saga: RollbackSaga,
    container_id: str,
    remove_function: Callable[[], None]
):
    """Register a Docker container that should be cleaned up on failure"""
    saga.register(ResourceAllocation(
        resource_id=container_id,
        resource_type=ResourceType.DOCKER_CONTAINER,
        metadata={"type": "docker"},
        compensation_action=remove_function
    ))

def register_port_binding(
    saga: RollbackSaga,
    port: int,
    release_function: Callable[[], None]
):
    """Register a port binding that should be released on failure"""
    saga.register(ResourceAllocation(
        resource_id=f"port_{port}",
        resource_type=ResourceType.PORT_BINDING,
        metadata={"port": port},
        compensation_action=release_function
    ))

def register_volume(
    saga: RollbackSaga,
    volume_name: str,
    remove_function: Callable[[], None]
):
    """Register a Docker volume"""
    saga.register(ResourceAllocation(
        resource_id=volume_name,
        resource_type=ResourceType.VOLUME,
        metadata={"volume": volume_name},
        compensation_action=remove_function
    ))

def commit_saga(saga_id: str):
    """Mark saga as successful (prevents rollback)"""
    if saga_id in active_sagas:
        active_sagas[saga_id].commit()
        del active_sagas[saga_id]

def rollback_saga(saga_id: str):
    """Manually trigger rollback"""
    if saga_id in active_sagas:
        active_sagas[saga_id].rollback()
        del active_sagas[saga_id]

def get_active_sagas() -> Dict:
    return {sid: saga.get_status() for sid, saga in active_sagas.items()}


# Example usage pattern for your infrastructure code
def example_infrastructure_with_rollback():
    """
    Recommended pattern when doing Docker / infrastructure work.
    """
    saga = create_saga()
    
    try:
        # Example: Start a container
        # container = docker_client.containers.run(...)
        # register_docker_container(saga, container.id, lambda: container.remove(force=True))
        
        # Do more work...
        # If anything fails here, call rollback_saga(saga.saga_id)
        
        commit_saga(saga.saga_id)   # Success path
        return saga.saga_id
        
    except Exception as e:
        print(f"Infrastructure failed: {e}")
        rollback_saga(saga.saga_id)
        raise
