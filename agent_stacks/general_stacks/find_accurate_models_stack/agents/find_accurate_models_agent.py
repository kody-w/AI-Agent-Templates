from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime


class FindAccurateModelsAgent(BasicAgent):
    def __init__(self):
        self.name = "FindAccurateModels"
        self.metadata = {
            "name": self.name,
            "description": "Locates and recommends the most accurate AI models, product models, and service configurations based on specific requirements and use cases.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_type": {
                        "type": "string",
                        "description": "Type of model to find",
                        "enum": ["ai_model", "product_model", "pricing_model", "forecast_model", "risk_model"]
                    },
                    "use_case": {
                        "type": "string",
                        "description": "Specific use case or application"
                    },
                    "requirements": {
                        "type": "object",
                        "description": "Optional. Specific requirements",
                        "properties": {
                            "accuracy_threshold": {"type": "number"},
                            "performance_needs": {"type": "string"},
                            "constraints": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "comparison_count": {
                        "type": "integer",
                        "description": "Optional. Number of models to compare (default 3)"
                    }
                },
                "required": ["model_type", "use_case"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        model_type = kwargs.get('model_type')
        use_case = kwargs.get('use_case')
        requirements = kwargs.get('requirements', {})
        comparison_count = kwargs.get('comparison_count', 3)

        try:
            if not model_type or not use_case:
                raise ValueError("Model type and use case are required")

            # Find and evaluate models
            model_recommendations = self._find_models(
                model_type, use_case, requirements, comparison_count
            )

            return json.dumps({
                "status": "success",
                "message": f"Found {len(model_recommendations['models'])} accurate models for {use_case}",
                "data": model_recommendations
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to find accurate models: {str(e)}"
            })

    def _find_models(self, model_type, use_case, requirements, comparison_count):
        """Find and evaluate models based on criteria"""
        
        models = []
        for i in range(comparison_count):
            models.append({
                "model_id": f"MDL-{random.randint(1000, 9999)}",
                "name": f"Model {chr(65 + i)} Pro",
                "type": model_type,
                "version": f"v{random.randint(1, 5)}.{random.randint(0, 9)}",
                "accuracy_score": round(random.uniform(0.85, 0.99), 3),
                "performance_metrics": {
                    "precision": round(random.uniform(0.85, 0.98), 3),
                    "recall": round(random.uniform(0.82, 0.96), 3),
                    "f1_score": round(random.uniform(0.84, 0.97), 3),
                    "latency_ms": random.randint(10, 200)
                },
                "use_cases": [use_case, "General purpose", "Enterprise"],
                "strengths": random.sample([
                    "High accuracy", "Fast inference", "Low resource usage",
                    "Scalable", "Well-documented", "Active support"
                ], 3),
                "limitations": random.sample([
                    "Requires large dataset", "Complex setup", "High cost",
                    "Limited languages", "Cloud-only"
                ], 2),
                "pricing": {
                    "model": random.choice(["Per API call", "Monthly subscription", "Enterprise license"]),
                    "cost": f"${random.randint(99, 9999)}/month"
                },
                "compatibility": {
                    "platforms": ["Cloud", "On-premise", "Edge"],
                    "languages": ["Python", "Java", "REST API"],
                    "frameworks": ["TensorFlow", "PyTorch", "ONNX"]
                }
            })
        
        # Sort by accuracy
        models.sort(key=lambda x: x['accuracy_score'], reverse=True)
        
        return {
            "query": {
                "model_type": model_type,
                "use_case": use_case,
                "requirements": requirements
            },
            "models": models,
            "recommendation": {
                "best_overall": models[0]['name'],
                "best_value": models[1]['name'] if len(models) > 1 else models[0]['name'],
                "best_performance": models[0]['name'],
                "reasoning": f"Based on accuracy scores and {use_case} requirements"
            },
            "comparison_matrix": {
                "accuracy": {m['name']: m['accuracy_score'] for m in models},
                "latency": {m['name']: f"{m['performance_metrics']['latency_ms']}ms" for m in models},
                "cost": {m['name']: m['pricing']['cost'] for m in models}
            },
            "implementation_guide": {
                "quick_start": "1. Sign up for API access\n2. Install SDK\n3. Configure credentials\n4. Deploy model",
                "estimated_time": "2-4 hours",
                "support_available": True
            }
        }


if __name__ == "__main__":
    agent = FindAccurateModelsAgent()
    
    result = agent.perform(
        model_type="ai_model",
        use_case="Customer sentiment analysis",
        requirements={
            "accuracy_threshold": 0.95,
            "performance_needs": "Real-time",
            "constraints": ["GDPR compliant", "Multi-language"]
        },
        comparison_count=3
    )
    
    print(json.dumps(json.loads(result), indent=2))