/**
 * Zod validation schemas for API Gateway request/response validation
 */

import { z } from 'zod';

// ============= Common Schemas =============

const uuidSchema = z.string().uuid();
const emailSchema = z.string().email();
const urlSchema = z.string().url();
const hexColorSchema = z.string().regex(/^#[0-9A-Fa-f]{6}$/);
const timestampSchema = z.coerce.date();

// ============= Enums =============

export const DocumentStatusEnum = z.enum(['pending', 'processing', 'completed', 'failed']);
export const ResourceStatusEnum = z.enum(['pending', 'fetching', 'completed', 'failed']);
export const ProcessingJobTypeEnum = z.enum([
  'document_ingestion',
  'document_analysis',
  'embedding_generation',
  'knowledge_graph_extraction',
]);
export const ProcessingJobStatusEnum = z.enum(['queued', 'processing', 'completed', 'failed']);
export const MessageRoleEnum = z.enum(['system', 'user', 'assistant']);
export const SearchTypeEnum = z.enum(['semantic', 'keyword', 'hybrid']);

// ============= User Schemas =============

export const userBaseSchema = z.object({
  username: z.string().min(3).max(50),
  email: emailSchema,
  fullName: z.string().max(255).optional().nullable(),
});

export const userCreateSchema = userBaseSchema.extend({
  password: z.string().min(8).max(255),
});

export const userUpdateSchema = z.object({
  email: emailSchema.optional(),
  fullName: z.string().max(255).optional().nullable(),
  preferences: z.record(z.any()).optional(),
});

export const userResponseSchema = userBaseSchema.extend({
  id: uuidSchema,
  preferences: z.record(z.any()).default({}),
  isVerified: z.boolean(),
  isActive: z.boolean(),
  lastLogin: timestampSchema.nullable(),
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Collection Schemas =============

export const collectionBaseSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().optional().nullable(),
  color: hexColorSchema,
  icon: z.string().max(50).optional().nullable(),
});

export const collectionCreateSchema = collectionBaseSchema.extend({
  parentCollectionId: uuidSchema.optional().nullable(),
});

export const collectionUpdateSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  description: z.string().optional().nullable(),
  color: hexColorSchema.optional(),
  icon: z.string().max(50).optional().nullable(),
  parentCollectionId: uuidSchema.optional().nullable(),
});

export const collectionResponseSchema = collectionBaseSchema.extend({
  id: uuidSchema,
  userId: uuidSchema,
  parentCollectionId: uuidSchema.nullable(),
  isDefault: z.boolean(),
  documentCount: z.number().int().nonnegative(),
  totalSize: z.number().int().nonnegative(),
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Document Schemas =============

export const documentBaseSchema = z.object({
  title: z.string().min(1).max(512),
  filePath: z.string().max(1024).optional().nullable(),
  mimeType: z.string().max(100).optional().nullable(),
});

export const documentUploadSchema = z.object({
  title: z.string().min(1).max(512),
  collectionId: uuidSchema,
  filePath: z.string().max(1024),
  fileHash: z.string().max(64),
  fileSize: z.number().int().positive(),
  mimeType: z.string().max(100),
  tags: z.array(uuidSchema).default([]),
});

export const documentUpdateSchema = z.object({
  title: z.string().min(1).max(512).optional(),
  collectionId: uuidSchema.optional(),
});

export const documentResponseSchema = documentBaseSchema.extend({
  id: uuidSchema,
  userId: uuidSchema,
  collectionId: uuidSchema,
  fileHash: z.string(),
  fileSize: z.number().int().nonnegative(),
  processingStatus: DocumentStatusEnum,
  extractedText: z.string().optional().nullable(),
  summary: z.string().optional().nullable(),
  keywords: z.array(z.string()).default([]),
  entities: z.record(z.any()).default({}),
  topics: z.array(z.string()).default([]),
  embeddingId: z.string().optional().nullable(),
  metadata: z.record(z.any()).default({}),
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Tag Schemas =============

export const tagBaseSchema = z.object({
  name: z.string().min(1).max(50),
  color: hexColorSchema,
});

export const tagCreateSchema = tagBaseSchema;

export const tagResponseSchema = tagBaseSchema.extend({
  id: uuidSchema,
  userId: uuidSchema,
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Annotation Schemas =============

export const annotationBaseSchema = z.object({
  pageNumber: z.number().int().positive().optional().nullable(),
  content: z.string().min(1),
});

export const annotationCreateSchema = annotationBaseSchema.extend({
  documentId: uuidSchema,
  startPosition: z.number().int().nonnegative().optional().nullable(),
  endPosition: z.number().int().nonnegative().optional().nullable(),
  highlightColor: hexColorSchema.optional().nullable(),
  note: z.string().optional().nullable(),
});

export const annotationResponseSchema = annotationBaseSchema.extend({
  id: uuidSchema,
  userId: uuidSchema,
  documentId: uuidSchema,
  startPosition: z.number().int().optional().nullable(),
  endPosition: z.number().int().optional().nullable(),
  highlightColor: hexColorSchema.optional().nullable(),
  note: z.string().optional().nullable(),
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Conversation Schemas =============

export const conversationBaseSchema = z.object({
  title: z.string().min(1).max(255),
});

export const conversationCreateSchema = conversationBaseSchema.extend({
  contextDocumentIds: z.array(uuidSchema).default([]),
});

export const conversationResponseSchema = conversationBaseSchema.extend({
  id: uuidSchema,
  userId: uuidSchema,
  aiModel: z.string().optional().nullable(),
  contextDocumentIds: z.array(uuidSchema).default([]),
  messageCount: z.number().int().nonnegative(),
  totalTokens: z.number().int().nonnegative(),
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Message Schemas =============

export const messageBaseSchema = z.object({
  role: MessageRoleEnum,
  content: z.string().min(1),
});

export const messageCreateSchema = messageBaseSchema.extend({
  conversationId: uuidSchema,
  citations: z.record(z.any()).default({}),
});

export const messageResponseSchema = messageBaseSchema.extend({
  id: uuidSchema,
  conversationId: uuidSchema,
  tokenCount: z.number().int().nonnegative(),
  citations: z.record(z.any()).default({}),
  citedDocumentIds: z.array(uuidSchema).default([]),
  createdAt: timestampSchema,
});

// ============= Query Schemas =============

export const searchQuerySchema = z.object({
  queryText: z.string().min(1),
  searchType: SearchTypeEnum.default('hybrid'),
  collectionIds: z.array(uuidSchema).optional().nullable(),
  tagIds: z.array(uuidSchema).optional().nullable(),
  dateFrom: timestampSchema.optional().nullable(),
  dateTo: timestampSchema.optional().nullable(),
  limit: z.number().int().min(1).max(100).default(10),
  offset: z.number().int().nonnegative().default(0),
});

export const queryResponseSchema = z.object({
  id: uuidSchema,
  userId: uuidSchema,
  queryText: z.string(),
  searchType: SearchTypeEnum,
  filters: z.record(z.any()).default({}),
  resultCount: z.number().int().nonnegative(),
  executionTimeMs: z.number().int().nonnegative(),
  createdAt: timestampSchema,
});

// ============= Resource Schemas =============

export const resourceBaseSchema = z.object({
  url: urlSchema,
  title: z.string().max(512).optional().nullable(),
});

export const resourceCreateSchema = resourceBaseSchema.extend({
  collectionId: uuidSchema.optional().nullable(),
});

export const resourceResponseSchema = resourceBaseSchema.extend({
  id: uuidSchema,
  userId: uuidSchema,
  collectionId: uuidSchema.nullable(),
  status: ResourceStatusEnum,
  content: z.string().optional().nullable(),
  metadata: z.record(z.any()).default({}),
  lastFetchedAt: timestampSchema.nullable(),
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Knowledge Graph Schemas =============

export const knowledgeGraphNodeCreateSchema = z.object({
  entityName: z.string().min(1).max(255),
  entityType: z.string().max(100),
  properties: z.record(z.any()).default({}),
  documentIds: z.array(uuidSchema).default([]),
});

export const knowledgeGraphNodeResponseSchema = z.object({
  id: uuidSchema,
  userId: uuidSchema,
  entityName: z.string(),
  entityType: z.string(),
  properties: z.record(z.any()),
  documentIds: z.array(uuidSchema),
  embeddingId: z.string().optional().nullable(),
  createdAt: timestampSchema,
});

export const knowledgeGraphEdgeCreateSchema = z.object({
  sourceNodeId: uuidSchema,
  targetNodeId: uuidSchema,
  relationshipType: z.string().max(100),
  strength: z.number().min(0).max(1).default(1.0),
  properties: z.record(z.any()).default({}),
});

export const knowledgeGraphEdgeResponseSchema = z.object({
  id: uuidSchema,
  userId: uuidSchema,
  sourceNodeId: uuidSchema,
  targetNodeId: uuidSchema,
  relationshipType: z.string(),
  strength: z.number(),
  properties: z.record(z.any()),
  createdAt: timestampSchema,
});

// ============= Processing Job Schemas =============

export const processingJobCreateSchema = z.object({
  jobType: ProcessingJobTypeEnum,
  parameters: z.record(z.any()).default({}),
});

export const processingJobResponseSchema = z.object({
  id: uuidSchema,
  userId: uuidSchema,
  jobType: ProcessingJobTypeEnum,
  status: ProcessingJobStatusEnum,
  progress: z.number().int().min(0).max(100),
  parameters: z.record(z.any()),
  result: z.record(z.any()).optional().nullable(),
  errorMessage: z.string().optional().nullable(),
  createdAt: timestampSchema,
  startedAt: timestampSchema.nullable(),
  completedAt: timestampSchema.nullable(),
});

// ============= API Key Schemas =============

export const apiKeyCreateSchema = z.object({
  provider: z.string().max(50),
  encryptedKey: z.string(),
  description: z.string().max(255).optional().nullable(),
});

export const apiKeyResponseSchema = z.object({
  id: uuidSchema,
  userId: uuidSchema,
  provider: z.string(),
  description: z.string().optional().nullable(),
  lastUsedAt: timestampSchema.nullable(),
  usageCount: z.number().int().nonnegative(),
  createdAt: timestampSchema,
});

// ============= System Setting Schemas =============

export const systemSettingCreateSchema = z.object({
  key: z.string().max(100),
  value: z.any(),
  description: z.string().max(255).optional().nullable(),
});

export const systemSettingUpdateSchema = z.object({
  value: z.any(),
  description: z.string().max(255).optional().nullable(),
});

export const systemSettingResponseSchema = z.object({
  id: uuidSchema,
  key: z.string(),
  value: z.any(),
  description: z.string().optional().nullable(),
  createdAt: timestampSchema,
  updatedAt: timestampSchema,
});

// ============= Type Exports =============

export type UserCreate = z.infer<typeof userCreateSchema>;
export type UserUpdate = z.infer<typeof userUpdateSchema>;
export type UserResponse = z.infer<typeof userResponseSchema>;

export type CollectionCreate = z.infer<typeof collectionCreateSchema>;
export type CollectionUpdate = z.infer<typeof collectionUpdateSchema>;
export type CollectionResponse = z.infer<typeof collectionResponseSchema>;

export type DocumentUpload = z.infer<typeof documentUploadSchema>;
export type DocumentUpdate = z.infer<typeof documentUpdateSchema>;
export type DocumentResponse = z.infer<typeof documentResponseSchema>;

export type TagCreate = z.infer<typeof tagCreateSchema>;
export type TagResponse = z.infer<typeof tagResponseSchema>;

export type AnnotationCreate = z.infer<typeof annotationCreateSchema>;
export type AnnotationResponse = z.infer<typeof annotationResponseSchema>;

export type ConversationCreate = z.infer<typeof conversationCreateSchema>;
export type ConversationResponse = z.infer<typeof conversationResponseSchema>;

export type MessageCreate = z.infer<typeof messageCreateSchema>;
export type MessageResponse = z.infer<typeof messageResponseSchema>;

export type SearchQuery = z.infer<typeof searchQuerySchema>;
export type QueryResponse = z.infer<typeof queryResponseSchema>;

export type ResourceCreate = z.infer<typeof resourceCreateSchema>;
export type ResourceResponse = z.infer<typeof resourceResponseSchema>;

export type KnowledgeGraphNodeCreate = z.infer<typeof knowledgeGraphNodeCreateSchema>;
export type KnowledgeGraphNodeResponse = z.infer<typeof knowledgeGraphNodeResponseSchema>;

export type KnowledgeGraphEdgeCreate = z.infer<typeof knowledgeGraphEdgeCreateSchema>;
export type KnowledgeGraphEdgeResponse = z.infer<typeof knowledgeGraphEdgeResponseSchema>;

export type ProcessingJobCreate = z.infer<typeof processingJobCreateSchema>;
export type ProcessingJobResponse = z.infer<typeof processingJobResponseSchema>;

export type ApiKeyCreate = z.infer<typeof apiKeyCreateSchema>;
export type ApiKeyResponse = z.infer<typeof apiKeyResponseSchema>;

export type SystemSettingCreate = z.infer<typeof systemSettingCreateSchema>;
export type SystemSettingUpdate = z.infer<typeof systemSettingUpdateSchema>;
export type SystemSettingResponse = z.infer<typeof systemSettingResponseSchema>;
