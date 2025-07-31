#!/usr/bin/env node
/**
 * Oracle-Enabled MCP Memory Server
 * Automatically syncs all memory operations with Oracle Object Storage
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const fs = require('fs').promises;
const path = require('path');
const https = require('https');

// Oracle Object Storage configuration
const ORACLE_BASE_URL = process.env.ORACLE_BASE_URL || "";
const MEMORY_OBJECT_NAME = "copilot-memory.json";
const LOCAL_MEMORY_PATH = process.env.MEMORY_FILE_PATH || "./copilot-memory.json";

class OracleMemoryServer {
  constructor() {
    this.server = new Server(
      {
        name: 'oracle-memory-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  async uploadToOracle(memoryData) {
    return new Promise((resolve, reject) => {
      const uploadUrl = `${ORACLE_BASE_URL}${MEMORY_OBJECT_NAME}`;
      const data = JSON.stringify(memoryData, null, 2);
      
      const url = new URL(uploadUrl);
      const options = {
        hostname: url.hostname,
        port: 443,
        path: url.pathname + url.search,
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data)
        }
      };

      const req = https.request(options, (res) => {
        let responseData = '';
        res.on('data', (chunk) => {
          responseData += chunk;
        });
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            console.log(`✅ Memory synced to Oracle Cloud at ${new Date().toISOString()}`);
            resolve(true);
          } else {
            console.error(`❌ Oracle upload failed: ${res.statusCode}`);
            reject(new Error(`Upload failed: ${res.statusCode}`));
          }
        });
      });

      req.on('error', (error) => {
        console.error(`❌ Oracle upload error: ${error.message}`);
        reject(error);
      });

      req.write(data);
      req.end();
    });
  }

  async downloadFromOracle() {
    return new Promise((resolve, reject) => {
      const downloadUrl = `${ORACLE_BASE_URL}${MEMORY_OBJECT_NAME}`;
      
      const url = new URL(downloadUrl);
      const options = {
        hostname: url.hostname,
        port: 443,
        path: url.pathname + url.search,
        method: 'GET'
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const memoryData = JSON.parse(data);
              console.log(`✅ Memory downloaded from Oracle Cloud at ${new Date().toISOString()}`);
              resolve(memoryData);
            } catch (error) {
              console.error(`❌ Invalid JSON from Oracle: ${error.message}`);
              resolve({ entities: [], relations: [] });
            }
          } else if (res.statusCode === 404) {
            console.log(`⚠️  No memory found in Oracle Cloud, starting fresh`);
            resolve({ entities: [], relations: [] });
          } else {
            console.error(`❌ Oracle download failed: ${res.statusCode}`);
            reject(new Error(`Download failed: ${res.statusCode}`));
          }
        });
      });

      req.on('error', (error) => {
        console.error(`❌ Oracle download error: ${error.message}`);
        reject(error);
      });

      req.end();
    });
  }

  async loadMemory() {
    try {
      // Always load from Oracle Cloud first
      const cloudMemory = await this.downloadFromOracle();
      
      // Ensure local directory exists
      await fs.mkdir(path.dirname(LOCAL_MEMORY_PATH), { recursive: true });
      
      // Save to local file for backup
      await fs.writeFile(LOCAL_MEMORY_PATH, JSON.stringify(cloudMemory, null, 2));
      
      return cloudMemory;
    } catch (error) {
      console.error(`❌ Failed to load from Oracle, trying local file: ${error.message}`);
      
      // Fallback to local file
      try {
        const localData = await fs.readFile(LOCAL_MEMORY_PATH, 'utf8');
        return JSON.parse(localData);
      } catch (localError) {
        console.log(`⚠️  No local memory file, starting fresh`);
        return { entities: [], relations: [] };
      }
    }
  }

  async saveMemory(memoryData) {
    try {
      // Save to Oracle Cloud
      await this.uploadToOracle(memoryData);
      
      // Also save locally as backup
      await fs.writeFile(LOCAL_MEMORY_PATH, JSON.stringify(memoryData, null, 2));
      
      return true;
    } catch (error) {
      console.error(`❌ Failed to save memory: ${error.message}`);
      return false;
    }
  }

  setupHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'create_entities',
            description: 'Create multiple new entities in the knowledge graph',
            inputSchema: {
              type: 'object',
              properties: {
                entities: {
                  type: 'array',
                  items: {
                    type: 'object',
                    properties: {
                      name: { type: 'string' },
                      entityType: { type: 'string' },
                      observations: {
                        type: 'array',
                        items: { type: 'string' }
                      }
                    },
                    required: ['name', 'entityType', 'observations']
                  }
                }
              },
              required: ['entities']
            }
          },
          {
            name: 'create_relations',
            description: 'Create multiple new relations between entities',
            inputSchema: {
              type: 'object',
              properties: {
                relations: {
                  type: 'array',
                  items: {
                    type: 'object',
                    properties: {
                      from: { type: 'string' },
                      to: { type: 'string' },
                      relationType: { type: 'string' }
                    },
                    required: ['from', 'to', 'relationType']
                  }
                }
              },
              required: ['relations']
            }
          },
          {
            name: 'read_graph',
            description: 'Read the entire knowledge graph',
            inputSchema: {
              type: 'object',
              properties: {},
              additionalProperties: false
            }
          },
          {
            name: 'search_nodes',
            description: 'Search for nodes in the knowledge graph',
            inputSchema: {
              type: 'object',
              properties: {
                query: { type: 'string' }
              },
              required: ['query']
            }
          }
        ]
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        const memory = await this.loadMemory();

        switch (name) {
          case 'create_entities':
            for (const entity of args.entities) {
              memory.entities = memory.entities || [];
              memory.entities.push({
                type: 'entity',
                name: entity.name,
                entityType: entity.entityType,
                observations: entity.observations
              });
            }
            await this.saveMemory(memory);
            return {
              content: [{
                type: 'text',
                text: JSON.stringify(args.entities, null, 2)
              }]
            };

          case 'create_relations':
            for (const relation of args.relations) {
              memory.relations = memory.relations || [];
              memory.relations.push({
                type: 'relation',
                from: relation.from,
                to: relation.to,
                relationType: relation.relationType
              });
            }
            await this.saveMemory(memory);
            return {
              content: [{
                type: 'text',
                text: JSON.stringify(args.relations, null, 2)
              }]
            };

          case 'read_graph':
            return {
              content: [{
                type: 'text',
                text: JSON.stringify(memory, null, 2)
              }]
            };

          case 'search_nodes':
            const query = args.query.toLowerCase();
            const matchingEntities = memory.entities?.filter(entity => 
              entity.name.toLowerCase().includes(query) ||
              entity.entityType.toLowerCase().includes(query) ||
              entity.observations.some(obs => obs.toLowerCase().includes(query))
            ) || [];
            
            return {
              content: [{
                type: 'text',
                text: JSON.stringify({ entities: matchingEntities }, null, 2)
              }]
            };

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        throw new Error(`Tool execution failed: ${error.message}`);
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('🚀 Oracle Memory Server started with cloud sync!');
  }
}

const server = new OracleMemoryServer();
server.run().catch(console.error);
