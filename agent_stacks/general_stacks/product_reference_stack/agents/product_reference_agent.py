from agents.basic_agent import BasicAgent
import json
from datetime import datetime
import random


class ProductReferenceAgent(BasicAgent):
    def __init__(self):
        self.name = "ProductReference"
        self.metadata = {
            "name": self.name,
            "description": "Provides comprehensive product information, specifications, comparisons, and recommendations. Access detailed product catalogs, technical specs, and intelligent search capabilities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product search query or question"
                    },
                    "product_id": {
                        "type": "string",
                        "description": "Optional. Specific product ID for detailed information"
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional. Product category to filter results"
                    },
                    "comparison_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. List of product IDs to compare"
                    },
                    "include_alternatives": {
                        "type": "boolean",
                        "description": "Optional. Include alternative product suggestions"
                    },
                    "technical_level": {
                        "type": "string",
                        "description": "Optional. Level of technical detail",
                        "enum": ["basic", "intermediate", "advanced"]
                    }
                },
                "required": ["query"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        query = kwargs.get('query')
        product_id = kwargs.get('product_id')
        category = kwargs.get('category')
        comparison_ids = kwargs.get('comparison_ids', [])
        include_alternatives = kwargs.get('include_alternatives', True)
        technical_level = kwargs.get('technical_level', 'intermediate')

        try:
            if not query or not query.strip():
                raise ValueError("Query is required and cannot be empty")

            # Generate product reference data
            reference_data = self._generate_product_reference(
                query, product_id, category, comparison_ids, 
                include_alternatives, technical_level
            )

            return json.dumps({
                "status": "success",
                "message": f"Found product information for: {query}",
                "data": reference_data
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to retrieve product reference: {str(e)}"
            })

    def _generate_product_reference(self, query, product_id, category, comparison_ids, 
                                   include_alternatives, technical_level):
        """Generate comprehensive product reference data"""
        
        reference = {
            "query": query,
            "results_count": random.randint(5, 20),
            "primary_product": {
                "product_id": product_id or f"PRD-{random.randint(1000, 9999)}",
                "name": "ProMax Enterprise Solution X500",
                "category": category or "Enterprise Software",
                "manufacturer": "TechCorp Industries",
                "model_number": "X500-ENT-2024",
                "release_date": "2024-01-15",
                "status": "Available",
                "price": {
                    "list_price": "$4,999",
                    "discount_price": "$4,499",
                    "volume_pricing": "Available for 10+ units",
                    "subscription": "$199/month"
                },
                "ratings": {
                    "overall": 4.7,
                    "performance": 4.8,
                    "reliability": 4.9,
                    "value": 4.5,
                    "support": 4.6,
                    "total_reviews": 342
                }
            },
            "specifications": self._generate_specifications(technical_level),
            "features": [
                "Advanced AI-powered analytics",
                "Real-time data synchronization",
                "Multi-platform compatibility",
                "Enterprise-grade security",
                "24/7 customer support",
                "Customizable dashboard",
                "API integration support",
                "Automated reporting"
            ],
            "use_cases": [
                {
                    "industry": "Finance",
                    "scenario": "Risk assessment and portfolio management",
                    "benefits": "40% reduction in analysis time"
                },
                {
                    "industry": "Healthcare",
                    "scenario": "Patient data management and analytics",
                    "benefits": "30% improvement in care coordination"
                },
                {
                    "industry": "Retail",
                    "scenario": "Inventory optimization and demand forecasting",
                    "benefits": "25% reduction in stockouts"
                }
            ],
            "compatibility": {
                "operating_systems": ["Windows 10+", "macOS 12+", "Linux Ubuntu 20.04+"],
                "browsers": ["Chrome 90+", "Firefox 88+", "Safari 14+", "Edge 90+"],
                "mobile": ["iOS 14+", "Android 11+"],
                "integrations": ["Salesforce", "Microsoft 365", "SAP", "Oracle", "Slack"]
            },
            "documentation": {
                "user_guide": "https://docs.example.com/x500/user-guide",
                "api_reference": "https://docs.example.com/x500/api",
                "video_tutorials": "https://learn.example.com/x500",
                "quick_start": "https://docs.example.com/x500/quickstart",
                "faq": "https://support.example.com/x500/faq"
            }
        }

        # Add comparison if requested
        if comparison_ids:
            reference["comparison"] = self._generate_comparison(comparison_ids)

        # Add alternatives if requested
        if include_alternatives:
            reference["alternatives"] = self._generate_alternatives()

        # Add recommendations
        reference["recommendations"] = {
            "best_for": ["Large enterprises", "Data-intensive operations", "Multi-team collaboration"],
            "not_recommended_for": ["Small businesses with < 10 employees", "Basic use cases"],
            "complementary_products": [
                {"name": "DataSync Pro", "purpose": "Enhanced data migration"},
                {"name": "SecureVault", "purpose": "Additional security layer"},
                {"name": "Analytics Plus", "purpose": "Advanced reporting"}
            ],
            "upgrade_path": "X500 Pro → X700 Enterprise → X900 Ultimate"
        }

        # Add availability information
        reference["availability"] = {
            "in_stock": True,
            "locations": ["Online", "Partner Network", "Direct Sales"],
            "lead_time": "2-3 business days",
            "trial_available": True,
            "trial_duration": "30 days",
            "demo_available": True
        }

        return reference

    def _generate_specifications(self, technical_level):
        """Generate product specifications based on technical level"""
        specs = {
            "basic": {
                "Processing": "High-performance",
                "Storage": "1TB included",
                "Users": "Unlimited",
                "Support": "24/7 available"
            },
            "intermediate": {
                "Processing": {
                    "CPU": "8-core minimum",
                    "RAM": "16GB recommended",
                    "Throughput": "10,000 transactions/second"
                },
                "Storage": {
                    "Included": "1TB",
                    "Max": "Unlimited with cloud",
                    "Type": "SSD recommended"
                },
                "Network": {
                    "Bandwidth": "100 Mbps minimum",
                    "Latency": "< 50ms recommended",
                    "Protocol": "HTTPS/TLS 1.3"
                },
                "Security": {
                    "Encryption": "AES-256",
                    "Authentication": "Multi-factor",
                    "Compliance": "SOC 2, GDPR, HIPAA"
                }
            },
            "advanced": {
                "Architecture": {
                    "Type": "Microservices",
                    "Deployment": "Kubernetes/Docker",
                    "Scaling": "Horizontal auto-scaling",
                    "Load Balancing": "Round-robin with health checks"
                },
                "Performance": {
                    "CPU": {
                        "Cores": "8-32 (scalable)",
                        "Architecture": "x86_64 or ARM64",
                        "Utilization": "Average 40-60%"
                    },
                    "Memory": {
                        "RAM": "16-128GB",
                        "Cache": "Redis/Memcached",
                        "Garbage Collection": "G1GC optimized"
                    },
                    "I/O": {
                        "Disk": "NVMe SSD, 5000+ IOPS",
                        "Network": "10 Gbps fiber",
                        "Database": "PostgreSQL 14+, MongoDB 5+"
                    }
                },
                "API": {
                    "Type": "RESTful and GraphQL",
                    "Rate Limits": "10,000 req/min",
                    "Authentication": "OAuth 2.0/JWT",
                    "Versioning": "Semantic versioning"
                }
            }
        }
        
        return specs.get(technical_level, specs['intermediate'])

    def _generate_comparison(self, comparison_ids):
        """Generate product comparison data"""
        products = ["ProMax X500", "CompetitorA Pro", "CompetitorB Enterprise"]
        comparison = {
            "products": products[:len(comparison_ids) + 1],
            "features": {
                "AI Analytics": ["Yes", "Yes", "Limited"],
                "Real-time Sync": ["Yes", "No", "Yes"],
                "API Access": ["Full", "Limited", "Full"],
                "Mobile App": ["Yes", "Yes", "No"],
                "Custom Reports": ["Unlimited", "10/month", "5/month"],
                "Storage": ["1TB", "500GB", "750GB"],
                "Support": ["24/7", "Business hours", "24/7"],
                "Price": ["$4,999", "$5,499", "$4,299"]
            },
            "verdict": {
                "winner": "ProMax X500",
                "reason": "Best overall value with superior features and support",
                "pros": ["Most features", "Best support", "Competitive pricing"],
                "cons": ["Higher learning curve", "Requires more setup time"]
            }
        }
        return comparison

    def _generate_alternatives(self):
        """Generate alternative product suggestions"""
        return [
            {
                "product_id": "PRD-3847",
                "name": "ProMax X300 Standard",
                "reason": "More affordable option with core features",
                "price": "$2,999",
                "match_score": 0.85
            },
            {
                "product_id": "PRD-7621",
                "name": "QuickStart Business Suite",
                "reason": "Easier implementation for smaller teams",
                "price": "$1,999",
                "match_score": 0.72
            },
            {
                "product_id": "PRD-9102",
                "name": "Enterprise Pro Maximum",
                "reason": "Premium option with additional features",
                "price": "$7,999",
                "match_score": 0.68
            }
        ]


if __name__ == "__main__":
    agent = ProductReferenceAgent()
    
    # Test product reference lookup
    result = agent.perform(
        query="enterprise analytics solution with AI capabilities",
        category="Enterprise Software",
        include_alternatives=True,
        technical_level="intermediate",
        comparison_ids=["PRD-001", "PRD-002"]
    )
    
    print(json.dumps(json.loads(result), indent=2))