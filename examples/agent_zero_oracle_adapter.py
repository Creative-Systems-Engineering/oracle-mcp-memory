#!/usr/bin/env python3
"""
Agent-Zero Oracle Memory Adapter
Connects Agent-Zero to Oracle Cloud Storage for persistent, shared AI memory
"""

import requests
import json
import os
import datetime
from typing import Dict, List, Any, Optional

class OracleMemoryAdapter:
    """
    Memory adapter that connects Agent-Zero to Oracle Cloud Storage
    Enables shared memory across multiple AI agents and environments
    """
    
    def __init__(self, oracle_base_url: Optional[str] = None):
        self.oracle_base_url = oracle_base_url or os.getenv("ORACLE_BASE_URL", "")
        if not self.oracle_base_url:
            raise ValueError("ORACLE_BASE_URL environment variable must be set")
            
        self.memory_object = "agent-zero-memory.json"
        self.agent_id = "agent-zero"
        
    def load_memory(self) -> Dict[str, Any]:
        """Load complete memory from Oracle Cloud Storage"""
        try:
            url = f"{self.oracle_base_url}{self.memory_object}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ Loaded memory from Oracle Cloud")
                return response.json()
            elif response.status_code == 404:
                print(f"⚠️ No existing memory found, starting fresh")
                return self._create_empty_memory()
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except requests.RequestException as e:
            print(f"❌ Network error loading memory: {e}")
            return self._create_empty_memory()
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in memory file: {e}")
            return self._create_empty_memory()
        except Exception as e:
            print(f"❌ Unexpected error loading memory: {e}")
            return self._create_empty_memory()
    
    def save_memory(self, memory_data: Dict[str, Any]) -> bool:
        """Save complete memory to Oracle Cloud Storage"""
        try:
            url = f"{self.oracle_base_url}{self.memory_object}"
            headers = {"Content-Type": "application/json"}
            
            # Add metadata
            memory_data["last_updated"] = datetime.datetime.now().isoformat()
            memory_data["updated_by"] = self.agent_id
            
            response = requests.put(url, 
                                  data=json.dumps(memory_data, indent=2),
                                  headers=headers,
                                  timeout=30)
            
            if response.status_code in [200, 201]:
                print(f"✅ Memory saved to Oracle Cloud")
                return True
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except requests.RequestException as e:
            print(f"❌ Network error saving memory: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error saving memory: {e}")
            return False
    
    def add_entity(self, name: str, entity_type: str, observations: List[str]) -> bool:
        """Add a new knowledge entity to memory"""
        memory = self.load_memory()
        
        # Check if entity already exists
        for entity in memory["entities"]:
            if entity["name"] == name and entity["entityType"] == entity_type:
                # Update existing entity
                entity["observations"].extend(observations)
                entity["last_updated_by"] = self.agent_id
                break
        else:
            # Add new entity
            memory["entities"].append({
                "name": name,
                "entityType": entity_type,
                "observations": observations,
                "created_by": self.agent_id,
                "created_at": datetime.datetime.now().isoformat()
            })
        
        return self.save_memory(memory)
    
    def add_relation(self, from_entity: str, to_entity: str, relation_type: str) -> bool:
        """Add a relationship between entities"""
        memory = self.load_memory()
        
        # Check if relation already exists
        for relation in memory["relations"]:
            if (relation["from"] == from_entity and 
                relation["to"] == to_entity and 
                relation["relationType"] == relation_type):
                return True  # Relation already exists
        
        # Add new relation
        memory["relations"].append({
            "from": from_entity,
            "to": to_entity,
            "relationType": relation_type,
            "created_by": self.agent_id,
            "created_at": datetime.datetime.now().isoformat()
        })
        
        return self.save_memory(memory)
    
    def add_agent_session(self, task: str, outcome: str, learned_facts: List[str], 
                         environment: Optional[Dict] = None) -> bool:
        """Record an Agent-Zero session with learnings"""
        memory = self.load_memory()
        
        session_data = {
            "session_id": f"{self.agent_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "agent_id": self.agent_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "task": task,
            "outcome": outcome,
            "learned_facts": learned_facts,
            "environment": environment or {}
        }
        
        memory["agent_sessions"].append(session_data)
        
        # Also add learned facts as entities
        for fact in learned_facts:
            self.add_entity(
                name=f"Learning: {fact[:50]}...",
                entity_type="learned_fact",
                observations=[fact, f"Learned during: {task}"]
            )
        
        return self.save_memory(memory)
    
    def search_entities(self, query: str) -> List[Dict[str, Any]]:
        """Search for entities matching query"""
        memory = self.load_memory()
        query_lower = query.lower()
        
        matching_entities = []
        for entity in memory["entities"]:
            if (query_lower in entity["name"].lower() or
                query_lower in entity["entityType"].lower() or
                any(query_lower in obs.lower() for obs in entity["observations"])):
                matching_entities.append(entity)
        
        return matching_entities
    
    def get_related_experiences(self, task_description: str) -> List[Dict[str, Any]]:
        """Find past Agent-Zero sessions related to current task"""
        memory = self.load_memory()
        task_words = set(task_description.lower().split())
        
        related_sessions = []
        for session in memory.get("agent_sessions", []):
            session_words = set(session.get("task", "").lower().split())
            
            # Calculate word overlap
            overlap = len(task_words.intersection(session_words))
            if overlap > 0:
                session["relevance_score"] = overlap / len(task_words.union(session_words))
                related_sessions.append(session)
        
        # Sort by relevance
        related_sessions.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return related_sessions[:10]  # Return top 10 most relevant
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about current memory state"""
        memory = self.load_memory()
        
        return {
            "total_entities": len(memory.get("entities", [])),
            "total_relations": len(memory.get("relations", [])),
            "total_sessions": len(memory.get("agent_sessions", [])),
            "agents_involved": list(set(
                entity.get("created_by", "unknown") 
                for entity in memory.get("entities", [])
            )),
            "last_updated": memory.get("last_updated", "Never"),
            "memory_size_kb": len(json.dumps(memory)) / 1024
        }
    
    def _create_empty_memory(self) -> Dict[str, Any]:
        """Create an empty memory structure"""
        return {
            "entities": [],
            "relations": [],
            "agent_sessions": [],
            "created_at": datetime.datetime.now().isoformat(),
            "created_by": self.agent_id
        }


class AgentZeroWithOracle:
    """
    Enhanced Agent-Zero class with Oracle Cloud memory integration
    """
    
    def __init__(self, oracle_base_url: Optional[str] = None):
        self.memory = OracleMemoryAdapter(oracle_base_url)
        self.current_task = None
        self.session_start = None
        
    def start_task(self, task_description: str) -> List[Dict[str, Any]]:
        """Start a new task with memory-assisted context"""
        self.current_task = task_description
        self.session_start = datetime.datetime.now()
        
        print(f"🚀 Starting task: {task_description}")
        
        # Get related experiences
        related = self.memory.get_related_experiences(task_description)
        
        if related:
            print(f"🧠 Found {len(related)} related experiences:")
            for i, exp in enumerate(related[:3], 1):
                print(f"   {i}. {exp['task']} → {exp['outcome']}")
                if exp.get("learned_facts"):
                    print(f"      💡 Key learning: {exp['learned_facts'][0]}")
        else:
            print("🆕 No related experiences found - this is new territory!")
            
        return related
    
    def learn_fact(self, fact: str, entity_type: str = "knowledge") -> bool:
        """Learn and remember a new fact"""
        return self.memory.add_entity(
            name=f"Fact: {fact[:50]}...",
            entity_type=entity_type,
            observations=[fact, f"Learned during: {self.current_task}"]
        )
    
    def establish_relationship(self, from_concept: str, to_concept: str, 
                             relationship: str) -> bool:
        """Establish a relationship between concepts"""
        return self.memory.add_relation(from_concept, to_concept, relationship)
    
    def complete_task(self, outcome: str, learned_facts: List[str], 
                     environment: Optional[Dict] = None) -> bool:
        """Complete current task and save all learnings"""
        if not self.current_task:
            print("❌ No active task to complete")
            return False
            
        duration = datetime.datetime.now() - self.session_start
        
        env_data = environment or {}
        env_data.update({
            "duration_seconds": duration.total_seconds(),
            "completed_at": datetime.datetime.now().isoformat()
        })
        
        success = self.memory.add_agent_session(
            task=self.current_task,
            outcome=outcome,
            learned_facts=learned_facts,
            environment=env_data
        )
        
        if success:
            print(f"✅ Task completed and saved to Oracle Cloud")
            print(f"   📊 Duration: {duration}")
            print(f"   📝 Learned {len(learned_facts)} new facts")
        
        self.current_task = None
        self.session_start = None
        return success
    
    def show_memory_stats(self):
        """Display current memory statistics"""
        stats = self.memory.get_memory_stats()
        print(f"\n📊 Memory Statistics:")
        print(f"   🧠 Entities: {stats['total_entities']}")
        print(f"   🔗 Relations: {stats['total_relations']}")
        print(f"   📝 Sessions: {stats['total_sessions']}")
        print(f"   🤖 Agents: {', '.join(stats['agents_involved'])}")
        print(f"   💾 Size: {stats['memory_size_kb']:.1f} KB")
        print(f"   🕐 Last Updated: {stats['last_updated']}")


# Example usage
if __name__ == "__main__":
    # Set up Oracle connection
    oracle_url = os.getenv("ORACLE_BASE_URL")
    if not oracle_url:
        print("❌ Please set ORACLE_BASE_URL environment variable")
        exit(1)
    
    # Create Agent-Zero with Oracle memory
    agent = AgentZeroWithOracle(oracle_url)
    
    # Show current memory state
    agent.show_memory_stats()
    
    # Example task workflow
    related_experiences = agent.start_task("Analyze Python code for security vulnerabilities")
    
    # Simulate learning during task
    agent.learn_fact("SQL injection vulnerabilities often occur in dynamic query construction")
    agent.learn_fact("Use parameterized queries to prevent SQL injection")
    agent.establish_relationship("SQL Injection", "Parameterized Queries", "prevented_by")
    
    # Complete the task
    agent.complete_task(
        outcome="Successfully identified 3 potential security issues",
        learned_facts=[
            "Bandit tool is effective for Python security analysis",
            "Common issues: hardcoded passwords, SQL injection risks",
            "Fixed all issues using secure coding practices"
        ],
        environment={
            "tools_used": ["bandit", "safety"],
            "files_analyzed": 15,
            "issues_found": 3
        }
    )
    
    # Show updated stats
    agent.show_memory_stats()
