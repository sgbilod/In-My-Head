"""
SQLAlchemy database models for In My Head.
Complete schema with all 15 tables, relationships, indexes, and constraints.
"""

from sqlalchemy import (
    Column, String, Integer, BigInteger, Text, Boolean,
    DateTime, Date, ARRAY, Numeric, ForeignKey,
    CheckConstraint, Index, Table
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid as uuid_pkg

Base = declarative_base()


# Association table for Document-Tag many-to-many relationship
document_tags = Table(
    'document_tags',
    Base.metadata,
    Column('document_id', UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
)

# Create indexes for association table
Index('idx_document_tags_document_id', document_tags.c.document_id)
Index('idx_document_tags_tag_id', document_tags.c.tag_id)


class User(Base):
    """User accounts and preferences."""
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(Text)
    preferences = Column(JSONB, default={})
    ai_model_preference = Column(String(100), default='local')
    theme = Column(String(50), default='dark')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    collections = relationship("Collection", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="user", cascade="all, delete-orphan")
    annotations = relationship("Annotation", back_populates="user", cascade="all, delete-orphan")
    queries = relationship("Query", back_populates="user", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="user", cascade="all, delete-orphan")
    kg_nodes = relationship("KnowledgeGraphNode", back_populates="user", cascade="all, delete-orphan")
    kg_edges = relationship("KnowledgeGraphEdge", back_populates="user", cascade="all, delete-orphan")
    processing_jobs = relationship("ProcessingJob", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Collection(Base):
    """Document organization and grouping."""
    __tablename__ = 'collections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    color = Column(String(7))
    icon = Column(String(50))
    parent_collection_id = Column(UUID(as_uuid=True), ForeignKey('collections.id', ondelete='SET NULL'), index=True)
    is_default = Column(Boolean, default=False)
    document_count = Column(Integer, default=0)
    total_size_bytes = Column(BigInteger, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="collections")
    documents = relationship("Document", back_populates="collection")
    conversations = relationship("Conversation", back_populates="collection")
    parent = relationship("Collection", remote_side=[id], backref="children")

    __table_args__ = (
        CheckConstraint("color ~ '^#[0-9A-Fa-f]{6}$'", name='check_collection_color'),
    )

    def __repr__(self) -> str:
        return f"<Collection(id={self.id}, name={self.name}, user_id={self.user_id})>"


class Document(Base):
    """User's uploaded files and extracted content."""
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('collections.id', ondelete='SET NULL'), index=True)

    # File Information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    mime_type = Column(String(255), nullable=False, index=True)
    file_hash = Column(String(64), nullable=False, index=True)

    # Document Metadata
    title = Column(String(500))
    description = Column(Text)
    language = Column(String(10), default='en')
    author = Column(String(255))
    created_date = Column(Date)

    # Processing Status
    status = Column(String(50), default='pending', index=True)
    processing_error = Column(Text)
    indexed_at = Column(DateTime(timezone=True))

    # Extracted Content
    extracted_text = Column(Text)
    text_content_length = Column(Integer)
    page_count = Column(Integer)
    word_count = Column(Integer)

    # AI-Generated Metadata
    summary = Column(Text)
    keywords = Column(ARRAY(Text))
    entities = Column(JSONB)
    topics = Column(ARRAY(Text))
    sentiment = Column(String(50))

    # Vector Search
    embedding_id = Column(UUID(as_uuid=True))
    embedding_model = Column(String(100))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="documents")
    collection = relationship("Collection", back_populates="documents")
    annotations = relationship("Annotation", back_populates="document", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=document_tags, back_populates="documents")

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed')", name='check_document_status'),
        Index('idx_documents_keywords', 'keywords', postgresql_using='gin'),
        Index('idx_documents_topics', 'topics', postgresql_using='gin'),
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, title={self.title}, status={self.status})>"


class Tag(Base):
    """Custom tags for document organization."""
    __tablename__ = 'tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    color = Column(String(7))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="tags")
    documents = relationship("Document", secondary=document_tags, back_populates="tags")

    __table_args__ = (
        CheckConstraint("color ~ '^#[0-9A-Fa-f]{6}$'", name='check_tag_color'),
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name}, user_id={self.user_id})>"


# DocumentTag is handled by the association table above


class Annotation(Base):
    """User notes and highlights on documents."""
    __tablename__ = 'annotations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)

    # Location in document
    page_number = Column(Integer)
    start_position = Column(Integer)
    end_position = Column(Integer)
    selected_text = Column(Text)

    # Annotation content
    note = Column(Text)
    highlight_color = Column(String(7))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="annotations")
    document = relationship("Document", back_populates="annotations")

    def __repr__(self) -> str:
        return f"<Annotation(id={self.id}, document_id={self.document_id})>"


class Conversation(Base):
    """Chat history with AI."""
    __tablename__ = 'conversations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(255))

    # AI Model used
    ai_model = Column(String(100), nullable=False)
    ai_provider = Column(String(50), nullable=False)

    # Context
    collection_id = Column(UUID(as_uuid=True), ForeignKey('collections.id', ondelete='SET NULL'), index=True)
    document_ids = Column(ARRAY(UUID(as_uuid=True)))

    # Statistics
    message_count = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), index=True)
    last_message_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="conversations")
    collection = relationship("Collection", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title={self.title}, ai_model={self.ai_model})>"


class Message(Base):
    """Individual messages in conversations."""
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)

    # Message content
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

    # Metadata
    tokens = Column(Integer)
    model = Column(String(100))

    # Citations
    cited_document_ids = Column(ARRAY(UUID(as_uuid=True)))
    citations = Column(JSONB)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant', 'system')", name='check_message_role'),
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"


class Query(Base):
    """Search history and analytics."""
    __tablename__ = 'queries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # Query details
    query_text = Column(Text, nullable=False)
    query_type = Column(String(50))
    filters = Column(JSONB)

    # Results
    result_count = Column(Integer)
    result_document_ids = Column(ARRAY(UUID(as_uuid=True)))

    # Performance
    execution_time_ms = Column(Integer)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="queries")

    def __repr__(self) -> str:
        return f"<Query(id={self.id}, query_type={self.query_type}, result_count={self.result_count})>"


class Resource(Base):
    """External resources discovered/managed."""
    __tablename__ = 'resources'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # Resource details
    resource_type = Column(String(50), nullable=False)
    url = Column(Text, nullable=False, index=True)
    title = Column(String(500))
    description = Column(Text)

    # Metadata
    domain = Column(String(255), index=True)
    last_fetched_at = Column(DateTime(timezone=True))
    fetch_status = Column(String(50))
    fetch_error = Column(Text)

    # Content
    content = Column(Text)
    content_hash = Column(String(64))

    # Auto-discovery
    discovered_by = Column(String(100))
    relevance_score = Column(Numeric(3, 2))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="resources")

    def __repr__(self) -> str:
        return f"<Resource(id={self.id}, resource_type={self.resource_type}, url={self.url})>"


class KnowledgeGraphNode(Base):
    """Entities in knowledge graph."""
    __tablename__ = 'knowledge_graph_nodes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # Node details
    entity_name = Column(String(255), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True)

    # Content
    description = Column(Text)
    properties = Column(JSONB)

    # Connections
    document_ids = Column(ARRAY(UUID(as_uuid=True)))
    occurrence_count = Column(Integer, default=0)

    # Embeddings
    embedding_id = Column(UUID(as_uuid=True))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="kg_nodes")
    outgoing_edges = relationship("KnowledgeGraphEdge", foreign_keys="KnowledgeGraphEdge.source_node_id", back_populates="source_node", cascade="all, delete-orphan")
    incoming_edges = relationship("KnowledgeGraphEdge", foreign_keys="KnowledgeGraphEdge.target_node_id", back_populates="target_node", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<KnowledgeGraphNode(id={self.id}, entity_name={self.entity_name}, entity_type={self.entity_type})>"


class KnowledgeGraphEdge(Base):
    """Relationships between entities in knowledge graph."""
    __tablename__ = 'knowledge_graph_edges'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Edge details
    source_node_id = Column(UUID(as_uuid=True), ForeignKey('knowledge_graph_nodes.id', ondelete='CASCADE'), nullable=False, index=True)
    target_node_id = Column(UUID(as_uuid=True), ForeignKey('knowledge_graph_nodes.id', ondelete='CASCADE'), nullable=False, index=True)
    relationship_type = Column(String(100), nullable=False, index=True)

    # Metadata
    strength = Column(Numeric(3, 2), default=1.0)
    document_ids = Column(ARRAY(UUID(as_uuid=True)))
    context = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="kg_edges")
    source_node = relationship("KnowledgeGraphNode", foreign_keys=[source_node_id], back_populates="outgoing_edges")
    target_node = relationship("KnowledgeGraphNode", foreign_keys=[target_node_id], back_populates="incoming_edges")

    __table_args__ = (
        Index('idx_kg_edges_unique', 'source_node_id', 'target_node_id', 'relationship_type', unique=True),
    )

    def __repr__(self) -> str:
        return f"<KnowledgeGraphEdge(id={self.id}, relationship_type={self.relationship_type})>"


class ProcessingJob(Base):
    """Background processing jobs."""
    __tablename__ = 'processing_jobs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # Job details
    job_type = Column(String(100), nullable=False)
    entity_id = Column(UUID(as_uuid=True))
    entity_type = Column(String(50))

    # Status
    status = Column(String(50), default='pending', index=True)
    progress = Column(Integer, default=0)
    error_message = Column(Text)

    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="processing_jobs")

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'running', 'completed', 'failed')", name='check_job_status'),
        CheckConstraint("progress >= 0 AND progress <= 100", name='check_job_progress'),
        Index('idx_jobs_entity', 'entity_id', 'entity_type'),
    )

    def __repr__(self) -> str:
        return f"<ProcessingJob(id={self.id}, job_type={self.job_type}, status={self.status})>"


class ApiKey(Base):
    """API keys for external AI services."""
    __tablename__ = 'api_keys'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # API details
    provider = Column(String(50), nullable=False, index=True)
    encrypted_key = Column(Text, nullable=False)
    key_name = Column(String(100))

    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="api_keys")

    def __repr__(self) -> str:
        return f"<ApiKey(id={self.id}, provider={self.provider}, key_name={self.key_name})>"


class SystemSetting(Base):
    """System-wide configuration settings."""
    __tablename__ = 'system_settings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4)
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(JSONB, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<SystemSetting(key={self.key})>"


# Alias for backward compatibility
DocumentTag = document_tags
