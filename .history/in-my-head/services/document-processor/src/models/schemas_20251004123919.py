"""
Pydantic schemas for API request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field, UUID4, validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============= Enums =============

class DocumentStatus(str, Enum):
    """Document processing status."""
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ResourceStatus(str, Enum):
    """Resource fetch status."""
    pending = "pending"
    fetching = "fetching"
    completed = "completed"
    failed = "failed"


class ProcessingJobType(str, Enum):
    """Processing job types."""
    document_ingestion = "document_ingestion"
    document_analysis = "document_analysis"
    embedding_generation = "embedding_generation"
    knowledge_graph_extraction = "knowledge_graph_extraction"


class ProcessingJobStatus(str, Enum):
    """Processing job status."""
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class MessageRole(str, Enum):
    """Message roles in conversation."""
    system = "system"
    user = "user"
    assistant = "assistant"


class SearchType(str, Enum):
    """Search query types."""
    semantic = "semantic"
    keyword = "keyword"
    hybrid = "hybrid"


# ============= Base Schemas =============

class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============= User Schemas =============

class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    preferences: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase, TimestampMixin):
    """Schema for user response."""
    id: UUID4
    preferences: Dict[str, Any] = Field(default_factory=dict)
    is_verified: bool
    is_active: bool
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============= Collection Schemas =============

class CollectionBase(BaseModel):
    """Base collection schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    
    model_config = ConfigDict(from_attributes=True)


class CollectionCreate(CollectionBase):
    """Schema for creating a collection."""
    parent_collection_id: Optional[UUID4] = None


class CollectionUpdate(BaseModel):
    """Schema for updating a collection."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    parent_collection_id: Optional[UUID4] = None
    
    model_config = ConfigDict(from_attributes=True)


class CollectionResponse(CollectionBase, TimestampMixin):
    """Schema for collection response."""
    id: UUID4
    user_id: UUID4
    parent_collection_id: Optional[UUID4] = None
    is_default: bool
    document_count: int
    total_size: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= Document Schemas =============

class DocumentBase(BaseModel):
    """Base document schema."""
    title: str = Field(..., min_length=1, max_length=512)
    file_path: Optional[str] = Field(None, max_length=1024)
    mime_type: Optional[str] = Field(None, max_length=100)
    
    model_config = ConfigDict(from_attributes=True)


class DocumentUpload(BaseModel):
    """Schema for uploading a document."""
    title: str = Field(..., min_length=1, max_length=512)
    collection_id: UUID4
    file_path: str = Field(..., max_length=1024)
    file_hash: str = Field(..., max_length=64)
    file_size: int = Field(..., gt=0)
    mime_type: str = Field(..., max_length=100)
    tags: Optional[List[UUID4]] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)


class DocumentUpdate(BaseModel):
    """Schema for updating a document."""
    title: Optional[str] = Field(None, min_length=1, max_length=512)
    collection_id: Optional[UUID4] = None
    
    model_config = ConfigDict(from_attributes=True)


class DocumentResponse(DocumentBase, TimestampMixin):
    """Schema for document response."""
    id: UUID4
    user_id: UUID4
    collection_id: UUID4
    file_hash: str
    file_size: int
    processing_status: DocumentStatus
    extracted_text: Optional[str] = None
    summary: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    entities: Dict[str, Any] = Field(default_factory=dict)
    topics: List[str] = Field(default_factory=list)
    embedding_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(from_attributes=True)


# ============= Tag Schemas =============

class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    
    model_config = ConfigDict(from_attributes=True)


class TagCreate(TagBase):
    """Schema for creating a tag."""
    pass


class TagResponse(TagBase, TimestampMixin):
    """Schema for tag response."""
    id: UUID4
    user_id: UUID4
    
    model_config = ConfigDict(from_attributes=True)


# ============= Annotation Schemas =============

class AnnotationBase(BaseModel):
    """Base annotation schema."""
    page_number: Optional[int] = Field(None, ge=1)
    content: str = Field(..., min_length=1)
    
    model_config = ConfigDict(from_attributes=True)


class AnnotationCreate(AnnotationBase):
    """Schema for creating an annotation."""
    document_id: UUID4
    start_position: Optional[int] = Field(None, ge=0)
    end_position: Optional[int] = Field(None, ge=0)
    highlight_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    note: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class AnnotationResponse(AnnotationBase, TimestampMixin):
    """Schema for annotation response."""
    id: UUID4
    user_id: UUID4
    document_id: UUID4
    start_position: Optional[int] = None
    end_position: Optional[int] = None
    highlight_color: Optional[str] = None
    note: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============= Conversation Schemas =============

class ConversationBase(BaseModel):
    """Base conversation schema."""
    title: str = Field(..., min_length=1, max_length=255)
    
    model_config = ConfigDict(from_attributes=True)


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation."""
    context_document_ids: Optional[List[UUID4]] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)


class ConversationResponse(ConversationBase, TimestampMixin):
    """Schema for conversation response."""
    id: UUID4
    user_id: UUID4
    ai_model: Optional[str] = None
    context_document_ids: List[UUID4] = Field(default_factory=list)
    message_count: int
    total_tokens: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= Message Schemas =============

class MessageBase(BaseModel):
    """Base message schema."""
    role: MessageRole
    content: str = Field(..., min_length=1)
    
    model_config = ConfigDict(from_attributes=True)


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    conversation_id: UUID4
    citations: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(MessageBase, TimestampMixin):
    """Schema for message response."""
    id: UUID4
    conversation_id: UUID4
    token_count: int
    citations: Dict[str, Any] = Field(default_factory=dict)
    cited_document_ids: List[UUID4] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)


# ============= Query Schemas =============

class SearchQuery(BaseModel):
    """Schema for search query."""
    query_text: str = Field(..., min_length=1)
    search_type: SearchType = SearchType.hybrid
    collection_ids: Optional[List[UUID4]] = None
    tag_ids: Optional[List[UUID4]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
    
    model_config = ConfigDict(from_attributes=True)


class QueryResponse(BaseModel):
    """Schema for query response."""
    id: UUID4
    user_id: UUID4
    query_text: str
    search_type: SearchType
    filters: Dict[str, Any] = Field(default_factory=dict)
    result_count: int
    execution_time_ms: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============= Resource Schemas =============

class ResourceBase(BaseModel):
    """Base resource schema."""
    url: str = Field(..., max_length=2048)
    title: Optional[str] = Field(None, max_length=512)
    
    model_config = ConfigDict(from_attributes=True)


class ResourceCreate(ResourceBase):
    """Schema for creating a resource."""
    collection_id: Optional[UUID4] = None
    
    model_config = ConfigDict(from_attributes=True)


class ResourceResponse(ResourceBase, TimestampMixin):
    """Schema for resource response."""
    id: UUID4
    user_id: UUID4
    collection_id: Optional[UUID4] = None
    status: ResourceStatus
    content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    last_fetched_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============= Knowledge Graph Schemas =============

class KnowledgeGraphNodeCreate(BaseModel):
    """Schema for creating a knowledge graph node."""
    entity_name: str = Field(..., min_length=1, max_length=255)
    entity_type: str = Field(..., max_length=100)
    properties: Optional[Dict[str, Any]] = Field(default_factory=dict)
    document_ids: Optional[List[UUID4]] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)


class KnowledgeGraphNodeResponse(BaseModel):
    """Schema for knowledge graph node response."""
    id: UUID4
    user_id: UUID4
    entity_name: str
    entity_type: str
    properties: Dict[str, Any]
    document_ids: List[UUID4]
    embedding_id: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class KnowledgeGraphEdgeCreate(BaseModel):
    """Schema for creating a knowledge graph edge."""
    source_node_id: UUID4
    target_node_id: UUID4
    relationship_type: str = Field(..., max_length=100)
    strength: float = Field(1.0, ge=0.0, le=1.0)
    properties: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    model_config = ConfigDict(from_attributes=True)


class KnowledgeGraphEdgeResponse(BaseModel):
    """Schema for knowledge graph edge response."""
    id: UUID4
    user_id: UUID4
    source_node_id: UUID4
    target_node_id: UUID4
    relationship_type: str
    strength: float
    properties: Dict[str, Any]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============= Processing Job Schemas =============

class ProcessingJobCreate(BaseModel):
    """Schema for creating a processing job."""
    job_type: ProcessingJobType
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    model_config = ConfigDict(from_attributes=True)


class ProcessingJobResponse(BaseModel):
    """Schema for processing job response."""
    id: UUID4
    user_id: UUID4
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    progress: int
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============= API Key Schemas =============

class ApiKeyCreate(BaseModel):
    """Schema for creating an API key."""
    provider: str = Field(..., max_length=50)
    encrypted_key: str
    description: Optional[str] = Field(None, max_length=255)
    
    model_config = ConfigDict(from_attributes=True)


class ApiKeyResponse(BaseModel):
    """Schema for API key response."""
    id: UUID4
    user_id: UUID4
    provider: str
    description: Optional[str] = None
    last_used_at: Optional[datetime] = None
    usage_count: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============= System Setting Schemas =============

class SystemSettingCreate(BaseModel):
    """Schema for creating a system setting."""
    key: str = Field(..., max_length=100)
    value: Any
    description: Optional[str] = Field(None, max_length=255)
    
    model_config = ConfigDict(from_attributes=True)


class SystemSettingUpdate(BaseModel):
    """Schema for updating a system setting."""
    value: Any
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class SystemSettingResponse(BaseModel):
    """Schema for system setting response."""
    id: UUID4
    key: str
    value: Any
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
