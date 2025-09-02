"""
Serialization-safe wrapper to prevent circular references in Prefect workflows.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class SerializationSafeWrapper:
    """
    A wrapper that prevents objects with potential circular references 
    from being serialized by Prefect's parameter serialization.
    """
    
    def __init__(self, wrapped_object: Any, identifier: str = "wrapped_object"):
        """
        Initialize the wrapper.
        
        Args:
            wrapped_object: The object to wrap (should not be serialized)
            identifier: String identifier for logging/debugging
        """
        self._wrapped_object = wrapped_object
        self._identifier = identifier
    
    def __getattr__(self, name):
        """Delegate attribute access to the wrapped object."""
        return getattr(self._wrapped_object, name)
    
    def __repr__(self):
        """String representation that's safe for serialization."""
        return f"SerializationSafeWrapper({self._identifier})"
    
    def __str__(self):
        """String representation that's safe for serialization."""
        return f"SerializationSafeWrapper({self._identifier})"
    
    def __bool__(self):
        """Boolean evaluation of wrapped object."""
        return bool(self._wrapped_object)
    
    def __getstate__(self):
        """
        Custom getstate that prevents serialization of the wrapped object.
        Returns only the identifier to prevent circular references.
        """
        logger.warning(f"SerializationSafeWrapper({self._identifier}) being serialized - this may indicate a Prefect serialization issue")
        return {
            '_identifier': self._identifier,
            '_wrapped_object': None  # Don't serialize the actual object
        }
    
    def __setstate__(self, state):
        """Restore from serialization with None wrapped object."""
        self.__dict__.update(state)
        logger.warning(f"SerializationSafeWrapper({self._identifier}) restored from serialization with None wrapped object")
    
    def __dict__(self):
        """
        Override __dict__ to provide safe serializable representation.
        This prevents FastAPI's jsonable_encoder from accessing problematic attributes.
        """
        return {
            '_identifier': self._identifier,
            '_serialization_safe': True,
            '_wrapped_available': self._wrapped_object is not None
        }
    
    def keys(self):
        """Provide keys method for dict-like access."""
        return ['_identifier', '_serialization_safe', '_wrapped_available']
    
    def items(self):
        """Provide items method for dict-like access.""" 
        return [
            ('_identifier', self._identifier),
            ('_serialization_safe', True),
            ('_wrapped_available', self._wrapped_object is not None)
        ]
    
    def get_wrapped_object(self):
        """Get the wrapped object directly."""
        return self._wrapped_object
    
    def is_available(self):
        """Check if the wrapped object is available (not None)."""
        return self._wrapped_object is not None


def make_serialization_safe(obj: Any, identifier: str = "object") -> SerializationSafeWrapper:
    """
    Create a serialization-safe wrapper around an object.
    
    Args:
        obj: Object to wrap
        identifier: String identifier for debugging
        
    Returns:
        SerializationSafeWrapper instance
    """
    return SerializationSafeWrapper(obj, identifier)