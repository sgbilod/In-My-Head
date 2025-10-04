"""
Database models and validation schemas for In My Head document processor.
"""

# Database models (SQLAlchemy)
from .database import (
    Base,
    User,
    Collection,
    Document,
    Tag,
    DocumentTag,
    Annotation,
    Conversation,
    Message,
    Query,
    Resource,
    KnowledgeGraphNode,
    KnowledgeGraphEdge,
    ProcessingJob,
    ApiKey,
    SystemSetting
)

# Validation schemas (Pydantic)
from .schemas import (
    # Enums
    DocumentStatus,
    ResourceStatus,
    ProcessingJobType,
    ProcessingJobStatus,
    MessageRole,
    SearchType,
    # User schemas
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    # Collection schemas
    CollectionBase,
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
    # Document schemas
    DocumentBase,
    DocumentUpload,
    DocumentUpdate,
    DocumentResponse,
    # Tag schemas
    TagBase,
    TagCreate,
    TagResponse,
    # Annotation schemas
    AnnotationBase,
    AnnotationCreate,
    AnnotationResponse,
    # Conversation schemas
    ConversationBase,
    ConversationCreate,
    ConversationResponse,
    # Message schemas
    MessageBase,
    MessageCreate,
    MessageResponse,
    # Query schemas
    SearchQuery,
    QueryResponse,
    # Resource schemas
    ResourceBase,
    ResourceCreate,
    ResourceResponse,
    # Knowledge Graph schemas
    KnowledgeGraphNodeCreate,
    KnowledgeGraphNodeResponse,
    KnowledgeGraphEdgeCreate,
    KnowledgeGraphEdgeResponse,
    # Processing Job schemas
    ProcessingJobCreate,
    ProcessingJobResponse,
    # API Key schemas
    ApiKeyCreate,
    ApiKeyResponse,
    # System Setting schemas
    SystemSettingCreate,
    SystemSettingUpdate,
    SystemSettingResponse,
)

__all__ = [
    # Database models
    "Base",
    "User",
    "Collection",
    "Document",
    "Tag",
    "DocumentTag",
    "Annotation",
    "Conversation",
    "Message",
    "Query",
    "Resource",
    "KnowledgeGraphNode",
    "KnowledgeGraphEdge",
    "ProcessingJob",
    "ApiKey",
    "SystemSetting",
    # Enums
    "DocumentStatus",
    "ResourceStatus",
    "ProcessingJobType",
    "ProcessingJobStatus",
    "MessageRole",
    "SearchType",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Collection schemas
    "CollectionBase",
    "CollectionCreate",
    "CollectionUpdate",
    "CollectionResponse",
    # Document schemas
    "DocumentBase",
    "DocumentUpload",
    "DocumentUpdate",
    "DocumentResponse",
    # Tag schemas
    "TagBase",
    "TagCreate",
    "TagResponse",
    # Annotation schemas
    "AnnotationBase",
    "AnnotationCreate",
    "AnnotationResponse",
    # Conversation schemas
    "ConversationBase",
    "ConversationCreate",
    "ConversationResponse",
    # Message schemas
    "MessageBase",
    "MessageCreate",
    "MessageResponse",
    # Query schemas
    "SearchQuery",
    "QueryResponse",
    # Resource schemas
    "ResourceBase",
    "ResourceCreate",
    "ResourceResponse",
    # Knowledge Graph schemas
    "KnowledgeGraphNodeCreate",
    "KnowledgeGraphNodeResponse",
    "KnowledgeGraphEdgeCreate",
    "KnowledgeGraphEdgeResponse",
    # Processing Job schemas
    "ProcessingJobCreate",
    "ProcessingJobResponse",
    # API Key schemas
    "ApiKeyCreate",
    "ApiKeyResponse",
    # System Setting schemas
    "SystemSettingCreate",
    "SystemSettingUpdate",
    "SystemSettingResponse",
]
