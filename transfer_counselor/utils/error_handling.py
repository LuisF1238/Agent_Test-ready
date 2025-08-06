#!/usr/bin/env python3
"""
Comprehensive Error Handling and Recovery System
Provides robust error handling, retry mechanisms, and recovery strategies
"""

import logging
import time
import uuid
from typing import Dict, Any, List, Optional, Callable, Union, Type
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import traceback
import json
from functools import wraps
import threading

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RecoveryStrategy(Enum):
    """Recovery strategies for different error types"""
    RETRY = "retry"
    FALLBACK = "fallback"
    ESCALATE = "escalate"
    IGNORE = "ignore"
    CIRCUIT_BREAK = "circuit_break"

@dataclass
class ErrorContext:
    """Context information for an error"""
    error_id: str
    timestamp: datetime
    error_type: str
    error_message: str
    stack_trace: str
    severity: ErrorSeverity
    component: str
    operation: str
    session_id: Optional[str]
    user_id: Optional[str]
    context_data: Dict[str, Any]
    recovery_attempts: int
    recovery_strategy: Optional[RecoveryStrategy] = None

@dataclass
class RetryConfig:
    """Configuration for retry mechanisms"""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    backoff_strategy: str = "exponential"  # exponential, linear, fixed

class CircuitBreakerState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, requests rejected
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5
    recovery_timeout: int = 60
    success_threshold: int = 3
    timeout: float = 30.0

class CircuitBreaker:
    """Circuit breaker for handling cascading failures"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        with self.lock:
            if self.state == CircuitBreakerState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitBreakerState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitBreakerOpenError(f"Circuit breaker {self.name} is OPEN")
            
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                if execution_time > self.config.timeout:
                    raise TimeoutError(f"Operation timed out after {execution_time:.2f}s")
                
                self._on_success()
                return result
                
            except Exception as e:
                self._on_failure()
                raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt to reset"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.config.recovery_timeout
    
    def _on_success(self):
        """Handle successful execution"""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
        elif self.state == CircuitBreakerState.CLOSED:
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed execution"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitBreakerState.OPEN

class CircuitBreakerOpenError(Exception):
    """Exception raised when circuit breaker is open"""
    pass

class ErrorHandler:
    """Comprehensive error handling system"""
    
    def __init__(self):
        self.error_registry: Dict[str, ErrorContext] = {}
        self.error_handlers: Dict[Type[Exception], Callable] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.fallback_handlers: Dict[str, Callable] = {}
        self.error_patterns: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        
        # Setup default error handlers
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Setup default error handlers for common exceptions"""
        self.register_error_handler(ConnectionError, self._handle_connection_error)
        self.register_error_handler(TimeoutError, self._handle_timeout_error)
        self.register_error_handler(ValueError, self._handle_validation_error)
        self.register_error_handler(KeyError, self._handle_key_error)
        self.register_error_handler(Exception, self._handle_generic_error)
    
    def register_error_handler(self, exception_type: Type[Exception], handler: Callable):
        """Register a custom error handler for specific exception types"""
        self.error_handlers[exception_type] = handler
        logger.info(f"Registered error handler for {exception_type.__name__}")
    
    def register_circuit_breaker(self, name: str, config: CircuitBreakerConfig):
        """Register a circuit breaker"""
        self.circuit_breakers[name] = CircuitBreaker(name, config)
        logger.info(f"Registered circuit breaker: {name}")
    
    def register_fallback_handler(self, operation: str, handler: Callable):
        """Register a fallback handler for specific operations"""
        self.fallback_handlers[operation] = handler
        logger.info(f"Registered fallback handler for operation: {operation}")
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorContext:
        """Handle an error with appropriate recovery strategy"""
        import uuid
        
        error_id = str(uuid.uuid4())
        error_context = ErrorContext(
            error_id=error_id,
            timestamp=datetime.now(),
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            severity=self._determine_severity(error),
            component=context.get('component', 'unknown') if context else 'unknown',
            operation=context.get('operation', 'unknown') if context else 'unknown',
            session_id=context.get('session_id') if context else None,
            user_id=context.get('user_id') if context else None,
            context_data=context or {},
            recovery_attempts=0
        )
        
        # Store error context
        with self.lock:
            self.error_registry[error_id] = error_context
        
        # Log the error
        self._log_error(error_context)
        
        # Determine recovery strategy
        recovery_strategy = self._determine_recovery_strategy(error, error_context)
        error_context.recovery_strategy = recovery_strategy
        
        # Execute recovery strategy
        return self._execute_recovery_strategy(error, error_context)
    
    def _determine_severity(self, error: Exception) -> ErrorSeverity:
        """Determine error severity based on exception type"""
        if isinstance(error, (ConnectionError, TimeoutError)):
            return ErrorSeverity.HIGH
        elif isinstance(error, (ValueError, KeyError, TypeError)):
            return ErrorSeverity.MEDIUM
        elif isinstance(error, CircuitBreakerOpenError):
            return ErrorSeverity.CRITICAL
        else:
            return ErrorSeverity.LOW
    
    def _determine_recovery_strategy(self, error: Exception, context: ErrorContext) -> RecoveryStrategy:
        """Determine appropriate recovery strategy"""
        # Check for specific patterns
        for pattern in self.error_patterns:
            if self._matches_pattern(error, context, pattern):
                return RecoveryStrategy(pattern['strategy'])
        
        # Default strategies based on error type
        if isinstance(error, (ConnectionError, TimeoutError)):
            return RecoveryStrategy.RETRY
        elif isinstance(error, CircuitBreakerOpenError):
            return RecoveryStrategy.FALLBACK
        elif context.severity == ErrorSeverity.CRITICAL:
            return RecoveryStrategy.ESCALATE
        else:
            return RecoveryStrategy.RETRY
    
    def _matches_pattern(self, error: Exception, context: ErrorContext, pattern: Dict[str, Any]) -> bool:
        """Check if error matches a specific pattern"""
        # Check error type
        if 'error_type' in pattern and not isinstance(error, pattern['error_type']):
            return False
        
        # Check message pattern
        if 'message_pattern' in pattern:
            import re
            if not re.search(pattern['message_pattern'], str(error)):
                return False
        
        # Check component
        if 'component' in pattern and context.component != pattern['component']:
            return False
        
        return True
    
    def _execute_recovery_strategy(self, error: Exception, context: ErrorContext) -> ErrorContext:
        """Execute the recovery strategy"""
        strategy = context.recovery_strategy
        
        if strategy == RecoveryStrategy.RETRY:
            # Retry will be handled by the retry decorator
            pass
        elif strategy == RecoveryStrategy.FALLBACK:
            self._execute_fallback(context)
        elif strategy == RecoveryStrategy.ESCALATE:
            self._escalate_error(context)
        elif strategy == RecoveryStrategy.CIRCUIT_BREAK:
            self._trigger_circuit_breaker(context)
        
        return context
    
    def _execute_fallback(self, context: ErrorContext):
        """Execute fallback handler"""
        operation = context.operation
        if operation in self.fallback_handlers:
            try:
                self.fallback_handlers[operation](context)
                logger.info(f"Executed fallback for operation: {operation}")
            except Exception as e:
                logger.error(f"Fallback failed for operation {operation}: {e}")
    
    def _escalate_error(self, context: ErrorContext):
        """Escalate error to higher level"""
        logger.critical(f"Escalating error: {context.error_id} - {context.error_message}")
        # This could send alerts, notifications, etc.
    
    def _trigger_circuit_breaker(self, context: ErrorContext):
        """Trigger circuit breaker for the component"""
        component = context.component
        if component in self.circuit_breakers:
            # Circuit breaker will handle the logic
            pass
    
    def _log_error(self, context: ErrorContext):
        """Log error with appropriate level"""
        log_data = {
            "error_id": context.error_id,
            "error_type": context.error_type,
            "message": context.error_message,
            "component": context.component,
            "operation": context.operation,
            "severity": context.severity.value,
            "session_id": context.session_id,
            "user_id": context.user_id
        }
        
        if context.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"Critical error: {json.dumps(log_data)}")
        elif context.severity == ErrorSeverity.HIGH:
            logger.error(f"High severity error: {json.dumps(log_data)}")
        elif context.severity == ErrorSeverity.MEDIUM:
            logger.warning(f"Medium severity error: {json.dumps(log_data)}")
        else:
            logger.info(f"Low severity error: {json.dumps(log_data)}")
    
    def _handle_connection_error(self, error: ConnectionError, context: Dict[str, Any]):
        """Handle connection errors"""
        return ErrorContext(
            error_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            error_type="ConnectionError",
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            severity=ErrorSeverity.HIGH,
            component=context.get('component', 'network'),
            operation=context.get('operation', 'connection'),
            session_id=context.get('session_id'),
            user_id=context.get('user_id'),
            context_data=context,
            recovery_attempts=0,
            recovery_strategy=RecoveryStrategy.RETRY
        )
    
    def _handle_timeout_error(self, error: TimeoutError, context: Dict[str, Any]):
        """Handle timeout errors"""
        return self._handle_connection_error(error, context)
    
    def _handle_validation_error(self, error: ValueError, context: Dict[str, Any]):
        """Handle validation errors"""
        return ErrorContext(
            error_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            error_type="ValueError",
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            severity=ErrorSeverity.MEDIUM,
            component=context.get('component', 'validation'),
            operation=context.get('operation', 'validate'),
            session_id=context.get('session_id'),
            user_id=context.get('user_id'),
            context_data=context,
            recovery_attempts=0,
            recovery_strategy=RecoveryStrategy.IGNORE
        )
    
    def _handle_key_error(self, error: KeyError, context: Dict[str, Any]):
        """Handle key errors"""
        return self._handle_validation_error(error, context)
    
    def _handle_generic_error(self, error: Exception, context: Dict[str, Any]):
        """Handle generic errors"""
        return ErrorContext(
            error_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            severity=ErrorSeverity.MEDIUM,
            component=context.get('component', 'unknown'),
            operation=context.get('operation', 'unknown'),
            session_id=context.get('session_id'),
            user_id=context.get('user_id'),
            context_data=context,
            recovery_attempts=0,
            recovery_strategy=RecoveryStrategy.RETRY
        )
    
    def get_error_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Get error statistics for the specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_errors = [
            error for error in self.error_registry.values()
            if error.timestamp >= cutoff_time
        ]
        
        stats = {
            "total_errors": len(recent_errors),
            "by_severity": {},
            "by_component": {},
            "by_error_type": {},
            "recovery_strategies": {}
        }
        
        for error in recent_errors:
            # Count by severity
            severity = error.severity.value
            stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
            
            # Count by component
            component = error.component
            stats["by_component"][component] = stats["by_component"].get(component, 0) + 1
            
            # Count by error type
            error_type = error.error_type
            stats["by_error_type"][error_type] = stats["by_error_type"].get(error_type, 0) + 1
            
            # Count by recovery strategy
            if error.recovery_strategy:
                strategy = error.recovery_strategy.value
                stats["recovery_strategies"][strategy] = stats["recovery_strategies"].get(strategy, 0) + 1
        
        return stats

def with_retry(config: RetryConfig = None, error_handler: ErrorHandler = None):
    """Decorator for adding retry logic to functions"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_config = config or RetryConfig()
            handler = error_handler or _global_error_handler
            
            last_exception = None
            
            for attempt in range(retry_config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    # Handle the error
                    context = {
                        'component': func.__module__,
                        'operation': func.__name__,
                        'attempt': attempt + 1,
                        'max_attempts': retry_config.max_attempts
                    }
                    
                    error_context = handler.handle_error(e, context)
                    error_context.recovery_attempts = attempt + 1
                    
                    # Check if we should retry
                    if attempt < retry_config.max_attempts - 1:
                        if error_context.recovery_strategy == RecoveryStrategy.RETRY:
                            delay = _calculate_delay(attempt, retry_config)
                            logger.info(f"Retrying {func.__name__} in {delay:.2f}s (attempt {attempt + 1}/{retry_config.max_attempts})")
                            time.sleep(delay)
                            continue
                        else:
                            break
                    
            # All retries exhausted
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

def with_circuit_breaker(name: str, config: CircuitBreakerConfig = None, error_handler: ErrorHandler = None):
    """Decorator for adding circuit breaker protection"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = error_handler or _global_error_handler
            
            # Register circuit breaker if not exists
            if name not in handler.circuit_breakers:
                cb_config = config or CircuitBreakerConfig()
                handler.register_circuit_breaker(name, cb_config)
            
            circuit_breaker = handler.circuit_breakers[name]
            
            try:
                return circuit_breaker.call(func, *args, **kwargs)
            except Exception as e:
                context = {
                    'component': func.__module__,
                    'operation': func.__name__,
                    'circuit_breaker': name
                }
                handler.handle_error(e, context)
                raise
        
        return wrapper
    return decorator

def _calculate_delay(attempt: int, config: RetryConfig) -> float:
    """Calculate delay for retry attempt"""
    if config.backoff_strategy == "exponential":
        delay = config.initial_delay * (config.exponential_base ** attempt)
    elif config.backoff_strategy == "linear":
        delay = config.initial_delay * (attempt + 1)
    else:  # fixed
        delay = config.initial_delay
    
    # Apply max delay
    delay = min(delay, config.max_delay)
    
    # Add jitter if enabled
    if config.jitter:
        import random
        delay *= (0.5 + random.random() * 0.5)  # 50-100% of calculated delay
    
    return delay

# Global error handler instance
_global_error_handler = ErrorHandler()

def get_error_handler() -> ErrorHandler:
    """Get the global error handler instance"""
    return _global_error_handler