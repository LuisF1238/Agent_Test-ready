"""
Session Management Module

Handles persistent session storage and conversation history.
"""

import sqlite3
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import uuid


@dataclass
class SessionContext:
    """Session context data structure"""
    session_id: str
    user_id: Optional[str]
    conversation_history: List[Dict[str, Any]]
    shared_context: Dict[str, Any]
    active_agents: List[str]
    created_at: datetime
    last_updated: datetime


class SessionManager:
    """Manages persistent sessions and conversation history"""
    
    def __init__(self, persistent: bool = True, db_path: str = "sessions.db"):
        self.persistent = persistent
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.sessions: Dict[str, SessionContext] = {}
        
        if self.persistent:
            self._initialize_db()
        
        self.logger.info(f"Session manager initialized with database: {db_path}")
    
    def _initialize_db(self):
        """Initialize the SQLite database for persistent sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        conversation_history TEXT,
                        shared_context TEXT,
                        active_agents TEXT,
                        created_at TEXT,
                        last_updated TEXT
                    )
                """)
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to initialize session database: {e}")
            self.persistent = False
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session = SessionContext(
            session_id=session_id,
            user_id=user_id,
            conversation_history=[],
            shared_context={},
            active_agents=[],
            created_at=now,
            last_updated=now
        )
        
        self.sessions[session_id] = session
        
        if self.persistent:
            self._save_session(session)
        
        self.logger.info(f"Created session {session_id} for user {user_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionContext]:
        """Get session by ID"""
        if session_id in self.sessions:
            return self.sessions[session_id]
        
        if self.persistent:
            session = self._load_session(session_id)
            if session:
                self.sessions[session_id] = session
                return session
        
        return None
    
    def update_session(self, session_id: str, **kwargs):
        """Update session data"""
        session = self.get_session(session_id)
        if not session:
            self.logger.warning(f"Session {session_id} not found for update")
            return
        
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        session.last_updated = datetime.now()
        
        if self.persistent:
            self._save_session(session)
    
    def add_to_conversation_history(self, session_id: str, message: Dict[str, Any]):
        """Add message to conversation history"""
        session = self.get_session(session_id)
        if session:
            session.conversation_history.append(message)
            session.last_updated = datetime.now()
            
            if self.persistent:
                self._save_session(session)
    
    def get_conversation_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history for session"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        history = session.conversation_history
        if limit:
            history = history[-limit:]
        
        return history
    
    def cleanup_old_sessions(self, hours: int = 24) -> int:
        """Clean up sessions older than specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        removed_count = 0
        
        # Clean up in-memory sessions
        to_remove = []
        for session_id, session in self.sessions.items():
            if session.last_updated < cutoff:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            del self.sessions[session_id]
            removed_count += 1
        
        # Clean up database sessions
        if self.persistent:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "DELETE FROM sessions WHERE last_updated < ?",
                        (cutoff.isoformat(),)
                    )
                    removed_count += cursor.rowcount
                    conn.commit()
            except Exception as e:
                self.logger.error(f"Failed to cleanup database sessions: {e}")
        
        self.logger.info(f"Cleaned up {removed_count} old sessions")
        return removed_count
    
    def _save_session(self, session: SessionContext):
        """Save session to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO sessions 
                    (session_id, user_id, conversation_history, shared_context, 
                     active_agents, created_at, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.session_id,
                    session.user_id,
                    json.dumps(session.conversation_history),
                    json.dumps(session.shared_context),
                    json.dumps(session.active_agents),
                    session.created_at.isoformat(),
                    session.last_updated.isoformat()
                ))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to save session {session.session_id}: {e}")
    
    def _load_session(self, session_id: str) -> Optional[SessionContext]:
        """Load session from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT * FROM sessions WHERE session_id = ?",
                    (session_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    return SessionContext(
                        session_id=row[0],
                        user_id=row[1],
                        conversation_history=json.loads(row[2]),
                        shared_context=json.loads(row[3]),
                        active_agents=json.loads(row[4]),
                        created_at=datetime.fromisoformat(row[5]),
                        last_updated=datetime.fromisoformat(row[6])
                    )
        except Exception as e:
            self.logger.error(f"Failed to load session {session_id}: {e}")
        
        return None